from .. import Strategy
from xml.dom import minidom

class XML(Strategy.Strategy):
    
    # parse ___ input data
    def __init__(self, sample_input):
        pass

import random
#from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom as md

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = md.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

#dev random (big file)

def nest_em(elem_obj, count=0):
    if(count == 10):
        return elem_obj
    #new = Element('p')
    #new.text = 'that\'s deep man'
    #sub_elm = SubElement(new,'inner')
    for child in elem_obj:
        #child.append(new)
        sub_elm = SubElement(child,'inner')
        #to be arg later
        sub_elm.text = 'hecc'
        nest_em(child,count+1)


def change_id(elem_obj, new_ID):
    for child in elem_obj:
        if 'id' in child.attrib.keys():
            print(child)
            child.attrib["id"] = new_ID
#spicy files

tree = ET.parse('og.xml')
root = tree.getroot()

#nest_em(root)
change_id(root, 1000)
print(prettify(root))
