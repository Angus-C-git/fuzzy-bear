# Fuzzy Bear

> "The fuzzer nobody wanted but everyone needed..."

![tmp-logo](https://user-images.githubusercontent.com/44337835/122902328-b7a9a880-d391-11eb-96f2-a3c0a019de58.jpeg)


+  A pythonic blackbox (soon to be coverage guided) fuzzer for ELF binaries. 

## Usage

![fuzzybear_usage](https://user-images.githubusercontent.com/44337835/124685226-2ea77b00-df14-11eb-81db-94254b33e30c.png)


`./fuzzer <input> <binary>`

## Fuzzer Structure/Modules

![FuzzerStructureDiagram](https://user-images.githubusercontent.com/44337835/135193498-ffc403d4-db82-464a-ba4b-53b1cc444035.png)


### Harness

Responsible for feeding input to the binary through `stdin` and collecting the response from the binary to return to the aggregator. The harness also implements a **health check** function which is used by the aggregator to attempt to detect hangs and infinite loops in the binary. 

### Strategies

The set of broad tactics and techniques used in attempts to produce crashing inputs for the target binary as well as format specific techniques. Currently supported formats are:

+ TXT
+ CSV
+ JSON
+ XML
+ PDF
+ JPEG

## Aggregator

The aggregator is the component of the fuzzer responsible for bridging the gap between the generators (strategies) and the harness. It functions as the manager for the fuzzing campaign taking in user supplied parameters and orchestrating the calling of generators whose output it then feeds to the harness. It then monitors the response from the harness to deicide if a crash file should be written and the campaign halted, or if the program is hanging / stuck in an infinite loop in which case the strategy should be evolved.

## Libraries

+ [rich](https://github.com/willmcgugan/rich) for GUI
+ [python-magic](#) for input file detection


## Project Structure

*Note: soon to change*

```
.
|
├── fuzzer
├── fuzzybear
│   ├── Aggregator.py
│   ├── Harness.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── strategies
│   │   ├── CSV
│   │   │   └── CSV.py
│   │   ├── ELF
│   │   │   └── ELF.py
│   │   ├── __init__.py
│   │   ├── JPEG
│   │   │   └── JPEG.py
│   │   ├── JSON
│   │   │   └── JSON.py
│   │   ├── PDF
│   │   │   └── PDF.py
│   │   ├── README.md
│   │   ├── Strategy.py
│   │   ├── TXT
│   │   │   └── TXT.py
│   │   └── XML
│   │       └── XML.py
│   └── utility
│       ├── codec.py
│       └── response_codes.py
├── install.sh
├── mk_release.sh
├── README.md
├── requirements.txt
├── test_fuzzybear
├── TESTING.md
├── tests
│   ├── complete
│   │   ├── codecs
│   │   │   ├── csv1.txt
│   │   │   ├── csv2.txt
│   │   │   ├── jpg1.txt
│   │   │   ├── json1.txt
│   │   │   ├── json2.txt
│   │   │   ├── plaintext1.txt
│   │   │   ├── plaintext2.txt
│   │   │   ├── plaintext3.txt
│   │   │   ├── xml1.txt
│   │   │   ├── xml2.txt
│   │   │   └── xml3.txt
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
│   └── components
│       ├── aggregator
│       │   └── badIn.png
│       ├── harness
│       │   ├── bins
│       │   └── ins
│       └── strategies
│           ├── CSV
│           └── JSON
└── WRITEUP.md
```