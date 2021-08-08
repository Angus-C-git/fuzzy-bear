'''
This module attempts to determine the format of the 
supplied sample input.
'''
import magic, csv, json, xml, string

def detect(file):
    # print(f'   [DEBUG] Attempting to resolve codec for {file}')

    # PRIORITISING FILENAMES FIRST
    filename = file.split('/')[-1]
    if filename.startswith('jpg') or filename.endswith('.jpg') or filename.startswith('jpeg') or filename.endswith('.jpeg'):
        return "jpeg"
    elif filename.startswith('csv') or filename.endswith('.csv'):
        return "csv"
    elif filename.startswith('json') or filename.endswith('.json'):
        return "json"
    elif filename.startswith('xml') or filename.endswith('.xml'):
        return "xml"
    elif filename.startswith('pdf') or filename.endswith('.pdf'):
        return "pdf"
    elif filename.startswith('txt') or filename.endswith('.txt'):
        return "plain"

    # TRYING FOR JPG
    mime_type = magic.from_file(file, mime=True)
    result = mime_type.split('/')[-1]
    if result == "jpeg":
        return result
    
    # TRYING FOR JSON
    try:
        with open(file) as jsonfile:
            data = json.loads(jsonfile.read())
            return "json"
    except:
        pass

    # TRYING FOR XML
    try:
        data = xml.dom.minidom.parse(file)
        return "xml"
    except:
        pass

    # TRYING CSV
    try:
        with open(file, newline='') as csvfile:
            start = csvfile.read(4096)
            # isprintable does not allow newlines, printable does not allow umlauts...
            if not all([c in string.printable or c.isprintable() for c in start]):
                pass
            else:
                dialect = csv.Sniffer().sniff(start)
                return "csv"
    except csv.Error:
        pass

    return "plain"
    #mime_type = magic.from_file(file, mime=True)
    # print(f'   [DEBUG] Type guess is {mime_type}')
    #result = mime_type.split('/')[-1]

'''devnotes

TODO

    - [ ] This code will not survive conditions where the
          input file resembles a supported codec but does
          not contain the associated magic number for that
          codec
    - [ ] This will require the implementation of a weighted
          passing algorithm which attempts to determine what
          the best supported format choice is

'''

if __name__ == '__main__':
    print(detect('tests/complete/codecs/csv1.txt'))
    print(detect('tests/complete/codecs/csv2.txt'))
    print(detect('tests/complete/codecs/jpg1.txt'))
    print(detect('tests/complete/codecs/json1.txt'))
    print(detect('tests/complete/codecs/json2.txt'))
    print(detect('tests/complete/codecs/plaintext1.txt'))
    print(detect('tests/complete/codecs/plaintext2.txt'))
    print(detect('tests/complete/codecs/plaintext3.txt'))
    print(detect('tests/complete/codecs/xml1.txt'))
    print(detect('tests/complete/codecs/xml2.txt'))
    print(detect('tests/complete/codecs/xml3.txt'))

    print(detect('new.jpeg'))
