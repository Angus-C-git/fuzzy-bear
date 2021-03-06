# PDF Generator / Strategy

The PDF generator creates large pdf documents to test memory management of a PDF parser and invalid pdf documents, testing for memory corruption vulnerabilities where the length field doesn't match up with the stream object size. The PDF generator inserts stream objects with data from the strategy generator, which can include javascript to format string vulnerabilities. The intention of the PDF generator is to test to the extremities of PDF parsers, creating documents which aren't seen usually in the real world and thus are more likely to break parsers. 

*Interestingly: Some PDFs fuzzed by the generator proved to crash firefox's PDF reader on `ubuntu 21.04`*

## Key Strategies

### Bee Movie

Dumps the entire script of the bee movie but each line of the script is on a new page. Hopes to cause memory corruption by being too large and sparse to parse.

### Malicious Image

Uses the JPEG generator to generate fuzzed JPEG images to include in the fuzzed PDF in the hopes of breaking parsers which to not do edge case checking for malformed images included in PDFs.

### Polyglots

Since PDF documents may legally contain JavaScript under the spec as well as other entities like XML the polyglot tactic is employed in the hopes of replacing sections in the PDF which may attempt to unsafely parsed, rendered or used by the program causing memory corruption or other unintended behavior.  


## The PDF File Format

The pdf file structure is separated into 4 main parts: 

+ The header, 
+ The body 
+ The 'xref' Table
+ The Trailer

