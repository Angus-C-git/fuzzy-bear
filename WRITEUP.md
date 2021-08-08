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


## Static Path Analysis

The fuzzer includes functionallity to parse a binary and extract static paths, similarly to the disassembler BinaryNinja. We use the capstone library in order to disassemble the bytes of the 
binary into instructions. The instructions are then parsed in 2 ways:
1. By looking for jump instructions. The analysis tools keep track of the most recent point in the binary it began searching from (startPoint), and when an unseen jump instruction is found, it stores a 'jump block' which is denoted by startPoint and the address of the instruction that contains the jump. 
This is done recursively untill all jump blocks in the binary are found. From this we are able to build a data structure that represents all blocks in the code that end in a jump.
2. By looking for function calls. When the analysis tool finds a call instruction it stores both the address of the call instruction and the address of the function being called, into a data structure.
Once both of these data structures are built. 

We use pwntools in order to resolve the function names in the function call data structure. We also contextualise each jump block and denote in which function that jump block resides. 

Furthermore, this functionallity works even with PIE and ASLR enabled. Since we have the PID of the process running the binary, we are able to inspect /proc/{pid}/maps before fuzzing begins and find the base address of the binary and libc. 

### Potential Improvements
- The jump block data structure that we build is not exactly like the static path analysis performed by BinaryNinja, it could be made more comprehensive. We do not capture blocks that end in a non returning function call like exit. We also are not able to capture blocks that are defined by looping mechanics.
- We did not implement a infinite loop detection algorithm but I think the existing data structures support it. Our idea is to have some sort of a triggering mechanism when we are suspect that a loop is occuring, and then build a graph which grows when an existing jump block is visited. After a certain amount of iterations we start comparing the previous size of the graph to the new size of the graph. If it doesn't grow then we can assume the same places in the code are being repeatively jumped to, and the binary is stuck in an infinite loop.


## Strategies

### Common / Base Strategies

There exist a number of mutations which are agnostic to the file format being utilized for mutation or which can and should be used within format specific mutations. For this reason we implement a base class `Strategies` which is extended by all other strategies the fuzzer currently supports. This has several major benefits:

  + It reduces code reuse 
  + Makes extending the functionality of the fuzzer `trivial`
    + Add new broad strategies with class methods to the base class
    + Or add support for more file formats without losing the ability to utilise existing code
  + It makes it easy to focus on writing format specific generators

We implement the following universal strategies:

+ Chonk / Overflow - generates increasingly large string patterns 
+ Negate - Turns an integer to its negative counterpart or appends a `-` symbol to the front of supplied data
+ Format Strings - Generates format string payloads, supports width modifier
+ System Words - Generates unix like system commands 
+ System Paths - Generates unix like system paths
+ Polyglots - Generates polyglots of various bad strings, web, sql, XXE, newlines
+ Random Integers - Various random integer generators
+ Max Constants - Generates type threshold values
+ XOR
+ Bitflip
+ Byteflip


### CSV

CSV strategies focus on generating oddball data to place into *sensible* places within a CSV file. Currently this mainly revolves around loading the input file into memory and then mutating that data structures fields using tactics implemented in the base class. The CSV strategy also implements `add_entries` which focuses on creating a large valid csv structure with many rows/columns. Another key tactic that CSV implements is `negate` which makes the entries in the CSV negative.

### JSON

Similarly to the CSV based strategies the JSON generator attempts to create sane json structures with unnatural and unexpected fields which may cause a parser to break and  memory corruption to occur. A key strategy that the
JSON mutator implements is the ability to select a random field to alter with another tactics data. The JSON generator also implements a function to add a large number of extra fields in the hopes of causing overflow based crashes to occur.

### JPEG

While JPEG fuzzing was unsucessful, we implemented strategies by attempting to flip bits and replace bits with bits known to break jpeg files, such as 0x00 and 0xFF, and other large numbers. Unfortunately, this caused the JPEG file to be read as invalid. Afterwards, we attempted to also only fuzz bits which were a certain "distance" away from the markers (0xFF), but still the file was invalid 20% of the time. Unsure of the cause of this.

### XML
The XML generator modifies valid XML files by appending/altering attributes, inserting sub elements and overwriting elements/attributes with data from the strategy generator. This generator also creates files that include other files such as dev/random with the intention of creating buffer overflows in the target program. 

### PDF

The PDF generator creates large pdf documents to test memory management of a PDF parser and invalid pdf documents, testing for memory corruption vulnerabilities where the length field doesn't match up with the stream object size. The PDF generator inserts stream objects with data from the strategy generator, which can include javascript to format string vulnerabilities. The intention of the PDF generator is to test to the extremities of PDF parsers, creating documents which aren't seen usually in the real world and thus are more likely to break parsers. 

## Aggregator

The aggregator is the component of the fuzzer responsible for bridging the gap between the generators (strategies) and the harness. It functions as the manager for the fuzzing campaign taking in user supplied parameters and orchestrating the calling of generators whose output it then feeds to the harness. It then monitors the response from the harness to deicide if a crash file should be written and the campaign halted, or if the program is hanging / stuck in an infinite loop in which case the strategy should be evolved.




