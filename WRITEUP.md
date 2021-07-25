# Fuzzy Bear

## Design Overview

The fuzzer is designed with three primary components which work together to provide the desired functionality.

+ Harness
+ Strategies
+ Aggregator


Each component and indeed the fuzzer as a whole is designed with a strong focus on modular design. For strategies to be particularly useful they need to be able to be applied with great flexibility. 


```
fuzzer [Entry point]
|  
|  Harness <--> Binary
|   ^  |
V   |  V
Aggregator --> Strategies ---
    ^                       |
    |_______________________|

```

## Harness

Second only to the generators themselves is the harness. The harness is the component of the fuzzer which really makes it useful. It is responsible for feeding input to the binary through `stdin` and collecting the response from the binary to return to the aggregator. The harness also implements a **health check** function which aims to detect hangs and infinite loops in the binary. 


## Strategies

### Common

There exist a number of mutations which are agnostic to the file format being utilized for mutation or which can and should be used within format specific mutations. For this reason we implement a base class `Strategies` which is extended by all other strategies the fuzzer currently supports. This has several major benefits:

    + It reduces code reuse 
    + Makes extending the functionality of the fuzzer `trivial`
      + Add new broad strategies with class methods to the base class
      + Or add support for more file formats without losing the ability to utilise existing code
    + It makes it easy to focus on writing format specific generators

### CSV

CSV strategies focus on generating oddball data to place into *sensible* places within a CSV file. Currently this mainly revolves around loading the input file into memory and then mutating that data structures fields using tactics implemented in the base class. The CSV strategy also implements `add_entries` which focuses on creating a large valid csv structure with many rows/columns.

### JSON

Similarly to the CSV based strategies the JSON generator attempts to create sane json structures with unnatural and unexpected fields which may cause a parser to break and  memory corruption to occur. A key strategy that the
JSON mutator implements is the ability to select a random field to alter with another tactics data. The JSON generator also implements a function to add a large number of extra fields in the hopes of causing overflow based crashes to occur.


## Aggregator

The aggregator is the component of the fuzzer responsible for bridging the gap between the generators (strategies) and the harness. It functions as the manager for the fuzzing campaign taking in user supplied parameters and orchestrating the calling of generators whose output it then feeds to the harness. It then monitors the response from the harness to deicide if a crash file should be written and the campaign halted, or if the program is hanging / stuck in an infinite loop in which case the strategy should be evolved.