**Key Reading**
+ [Acrobat SDK](https://opensource.adobe.com/dc-acrobat-sdk-docs/)
+ [PDF File Format Basics](https://resources.infosecinstitute.com/topic/pdf-file-format-basic-structure/ )

> READ THIS!!!!!!!!!! PDF documents are really complicated... they're like an entire coding language


PDF allow you so store text, images, multimedia elements, they can be password protected, execute javascript etc.

### The header

The first line of a PDF specifies the version number of the used PDF spec this version number is hex encoded

+ e.g: 
    + `%PDF-1.3.%...`
+ hex encoded: 
    + `2550 4446 2d31 2e33 0a25 c4e5 f2e5 eba7`

The `%` symbol in pdf is actually a commend so the specification is commented out but it needs to be there fore the PDF reader.

The following characters are non-printable ASCII text (non-printable characters) which are usually there to tell some of the software products that the file contains binary data and shouldn't be treated as 7-bit ASCII text.

The version numbers go from 0-7 in the form `1.N`.

### The Body

The Body of the PDF document contain the objects that are typically included these can be:

+ text streams, images and other media elements.

The body section is used to hold all the document's data being shown to the user.

### xref table:

This is the cross reference table, which contains all the references to all the objects in the document. It allows random access to objects in the file so you don't have to read the whole PDF document to locate the particular object.
Each object is represented by one entry in the cross reference table, which is always 20 bytes long.

An example cross reference table:

```
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
```

**Note the 4 sections:**

the numbers above `(0 1, 3 1, 21 4, 36 1)` are used to determine the number of objects in each section  and the object numbers the first number refers to the object number the second number refers to the number of objects in the current subsection.

The first 10 bytes are the object's offset from the start of the pdf document
the bytes that follow the space specifies the object's generation number.  After that, the next space separator, followed by a letter 'f' or 'n' indicates whether the object is free or in use.

The first object has an ID - and always contains one entry with generation number 65535 which is at the head of the list of free objects.

The last object in the cross-reference table used the generation number 0.

All objects are marked with either an "f" or "n" flag meaning that the object may still be present in a file, but is marked as free, so it shouldn't be used. These objects contain a reference to the next free object and the generation number to be used if the object becomes valid again. The flag "n" is used to represent valid and used objects that contain the offset from the beginning of the file and generation number of the object

The generation number of the object is incremented when the object is freed, so if the object becomes valid again, the generation number of object 23 is 1, so if it becomes valid again, the generation number will still be 1, but if it's removed again, the generation number would increase to 2.

Multiple subsections are usually present in PDF documents that have been incrementally updated, otherwise only one subsection starting with the number 0 should be present


### Trailer

The PDF trailer specifies how the application reading the PDF document should find the xref table and other special objects. All PDF readers should starting reading a PDF from the end of the file.

```
trailer
&amp;amp;lt;&amp;amp;lt;
/Size 22
/Root 2 0 R
/Info 1 0 R
&amp;amp;gt;&amp;amp;gt;
startxref
24212
%%EOF
```

The line contains the end of the pdf document `%%EOF`

Before the end there is a tag `startxref` which specifies the offset from the beginning of the file to the cross-reference table.

Before that is a trailer string the specifies the start of the Trailer section.
The contents of the trailer sections are embedded with the << and >> characters (this is a dictionary that accepts key-value pairs).

There are several keys in the trailer section these being:

`/Size` [integer]: specifies the number of entries in the cross-reference table (counting the objects in the updated sections as well). The used number shouldn't be an indirect reference

`/Prev` [integer]: Specifies the offset from the beginning of the file to the previous cross-reference section, which is used if there are multiple cross-reference sections. The number should be a cross-reference.

`/Root` [dictionary]: specifies the reference object for the document catalog object. which is a special object that contains various pointers to different kinds of other special objects

`/Encrypt` [dictionary]: specifies the documents encryption

`/Info` [dictionary]: specifies the reference object for the document's information dictionary

`/ID` [array]: specifies an array of two-byte unencrypted strings that form the file identifier

`/XrefStm` [integer]: specifies the offset from the beginning of the file to the cross-reference stream in the decoded stream. (Only present in hybrid-reference files)



## PDF incremental updates

We can append new objects to the end of the PDF file without rewriting the entire file. this allows changes to the PDF document to be saved quickly.

PDF documents that have incremental updates still contain the original header, body, cross-reference table and trailer. There is an additional body, cross-reference and trailer section that is appended

The additional cross-reference sections will contain only the entries for objects that have been changed, replaced or deleted. Deleted objects will stay in the file, but will be marked with a "f" flag. Each trailer needs to be terminated by the "%%EOF" tag and should contain the `/Prev` entry, which points to the previous cross-reference section.

## PDF data types

**Booleans:** true and false

**Numbers:** 

Two types of numbers in a PDF document: integer and real

An integer consists of one of more digits optionally preceded by a + or - sign

The real value can be represented with one or more digits with and optional sign and leading / trailing or embedded decimal point (a period). (pretty much a float)

**Names:**

Names in PDF documents are represented by a sequence of ASCII characters in the range 0x21 - 0x7E. the exception are in the characters `%, (,),<,>,[,],{,},` and `#`.

The length of the name element can only be 127 bytes long
when writing a name, a slash must be used to introduce a name; the slash is not part of the name by the prefix indicating that the following is a sequence of characters representing the name. If we want to use white space of special characters we must encode it with two-digit hexadecimal notation

**string:**

Strings in a PDF document are represented as a serices of bytes surrounded by a parenthesis or angle brackets, but can be a max of 65535 bytes long. Any character may be represented by ASCII rep, and alternatively with octal or hex reps.

Octal rep requires the character to be written in the form ddd, where ddd is an octal number. Hex rep required the character to be written in the form <dd> where dd is a hex number

e.g:

+ (string)

+ `<6d79737472696e67>`

We can also use special well-known characters when representing a string. Those are: n for newline, r for carriage return, t for horizontal tab, b for backspace, f for form feed, ( for left parenthesis, ) for right parenthesis and for backslash

**Dictionaries:**

Dictionaries in a PDF document are represented as a table of key/value pairs. The key must be the name object, where as the value can be any object (can also be another dictionary)

The maximum number of entries in a dictionary is 4096. A dictionary can be represented with the entries enclosed in double angle brackets << and >>. An example of a dictionary is presented below

```
<< /mykey1 123

    /mykey2 0.123
    /key3 <<
        /key 5 (yeet)
    >>
>>
```

**Streams:**

A stream object is represented by a sequence of bytes and may be unlimited in length, which is why images and other big data blocks are usually represented as streams. A stream object is represented by a dictionary object followed by the keywords stream followed by newline and endstream.

```
<<

/Type /Page
    /Length 23 0 R
    /Filter /LZWDecode

>>

stream
...
endstream
```

All stream objects shall be indirect objects and the stream dictionary shall be an direct object.
The stream dictionary specifies the exact number of bytes of the stream. After the data there should be a newline and the endstream keyword.

Common keywords used in all stream dictionaries are:

+ Length: How many bytes of the PDF are used for stream's data
+ Type: The type of the PDF object that the dictionary describes.
+ Filter: the name of the filter that will be applied in processing. Multiple filters cna be specified in order in which they shall be applied
+ DecodeParms: A dictionary or an array of dictionaries used by the filters specified by filter. This value specifies the parameters that need to be passed to the filters when they are applied

+ F: Specifies the file containing the stream data.
+ FFilter: the name of the filter to be applied in processing the data found in the stream's external file.
+ FDecodeParms: A dictionary of an array of dictionaries used by the filters specified by FFilter.
+ DL: specifies the number of bytes in the decoded stream. Used if enough disk space is available to write a stream to file
+ N: number of indirect objects stored in the stream
+ First: offset in the decoded stream of the first compressed object
+ Extends: Specifies a reference to other object stream, which form an inheritance tree.
+ Null object: contains the keyword "null"

Stream data in hte object stream will contain N pairs of integers, where the first integer represents the object number and the second integer represents the offset in the decoded stream of the object. The objects in object streams are consecutive and don't need to be stored in increasing order relative to the object number. The first entry in the dictionary identifies the first object in the object stream.



