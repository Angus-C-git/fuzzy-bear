from .. import Strategy
from xml.dom import minidom
import random
#from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom as md

MAX_DEPTH = 300


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = md.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def nest_em(elem_obj,insert_text, count=0):
    if(count == MAX_DEPTH):
        return elem_obj
    for child in elem_obj:
        #child.append(new)
        sub_elm = SubElement(child,'inner')
        sub_elm.text = insert_text
        nest_em(child,insert_text, count+1)


def change_id(elem_obj, new_ID):
    for child in elem_obj:
        if 'id' in child.attrib.keys():
            print(child)
            child.attrib["id"] = new_ID
#spicy files

def spicy_file():
    
    spicy_string = '''
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE root [
 <!ENTITY spooky SYSTEM "file:///dev/random">
  ]>
  <root>&spooky;</root>
    '''
    return spicy_string


class XML(Strategy.Strategy):
    
    # parse xml input data
    def __init__(self, sample_input):
        super()
        self.sample_input = sample_input
        with open(sample_input) as xmlfile:
            element_tree = ET.parse(xmlfile)
            self.candidate_input = element_tree.getroot()

    # run strategies
    def run(self):
        print(f"\n   [DEBUG] mutating {self.candidate_input} \n")        

        mutation = self.candidate_input
        for emoji in super().emoji():
            nest_em(mutation, emoji)   
            yield prettify(mutation)
        
        
        for chonk in super().chonk():
            change_id(mutation, chonk)
            yield prettify(mutation)

        mutation = spicy_file() 
        print(f"[>>] mutation was {mutation}")
        yield mutation

