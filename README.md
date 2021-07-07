# Fuzzy Bear

> "The fuzzer nobody wanted but everyone needed..."

![tmp-logo](https://user-images.githubusercontent.com/44337835/122902328-b7a9a880-d391-11eb-96f2-a3c0a019de58.jpeg)


## Overview

+  A blackbox fuzzer written in 🐍

## Usage

![fuzzybear_usage](https://user-images.githubusercontent.com/44337835/124685031-cb1d4d80-df13-11eb-9c52-b8b5791f15d9.png)

`./fuzzbear <input> <binary>`

## Components/Modules

![Diagram]()

### Harness

+ Stuff and things

+ Stuff and things

### Mutator

+ Stuff and things

### Generator

+ Stuff and things

## Libraries

+ [enlighten](https://pypi.org/project/enlighten/)


## Structure

+ Project structure is based off various best practice docs
    + Mainly [Structuring](https://docs.python-guide.org/writing/structure/)

```
.
├── docs
├── fuzzybear
│   ├── Aggregator.py
│   ├── Harness.py
│   ├── __init__.py
│   ├── __main__.py
│   └── strategies
│       ├── CSV
│       │   └── CSV.py
│       ├── ELF
│       ├── __init__.py
│       ├── JPEG
│       ├── JSON
│       │   └── JSON.py
│       ├── opt
│       │   ├── HTML
│       │   │   └── HTML.py
│       │   ├── MD
│       │   │   └── MD.py
│       │   ├── README.md
│       │   ├── templates
│       │   │   ├── handlebars.py
│       │   │   ├── jinja.py
│       │   │   ├── mako.py
│       │   │   ├── README.md
│       │   │   ├── smarty.py
│       │   │   ├── tornado.py
│       │   │   └── twig.py
│       │   └── YAML
│       │       └── YAML.py
│       ├── PDF
│       ├── README.md
│       ├── Strategy.py
│       ├── TXT
│       │   └── TXT.py
│       └── XML
│           └── XML.py
├── install.sh
├── README.md
├── requirements.txt
└── tests
    ├── target-bins
    │   ├── csv1
    │   ├── csv2
    │   ├── jpg1
    │   ├── json1
    │   ├── json2
    │   ├── plaintext1
    │   ├── plaintext2
    │   ├── plaintext3
    │   ├── xml1
    │   ├── xml2
    │   └── xml3
    ├── target-ins
    │   ├── csv1.txt
    │   ├── csv2.txt
    │   ├── jpg1.txt
    │   ├── json1.txt
    │   ├── json2.txt
    │   ├── plaintext1.txt
    │   ├── plaintext2.txt
    │   ├── plaintext3.txt
    │   ├── xml1.txt
    │   ├── xml2.txt
    │   └── xml3.txt
    └── test_fuzzybear.py
```