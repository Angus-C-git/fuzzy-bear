from .. import Strategy


#creating the start of the pdf document
def create_header():
    return '%PDF-1.4\n'

#Creating the middle components of the pdf document
def pdf_object():
    pass

def create_resource_obj(obj_num, font_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Font << /F8 ' + str(font_num) + ' 0 R >>\n'
    stream += '/ProcSet [/PDF / Text]\n'
    stream += '>>\n'
    stream += 'endobj'

def type_obj(obj_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Type /Font\n'
    stream += '/Subtype /Type1\n'
    stream += '/BaseFont /Helvetica-Bold\n'
    stream += '/Encoding /WinAnsiEncoding\n'
    stream += '>>\n'
    stream += 'endobj\n'
    return stream

def page_node_obj(obj_num,page_leaf):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Type /Pages\n'
    stream += '/Kids [\n'
    for i in page_leaf:
        stream += str(i) + ' 0 R\n'
    stream += ']\n'
    stream += '/Count '+ str(len(page_leaf)) + '\n'
    stream += '>>\nendobj\n'
    return page_leaf_obj

def page_leaf_obj(obj_num ,parent_node_num, resource_obj_num, contents_obj_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Type /Page\n'
    stream += '/Parent ' + str(parent_node_num)+ ' 0 R\n'
    stream += '/Resources ' + str(resource_obj_num)+ ' 0 R\n'
    stream += '/Contents ' + str(contents_obj_num) + ' 0 R\n'
    stream += '/MediaBox [0 0 595.276 841.89]\n'
    stream += '>>\n'
    stream += 'endobj\n'
    return stream

def doc_catalog(obj_num, page_tree_obj_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Type /Catalog\n'
    stream += '/Pages '+str(page_tree_obj_num) + ' 0 R\n'
    stream += '>>\n'
    stream += 'endobj'
    return doc_catalog

def create_info_obj(obj_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Type /Info\n'
    stream += '/Producer (FuzzyBear fuzzer 11.1.1.1.1.11)\n'
    stream += '>>\n'
    stream += 'endobj\n'

#assuming data is a string
def create_stream(obj_num ,data, encoding):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    if encoding:
        stream += '/Filter /FlateDecode\n'
    stream += '/Length ' + str(len(data)) + '\n'
    stream += '>>\n'
    stream += 'stream\n'
    stream += str(data)
    stream += 'endstream\n'
    stream += 'endobj'
    return stream

##Creating the ending of the pdf document uses create_xref and create_trailer
def create_xref(object_locations):
    xref = 'xref\n'
    xref += '0 ' + str(len(object_locations)+1) + '\n'
    xref += '0000000000 65535 f\n'
    for i in object_locations:
        var = str(i)
        offset = 10-len(var) #NOTE var should be < 10 bytes long
        for i in range(0, offset):
            xref += '0'
        xref += var
        xref += ' '
        xref += '00000 n\n'
    return xref


#root_obj_id and info_obj_id must obj_id
#NOTE R is for indirect object
def create_trailer(root_obj_id, num_objects, info_obj_id, lenth_to_xref, prev_xref):
    trailer = 'trailer\n<<'
    trailer += '/Size '+ str(num_objects) + '\n'
    trailer += '/Root '+ str(root_obj_id) + ' 0 R\n'
    trailer += '/Info '+ str(info_obj_id) + ' 0 R\n'
    if(prev_xref != None):
        trailer += '/Prev '+ prev_xref
    trailer += '>>\n'
    trailer += 'startxref'
    trailer += lenth_to_xref
    trailer += '%%EOF'
    return trailer

#doc_catalog 1
#info 2
#page_node 3
#page_leaf 4 5
#stream location 6 7
#resouce_obj 8, 9
#font_obj 10, 11
def create_pdf_basic():
    obj_num = 1
    obj_locations = []
    pdf_document = ''
    pdf_document += create_header()
    obj_locations.append(len(pdf_document))
    pdf_document += doc_catalog(obj_num,3)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += create_info_obj(obj_num)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += page_node_obj(obj_num, [4, 5])
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += page_leaf_obj(obj_num , 3, 8, 6)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += page_leaf_obj(obj_num , 3, 9, 7)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += create_stream(obj_num ,"BT /F1 24 Tf 100 700 Td (Hello World)Tj ET", False)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += create_stream(obj_num ,"BT /F1 24 Tf 100 700 Td (Nice to meet you)Tj ET", False)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += create_resource_obj(obj_num, 10)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += create_resource_obj(obj_num, 11)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += type_obj(obj_num)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += type_obj(obj_num)

    length_to_xref = len(pdf_document)
    pdf_document += create_xref(obj_locations)
    pdf_document += create_trailer(1, obj_num, 2, length_to_xref, None)
    return pdf_document


class PDF(Strategy.Strategy):
    # parse ___ input data
    def __init__(self, sample_input):
        super()
        self.sample_input = sample_input
        self.parse_pdf()

    def parse_pdf(self):
        pass

    def run(self):
        yield(create_pdf_basic())



''' Dev Notes
- PDF file format

The pdf file structure is seperated into 4 main parts: The header, body 'xref' Table and trailer
https://opensource.adobe.com/dc-acrobat-sdk-docs/
https://resources.infosecinstitute.com/topic/pdf-file-format-basic-structure/   <<---- READ THIS!!!!!!!!!! PDF documents are really complicated... they're like an entire coding language

PDF allow you so store text, images, multimedia elements, they can be password protected, execute javascript etc.

The header:
The first line of a PDF specifies the version number of the used PDF spec this version number is hex encoded

e.g.: %PDF-1.3.%...
hex encoded: 2550 4446 2d31 2e33 0a25 c4e5 f2e5 eba7

the % symbol in pdf is actually a commend so the specification is commented out but it needs to be there fore the PDF reader

The following characters are non-printable ASCII text (non-printable characters) which are usually there to tell some of the software products that the file contains binary data and shouldn't be treated as 7-bit ASCII tesxt.

the version numbers go from 0-7 in the form 1.N 



The Body:
The Body of the PDF document contain the objects that are typically included these can be.

text streams, images and other media elements.
the body seciton is used to hold all the document's data being shown to the user.



xref table:
This is the cross reference table, which contains all the references to all the objects in the document.
It allows random access to objects in the file so you dont have to read the whole PDF document to locate the particular object.
Each object is represented by one entry in the cross reference table, which is always 20 bytes long

an example cross reference table:
xref
0 1
0000000023 65535 f
3 1
0000025324 00000 n
21 4
0000025518 00002 n
0000025632 00000 n
0000000024 00001 f
0000000000 00001 f
36 1
0000026900 00000 n

Note the 4 sections:
the numbers above (0 1, 3 1, 21 4, 36 1) are used to determin the number of objects in each section  and the object numbers
the first number refers to the object number 
the second number refers to the number of objects in the current subsection

The first 10 bytes are the object's offset from the start of the pdf document
the bytes that follow the space specifies the object's generation number. 
After that, the next space separator, followed by a letter 'f' or 'n' indicates whether the object is free or in use.

The first object has an ID - and always contains one entry with generation number 65535 which is at the head of the list of free objects.

The last object in the cross-reference table used the generation number 0.

All objects are marked with either an "f" or "n" flag meaning that the object may still be present in a file, but is marked as free, so it shouldn't be used. These objects contain a reference to the next free object and the generation number to be used if the object becomes valid again. The flag "n" is used to represent valid and used objects that contain the offset from the beginning of the file and generation number of the object

The generation number of the object is incremented when the object is freed, so if the object becomes valid again, the generation number of object 23 is 1, so if it becomes valid again, the generation number will still be 1, but if it's removed again, the generation number would increate to 2.

multiple subsections are usually present in PDF documents that have been incrementally updated, otherwise only one subsection starting with the number 0 should be present




Trailer:
The PDF trailer specifies how the application reading the PDF document should find the xref table and other special objects. All PDF readers should starting reading a PDF from the end of the file

trailer
&amp;amp;lt;&amp;amp;lt;
/Size 22
/Root 2 0 R
/Info 1 0 R
&amp;amp;gt;&amp;amp;gt;
startxref
24212
%%EOF

The line contains the end of the pdf document %%EOF

Before the end there is a tag startxref which specifies the offset from the beginning of the file to the cross-reference table.

Before that is a trailer string the specifies the start of the Trailer section.
The contents of the trailer sections are embedded with the << and >> characters (this is a dictionary that accepts key-value pairs).

There are several keys in the trailer section these being:

/Size [integer]: specifies the number of entries in the cross-reference table (counting the objects in the updated sections aswell). The used number shouldn't be an indirect reference

/Prev [integer]: Specifies the offset from the beginning of the file to the previous cross-reference section, which is used if there are multiple cross-reference sections. The number should be a cross-reference.

/Root [dictionary]: specifies the reference object for the document catalog object. which is a special object that contains various pointers to different kinds of other special objects

/Encrypt [dictionary]: specifies the documents encryption

/Info [dictionary]: specifies the reference object for the document's information dictionary

/ID [array]: specifies an array of two-byte unencrypted strings that form the file identifier

/XrefStm [integer]: specifies the offset from the beginning of the file to the cross-reference stream in the decoded stream. (Only present in hybrid-reference files)



PDF incremental updates:
We can append new objects to the end of the PDF file without rewriting the entire file. this allows changes to the PDF document to be saved quickly.

PDF documents that have incremental updates still contain the original header, body, cross-reference tbale and trailer. There is an additional body, cross-reference and trialer section that is appended

The additional cross-referece sections will contain only the entries for objects that have been changed, replaced or deleted. Deleted objects will stay in the file, but will be marked with a "f" flag. Each trailer needs to be terminated by the "%%EOF" tag and should contain the /Prev entry, which points to the previous cross-reference section.



PDF data types:

Booleans: trua and false

Numbers: 2 types of numbers in a PDF document: integer and real

An integer consists of one of more digits optionally preceded by a + or - sign

The real value can be represented with one or more digits with and optional sign and leading / trailing or embedded decimal point (a period). (pretty much a float)

Names:
Names in PDF documents are represented by a sequence of ASCII characters in the range 0x21 - 0x7E. the exception are in the characters %, (,),<,>,[,],{,},/ and #.
The length of the name elemetn can only be 127 bytes long
when writing a name, a slash must be used to introduce a name; the slash is not part of the name by the prefix indicating that the following is a sequence of characters representing the name. If we want to use white space of special charaters we must encode it with two-digit hexadecimal notation

string:
strings in a PDF document are represented as a serices of bytes surrounded by a parenthesis or angle brackets, but can be a max of 65535 bytes long. Any character may be represented by ASCII rep, and alternatively with octal or hex reps.

Octal rep requires the character to be written in the form ddd, where ddd is an octal number. Hex rep required the character to be written in the form <dd> where dd is a hex number

e.g:

(string)

<6d79737472696e67>

we can also use special well-known characters when representing a string. Those are: n for newline, r for carriage return, t for horizontal tab, b for backspace, f for form feed, ( for left parenthesis, ) for right parentheesis and for backslash

Dictionaries:
Dictionaries in a PDF documemnt are represented as a table of key/value pairs. The key must be the name object, where as the value can be any object (can also be another dictionary)

The maximum number of entries in a dictionary is 4096. A dictionary can be represented with the entries enclosed in double angle brackets << and >>. An example of a dictionary is presented belog

<< /mykey1 123

    /mykey2 0.123
    /key3 <<
        /key 5 (yeet)
    >>
>>

Streams:
A stream object is represented by a sequence of bytes and may be unlimited in length, which is why images and other big data blocks are usually represented as streams. A stream object is represented by a dictionary object followed by the keywords stream followed by newline and endstream.

e.g.

<<

/Type /Page
    /Length 23 0 R
    /Filter /LZWDecode

>>

stream
...
endstream

All stream objects shall be indirect objects and the stream dictionary shall be an direct object.
The stream dictionary specifies the exact number of bytes of the stream. After the data there should be a newline and the endstream keyword.

Common keywords used in all stream dictionaries are:

length: How many bytes of the PDF are used for stream's data
Type: The type of the PDF object that the dictionary describes.
Filter: the name of the filter that will be applied in processing. Multiple filters cna be specified in order in which they shall be applied
DecodeParms: A dictionary or an array of dictionaries used by the filters specified by filter. This value specifies the parameters that need to be passed to the filters when they are applied
F: Specifies the file containing the stream data.
FFilter: the name of the filter to be applied in processing the data found in the stream's external file.
FDecodeParms: A dictionary of an array of dictionaries used by the filters specified by FFilter.
DL: specifies the number of bytes in the decoded stream. Used if neough diskspace is available to write a stream to file
N: number of indirect objects stored in the stream
First: offset in the decoded streamo f the first compressed object
Extends: Specifies a reference to other object stream, which form an inheritance tree.

Steram data in hte object stream will conain N pairs of integers, where the first integer represents the obejct number and the second integer represents the offset in the decoded stream of the object. The objects in object streams are consecutive and dont need to be stored in increasing order relative to the object number. 
The first entry in the dictionary identiried the first object in the object stream.

Null object
contians the keyword "null"

Indirect objects
'''