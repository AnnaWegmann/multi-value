class Abstracts:
    """
    Generator of Wiki abstracts, copied from https://github.com/nlpsoc/STEL/blob/f73c6635c017cd50ce21a8b0fc98f6c5cb62e6fd/src/STEL/utility/base_generators.py#L6
    """

    def __init__(self, filename_wiki_abstracts="../STEL/Data/Datasets/enwiki-20181220-abstract.xml",
                 must_include=None):
        self.xml_filename = filename_wiki_abstracts
        # <feed>
        #   <doc>
        #     <abstract>
        import xml.etree.ElementTree as ET
        self.elem_iter = ET.iterparse(self.xml_filename)  # , events=("start", "end"))
        self.must_include = must_include

    def __iter__(self):
        for event, elem in self.elem_iter:
            # if event == 'end':
            # if elem.tag == 'doc':
            #    logging.info(elem.tag)
            if elem.tag == 'abstract':
                if elem.text and len(elem.text) > 10 and "." in elem.text and not "|" in elem.text \
                        and "{" not in elem.text and "}" not in elem.text \
                        and "(" not in elem.text and ")" not in elem.text:
                    if self.must_include and self.must_include not in elem.text:
                        continue
                    for sentence in elem.text.split(". "):
                        yield sentence
