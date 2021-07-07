# Fuzzy Bear

> "The fuzzer nobody wanted but everyone needed..."

![tmp-logo](https://user-images.githubusercontent.com/44337835/122902328-b7a9a880-d391-11eb-96f2-a3c0a019de58.jpeg)


## Overview

+  A blackbox fuzzer written in 🐍

## Usage

![fuzzybear_usage](https://user-images.githubusercontent.com/44337835/124685226-2ea77b00-df14-11eb-81db-94254b33e30c.png)


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
├── fuzzbear
├── fuzzybear
│   ├── Aggregator.py
│   ├── Harness.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── __pycache__
│   │   ├── Aggregator.cpython-39.pyc
│   │   ├── Harness.cpython-39.pyc
│   │   └── __init__.cpython-39.pyc
│   └── strategies
│       ├── CSV
│       │   └── CSV.py
│       ├── ELF
│       │   └── ELF.py
│       ├── __init__.py
│       ├── JPEG
│       │   └── JPEG.py
│       ├── JSON
│       │   └── JSON.py
│       ├── PDF
│       │   └── PDF.py
│       ├── README.md
│       ├── Strategy.py
│       ├── TXT
│       │   └── TXT.py
│       └── XML
│           └── XML.py
├── install.sh
├── README.md
├── requirements.txt
├── test_fuzzybear
└── tests
    ├── complete
    │   ├── target-bins
    │   │   ├── csv1
    │   │   ├── csv2
    │   │   ├── jpg1
    │   │   ├── json1
    │   │   ├── json2
    │   │   ├── plaintext1
    │   │   ├── plaintext2
    │   │   ├── plaintext3
    │   │   ├── xml1
    │   │   ├── xml2
    │   │   └── xml3
    │   └── target-ins
    │       ├── csv1.txt
    │       ├── csv2.txt
    │       ├── jpg1.txt
    │       ├── json1.txt
    │       ├── json2.txt
    │       ├── plaintext1.txt
    │       ├── plaintext2.txt
    │       ├── plaintext3.txt
    │       ├── xml1.txt
    │       ├── xml2.txt
    │       └── xml3.txt
    └── components
        ├── harness
        │   ├── bins
        │   │   └── harness_mvp
        │   └── ins
        │       └── big.txt
        └── strategies
```