from argparse import ONE_OR_MORE
from fuzzybear.strategies.JPEG.JPEG import JPEG
from .. import Strategy


#creating the start of the pdf document
def create_header():
    return '%PDF-1.4\n'


def create_img_and_text_resouce(obj_num, img_num, font_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/XObject << /I1' + str(img_num) + ' 0 R >>\n'
    stream += '/Font << /F1 ' + str(font_num) + ' 0 R >>\n'
    stream += '/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]'
    stream += '>>\n'
    stream += 'endobj\n'
    return stream


def create_img_resouce_obj(obj_num, img_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/XObject << ' + str(img_num) + ' 0 R >>\n'
    stream += '/ProcSet [/PDF /ImageB /ImageC /ImageI]'
    stream += '>>\n'
    stream += 'endobj\n'
    return stream


def create_resource_obj(obj_num, font_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Font << /F1 ' + str(font_num) + ' 0 R >>\n'
    stream += '/ProcSet [/PDF /Text]\n'
    stream += '>>\n'
    stream += 'endobj\n'
    return stream


def type_obj(obj_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Type /Font\n'
    stream += '/Subtype /Type1\n'
    stream += '/BaseFont /Helvetica\n'
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
    return stream


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
    stream += 'endobj\n'
    return stream


def create_info_obj(obj_num):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    stream += '/Type /Info\n'
    stream += '/Producer (FuzzyBear fuzzer 11.1.1.1.1.11)\n'
    stream += '>>\n'
    stream += 'endobj\n'
    return stream


def create_img_stream(obj_num, data, type_encoding):
    stream = bytes(str(obj_num),'utf-8') + b' 0 obj\n<<\n'
    stream += b'/Type /XObject\n'
    stream += b'/Subtype /Image\n'
    stream += b'/Width  3510\n'
    stream += b'/Height 2491\n'
    stream += b'/ColorSpace /DeviceRGB\n'
    stream += b'BitsPerComponent 8\n'
    stream += b'/Filter ' + bytes(type_encoding,'utf-8') + b'\n'
    stream += b'/Length ' + bytes(str(len(data)),'utf-8') + b'\n' 
    stream += b'>>\n'
    stream += b'stream\n'
    stream += data
    stream += b'\nendstream\n'
    stream += b'endobj\n'
    return stream


#assuming data is a string
def create_stream(obj_num ,data, encoding, length):
    stream = str(obj_num) + ' 0 obj\n<<\n'
    if encoding:
        stream += '/Filter /FlateDecode\n'
    stream += '/Length ' + str(length) + '\n'
    stream += '>>\n'
    stream += 'stream\n'
    stream += str(data)
    stream += '\nendstream\n'
    stream += 'endobj\n'
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
        trailer += '/Prev '+ str(prev_xref)
    trailer += '>>\n'
    trailer += 'startxref\n'
    trailer += str(lenth_to_xref) + '\n'
    trailer += '%%EOF'
    return trailer


################################ Document Creation ################################
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
    data = "BT /F1 12 Tf 100 700 Td (Hello World)Tj ET"
    pdf_document += create_stream(obj_num ,data, False, len(data))
    obj_num += 1
    obj_locations.append(len(pdf_document))
    data = "BT /F1 24 Tf 200 700 Td (Nice to meet you)Tj ET"
    pdf_document += create_stream(obj_num ,data, False, len(data))
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


def create_large_page_document(num):
    obj_num = 1
    obj_locations = []
    pdf_document = create_header()
    obj_locations.append(len(pdf_document))
    pdf_document += create_info_obj(obj_num)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += type_obj(obj_num)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    resouce_obj = obj_num
    pdf_document += create_resource_obj(obj_num, obj_num-1)
    obj_num += 1
    
    parent_obj = obj_num + (num*2)
    page_obj_nums = []
    for i in range(num):
        obj_locations.append(len(pdf_document))
        data = "BT /F1 12 Tf 100 700 Td (Hello Adam, I hope you enjoy a very large PDF Document... I have much pain form PDFs)Tj ET"
        pdf_document += create_stream(obj_num ,data, False, len(data))
        obj_num += 1
        obj_locations.append(len(pdf_document))
        page_obj_nums.append(obj_num)
        pdf_document += page_leaf_obj(obj_num , parent_obj, resouce_obj, obj_num-1)
        obj_num += 1

    obj_locations.append(len(pdf_document))
    pdf_document += page_node_obj(obj_num, page_obj_nums)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += doc_catalog(obj_num,obj_num-1)
    obj_num += 1
    length_to_xref = len(pdf_document)
    pdf_document += create_xref(obj_locations)
    pdf_document += create_trailer(obj_num-1, obj_num, 2, length_to_xref, None)
    return pdf_document


def create_bee_movie_page(data):
    obj_num = 1
    obj_locations = []
    pdf_document = create_header()
    obj_locations.append(len(pdf_document))
    pdf_document += create_info_obj(obj_num)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += type_obj(obj_num)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    resouce_obj = obj_num
    pdf_document += create_resource_obj(obj_num, obj_num-1)
    obj_num += 1
    parent_obj = obj_num + (len(data)*2)
    page_obj_nums = []
    for i in data:
        obj_locations.append(len(pdf_document))
        val = "BT /F1 23 Tf 100 700 Td 1 Tr 2 w 0.25 Tc 2.5 Tw("+i+")Tj ET"
        pdf_document += create_stream(obj_num ,val, False, len(val))
        obj_num += 1
        obj_locations.append(len(pdf_document))
        page_obj_nums.append(obj_num)
        pdf_document += page_leaf_obj(obj_num , parent_obj, resouce_obj, obj_num-1)
        obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += page_node_obj(obj_num, page_obj_nums)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += doc_catalog(obj_num,obj_num-1)
    obj_num += 1
    length_to_xref = len(pdf_document)
    pdf_document += create_xref(obj_locations)
    pdf_document += create_trailer(obj_num-1, obj_num, 2, length_to_xref, None)
    return pdf_document


def create_document_image(data):
    obj_num = 1
    obj_locations = []
    pdf_document = bytes(create_header(),'utf-8')
    obj_locations.append(len(pdf_document))
    pdf_document += bytes(create_info_obj(obj_num),'utf-8')
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += create_img_stream(obj_num, data,'/DCTDecode')
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += bytes(create_img_resouce_obj(obj_num, obj_num-1),'utf-8')
    obj_num += 1
    obj_locations.append(len(pdf_document))
    val = 'q\n 1 0 0 1 100 200 cm\n 0 0 0 0 0 0 cm \n 150 0 0 80 0 0 cm\n /I1 Do\n Q'
    pdf_document += bytes(create_stream(obj_num, val , False, len(val)),'utf-8')
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += bytes(page_leaf_obj(obj_num, obj_num+1, obj_num-2, obj_num-1),'utf-8')
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += bytes(page_node_obj(obj_num, [(obj_num-1)]),'utf-8')
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += bytes(doc_catalog(obj_num,obj_num-1),'utf-8')
    obj_num += 1
    length_to_xref = len(pdf_document)
    pdf_document += bytes(create_xref(obj_locations),'utf-8')
    pdf_document += bytes(create_trailer(obj_num-1, obj_num, 2, length_to_xref, None),'utf-8')
    return pdf_document


def create_invalid(input, overflow_len):
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
    pdf_document += page_node_obj(obj_num, [4])
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += page_leaf_obj(obj_num , 3, 6, 5)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    data = "BT /F1 12 Tf 100 700 Td (I love in valid input "+ input +")Tj ET"
    pdf_document += create_stream(obj_num ,data, False, len(data)-overflow_len)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += create_resource_obj(obj_num, 7)
    obj_num += 1
    obj_locations.append(len(pdf_document))
    pdf_document += type_obj(obj_num)

    length_to_xref = len(pdf_document)
    pdf_document += create_xref(obj_locations)
    pdf_document += create_trailer(1, obj_num, 2, length_to_xref, None)
    return pdf_document
    

class PDF(Strategy.Strategy):

    def __init__(self, sample_input):
        super()
        self.sample_input = sample_input
        self.parse_pdf()


    def parse_pdf(self):
        pass


    def run(self):
        yield(bytes(create_pdf_basic(),'utf-8'))
        yield(bytes(create_large_page_document(10000),'utf-8'))

        with open('fuzzybear/strategies/PDF/bee_mov.txt') as f:
            lines = f.readlines()
            yield(bytes(create_bee_movie_page(lines),'utf-8'))

        jpg_gen  = JPEG('fuzzybear/strategies/PDF/bee.jpg')
        for i in jpg_gen.run():
            yield(create_document_image(i))

        for i in self.chonk():
            yield(bytes(create_invalid(i, len(i)),'utf-8'))
        
        for i in self.format_strings():
            yield(bytes(create_invalid(i, 0),'utf-8'))

        for i in self.polyglots():
            yield(bytes(create_invalid(i, 0),'utf-8'))

        



''' Dev Notes

+ See README in this directory for details

'''