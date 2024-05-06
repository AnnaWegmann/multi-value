import unittest
import src.Dialects
from src import wiki_streamer
import pandas as pd
import json


def transform_string(sae_text, function_name, transformer=None):
    if transformer is None:
        transformer = src.Dialects.DialectFromVector(dialect_name="all")
    feature_id_to_function_name = transformer.load_dict('resources/feature_id_to_function_name.json')
    all_function_names = [value[0] for value in feature_id_to_function_name.values()]
    assert function_name in all_function_names, "Function not found in feature_id_to_function_name.json"
    transformer.clear()
    transformer.update(sae_text)
    method = getattr(transformer, function_name)
    method()
    synth_dialect = transformer.compile_from_rules()
    return synth_dialect

def save_list_to_file(my_list, filename):
    # Open the file in write mode ('w')
    with open(filename, 'w') as f:
        # Iterate over the list
        for item in my_list:
            # Write each item on a new line
            f.write("%s\n" % item)

class TestStringMethods(unittest.TestCase):
    def test_on_string(self):
        sae_text = "You gave me this bike and it's a good bike"
        transformed_text = transform_string(sae_text, 'she_inanimate_objects')
        print(transformed_text)
        self.assertEqual("You gave me this bike and she's a good bike", transformed_text)

        sae_text = "Okay, it is time for lunch."
        transformed_text = transform_string(sae_text, 'it_is_non_referential')
        print(transformed_text)
        self.assertEqual("Okay, is time for lunch.", transformed_text)

        # strange: "It’s a good bike" doesn't transform to "She’s a good bike"
        sae_text = "It is very nice food."
        transformed_text = transform_string(sae_text, 'it_is_referential')
        print(transformed_text)
        self.assertEqual("Is very nice food.", transformed_text)

    def test_on_wiki(self):
        wiki_stream = wiki_streamer.Abstracts()
        transformer = src.Dialects.DialectFromVector(dialect_name="all")

        wiki_sentences = []
        it_is_non_referential = []

        feature_id_to_function_name = transformer.load_dict('resources/feature_id_to_function_name.json')
        all_function_names = [value[0] for value in feature_id_to_function_name.values()]

        possibilities = ['negative_concord', 'it_is_non_referential', 'never_negator', 'regularized_plurals']
        function_name = 'regularized_plurals'

        for function_name in all_function_names:
            wiki_sentences = []
            it_is_non_referential = []

            for i, s in enumerate(wiki_stream):
                transformed = transform_string(s, function_name, transformer)
                if transformed != s:
                    wiki_sentences.append(s)
                    it_is_non_referential.append(transformed)
                    print(s)
                    print(transformed)

                if len(wiki_sentences) >= 200:
                    break

                if i % 100 == 0:
                    print(i)

                if i > 10000:
                    break

            save_list_to_file(wiki_sentences, f"output/{function_name}_transformed-wiki_{len(wiki_sentences)}.txt")
            save_list_to_file(it_is_non_referential, f"output/{function_name}_org-wiki_{len(wiki_sentences)}.txt")
