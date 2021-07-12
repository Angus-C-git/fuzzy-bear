# Testing Fuzzy Bear

## Overview

+ Testing is setup and awful :) 
  + Someone can fix it if they so desire <3
+ Idk how to use pytest


## Setting Up A Test

1. Open `test_fuzzybear`
2. Add a new command line argument for your test

```python
# ... #

parser.add_argument('-P', '--your-test',
                    dest = 'test-name',
                    action='store_true',
                    help = 'what is your test for'
                    )


## Add command line args for your test ^
```

3. Define a function for your test

```python
########################## :: [DEFINE TESTS] :: ##########################

# test desc
def test_name():
    TEST_DIR = './tests/'
    TEST_FILE = f'{TEST_DIR}/target-bins/<binary>'
    TEST_SAMPLE = f'{TEST_DIR}/target-ins/<codec>'

    print(f"""
        [>>] Running test against {TEST_FILE.split('/')[-1]} with {TEST_SAMPLE.split('/')[-1]}
    """)

    # >-> test body <-<

```

4. Import any required files

```python

## <name> Test ##
from fuzzybear.<subdir> import <file/class>

## ADD TEST IMPORT ## ^

```

5. Use it in your test body like

```python
# >-> test body <-<
csv_worker = CSV.CSV(TEST_FILE)
```


## Running A Test

`./test_fuzzybear -h`

```


          ____    _____ _____ ____ _____   _____ _   _ ____________   __
          \ \ \  |_   _| ____/ ___|_   _| |  ___| | | |__  /__  /\ \ / /
           \ \ \   | | |  _| \___ \ | |   | |_  | | | | / /  / /  \ V / 
           / / /   | | | |___ ___) || |   |  _| | |_| |/ /_ / /_   | |  
          /_/_/    |_| |_____|____/ |_|   |_|    \___//____/____|  |_|  
                                                              
          ____  _____    _    ____  
         | __ )| ____|  / \  |  _ \ 
         |  _ \|  _|   / _ \ | |_) |
         | |_) | |___ / ___ \|  _ < 
         |____/|_____/_/   \_\_| \_                           
    
usage: test_fuzzybear [-h] [-H] [-CSV]

optional arguments:
  -h, --help         show this help message and exit
  -H, --harness      test harness
  -CSV, --CSV-codec  test the csv codec binaries

```

+ To run the `CSV` test for example
  + `./test_fuzzybear -CSV`