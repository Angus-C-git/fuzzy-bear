from .. import Strategy
from xml.dom import minidom
import random
#from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom as md
import copy


MAX_DEPTH = 100
target_elements = ['href', 'id', 'style', 'class']


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = md.parseString(rough_string)
    tmp = reparsed.toprettyxml(indent="  ")[23:]
    return tmp


def nest_em(elem_obj,insert_text, count=0):
    if(count == MAX_DEPTH):
        return elem_obj
    for child in elem_obj:
        #child.append(new)
        sub_elm = SubElement(child,'inner')
        sub_elm.text = insert_text
        nest_em(child, insert_text, count+1)


def change_element(elem_obj, new_elm, elem_type):
    for child in elem_obj.iter():
        if elem_type in child.attrib.keys():
            base_str = child.attrib[elem_type]
            child.attrib[elem_type] = base_str + base_str + base_str + base_str + base_str + base_str + base_str + new_elm


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



def fmt_string_insert():
    return (
        """
<html>
    <head>
        <link href="http://somewebsite.com" />
    </head>
    <body>
        <h1>I'm not a web developer.</h1>
    </body>

    <div id="#lol">
        <a href="http://google.com">Here is some link...</a>
    </div>


    <tail>
        <a href="http://bing.comhttp://bing.comhttp://bing.comhttp://bing.comhttp://bing.comhttp://bing.comhttp://bing.comhttp://bing.comhttp://bing.com%p%p%400$n">Footer link</a>
    </tail>
</html>
  
        """
    )


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
        # print(f"\n   [DEBUG] mutating {self.candidate_input} \n")        

        mutation = copy.deepcopy(self.candidate_input)
        emoji = next(super().emoji())
        # removed loop here
        nest_em(mutation, emoji)   
        yield prettify(mutation)
        
        mutation = copy.deepcopy(self.candidate_input)
        for chonk in super().chonk():
            for e in target_elements:
                change_element(mutation, chonk, e)
            yield prettify(mutation)

        mutation = spicy_file() 
        # print(f"[>>] mutation was {mutation}")
        yield mutation

    
        for fstring in super().format_strings():
            mutation = copy.deepcopy(self.candidate_input)
            for e in target_elements:
                change_element(mutation, fstring, e)
            
            try:
                # print("[>>] mutation was ", prettify(mutation))
                yield prettify(mutation)
            except:
                print("[>>] failed to yield")
                pass
