<p align="center">
  <a href="#" target="blank"><img src="https://i.imgur.com/TJU6XXK.gif" alt="Fuzzy Bear Logo" /></a>
</p>

<p align="center">
    A pythonic blackbox (soon to be) coverage guided fuzzer. 
</p>

<p align="center">
  <!-- badges -->
</p>

<hr style='width: 90%;'/>
<br />

## Contents

### ‣ [Install](#install)

### ‣ [Usage](#usage)

### ‣ [Fuzzer Structure/Modules](#fuzzer-structuremodules)

### ‣ [Libraries](#libraries)

### ‣ [Project Structure](#project-structure)

<br/>
<br/>
<p align="center">
    <img 
        src="https://i.imgur.com/pd4W61D.png" 
        alt="Fuzzy Bear Demo"
        width='80%' 
    />
</p>

## Install

### From Release

1. Download the latest build from releases
2. `unzip <release>.zip`
3. `cd fuzzy-bear/ && ./install.sh`
4. `./fuzzer -h`

### From Git

1. `git clone https://github.com/Angus-C-git/fuzzy-bear.git`
2. `cd fuzzy-bear/ && ./install.sh`
3. `./fuzzer -h`

## Usage

`./fuzzer <binary> <input>`

The following are (specifically) supported input corpus':

-   TXT
-   CSV
-   JSON
-   XML
-   PDF (no ui events)
-   JPEG (no ui events)

## Design Overview

The fuzzer is designed with three primary components which work together to provide the desired functionality.

-   Harness
-   Strategies
-   Aggregator

Each component and indeed the fuzzer as a whole is designed with a strong focus on modular design. For strategies to be particularly useful they need to be able to be applied with great flexibility.

_The goal is to make everything plug and play._

```
fuzzer [Entry point]
|
|  Harness <--> Binary [Fuzz Target]
|   ^  |
V   |  V
Aggregator --> Strategies ---
    ^                       |
    |_______________________|
```

## Fuzzer Structure/Modules

![FuzzerStructureDiagram](https://user-images.githubusercontent.com/44337835/135193498-ffc403d4-db82-464a-ba4b-53b1cc444035.png)

### Harness

Responsible for feeding input to the binary through `stdin` and collecting the response from the binary to return to the aggregator. The harness also implements a **health check** function which is used by the aggregator to attempt to detect hangs and infinite loops in the binary, although this feature is in its early stages.

### Strategies

The set of broad tactics and techniques used in attempts to produce crashing inputs for the target binary as well as format specific techniques. Currently supported formats are:

-   TXT
-   CSV
-   JSON
-   XML
-   PDF
-   JPEG

In a future release the generators for strategies will be combined with a more generalised mutation engine which will be agnostic to the input file format. Right now the generators are in their
early stages and serve more as a POC to highlight the direction of the project. Although many
of the techniques employed form a good foundation for a more advanced coverage guided mutation
based fuzzing. See [project direction](#project-direction) for more details.

#### Common

There exist a number of mutation strategies which are agnostic to the file format being targeted or which can, and should be used, within all format specific mutations. For this reason we implement a base class `Strategies` which is extended by all other strategies the fuzzer currently supports. This has several major benefits:

-   It reduces code reuse
-   Makes extending the functionality of the fuzzer `trivial`
    -   Add new broad strategies with class methods to the base class
    -   Or add support for more file formats without losing the ability to utilise existing code

_TLDR - It makes it easy to focus on writing format specific generators._

#### TXT Generator

The plaintext input generator focuses on producing a mixture of large magnitude inputs and abnormal characters. Currently plaintext specific strategies employed are:

-   Random bit flips
-   Control character injection
-   Whitespace injection
-   Carriage return and newline injection

#### CSV Generator

The CSV generator focuses on producing semi-sensible CSV format inputs with fields designed to cause undefined and unexpected behaviour after the initial parse. Current CSV specific strategies are:

-   Add entries
-   Negate random entries
-   Bit fip random fields

#### JSON Generator

Currently the JSON generator is rather primitive with most specific strategies unable to cope with high levels of input corpus nesting. Current specific strategies employed regardless are:

-   Large numbers of extra fields
-   Large field size (overflow fields)
-   Field negation
-   Format string injection
-   System path injection
-   polyglot injection
-   Max constant injection
-   Random byte flips

#### XML Generator

The XML generator modifies valid XML files by appending elements, inserting sub elements and overwriting elements/attributes with data from the strategy generator. This generator also creates files that include other files such as dev/random with the intention of creating buffer overflows in the target program.

#### PDF Generator

The PDF generator creates large pdf documents to test memory management of a PDF parser and invalid pdf documents, testing for memory corruption vulnerabilities where the length field doesn't match up with the stream object size. The PDF generator inserts stream objects with data from the strategy generator, which can include javascript to format string vulnerabilities. The intention of the PDF generator is to test to the extremities of PDF parsers, creating documents which aren't seen usually in the real world and thus are more likely to break parsers.

#### JPEG Generator

The JPEG generator is largely a work in progress, strategies in development attempt to flip bits and replace bits with bits known to break jpeg files, such as `0x00` and `0xFF`, and other large numbers. Unfortunately, this appears to corrupt the JPEG file too much causing it to be read as invalid. The generator has currently been modified to only fuzz bits which were a certain "distance" away from the markers (0xFF), but still the file is invalid 20% of the time.

### Aggregator

The aggregator is the component of the fuzzer responsible for bridging the gap between the generators (strategies) and the harness. It functions as the manager for the fuzzing campaign taking in user supplied parameters and orchestrating the calling of generators whose output it then feeds to the harness. It then monitors the response from the harness to deicide if a crash file should be written and the campaign halted, or if the program is hanging / stuck in an infinite loop in which case the strategy should be evolved.

## Static Path Analysis

The fuzzer includes functionality to parse a binary and extract static paths, similarly to the disassembler BinaryNinja. We use the capstone library in order to disassemble the bytes of the binary into instructions. The instructions are then parsed in 2 ways:

1. By looking for jump instructions. The analysis tools keep track of the most recent point in the binary it began searching from (startPoint), and when an unseen jump instruction is found, it stores a 'jump block' which is denoted by startPoint and the address of the instruction that contains the jump. This is done recursively until all jump blocks in the binary are found. From this we are able to build a data structure that represents all blocks in the code that end in a jump.

2. By looking for function calls. When the analysis tool finds a call instruction it stores both the address of the call instruction and the address of the function being called, into a data structure. Once both of these data structures are built. We use pwntools in order to resolve the function names in the function call data structure. We also contextualize each jump block and denote in which function that jump block resides.

Furthermore, this functionality works even with PIE and ASLR enabled. Since we have the PID of the process running the binary, we are able to inspect `/proc/{pid}/maps` before fuzzing begins and find the base address of the binary and shared libraries.

### Potential Improvements

-   The jump block data structure that we build is not exactly like the static path analysis performed by BinaryNinja, it could be made more comprehensive. We do not capture blocks that end in a non returning function call like exit. We also are not able to capture blocks that are defined by looping mechanics.

-   We did not implement a infinite loop detection algorithm but I think the existing data structures support it. Our idea is to have some sort of a triggering mechanism when we are suspect that a loop is occurring, and then build a graph which grows when an existing jump block is visited. After a certain amount of iterations we start comparing the previous size of the graph to the new size of the graph. If it doesn't grow then we can assume the same places in the code are being repetitively jumped to, and the binary is stuck in an infinite loop.

## Coverage

The project implements a small module `ptfuzz` which supports a pythonic interface to the unix `ptrace` syscall. However there are plans to make heavy modifications to this area of the project for the next release see [project direction](#project-direction).

### [ptfuzz](./fuzzybear/coverage/ptfuzz/README.md)

The **ptfuzz** module is a pythonic interface to the `ptrace` unix sys call specifically targeted at fuzzing. It exposes the methods necessary to collect coverage information from a binary in blackbox settings as well as the ability to fuzz programs entirely in memory, only forking once, by saving and restoring register state in the target program.

It aims to provide an easy way to harness the power of `ptrace` for fuzzing through simple abstracted methods. Being written in python also has advantages for portability and easy of use/extensibility.

#### Architectures

Currently the module only supports `x86` and `x86_64` trace targets however extending this support is nearly as simple as adding the necessary registers and types to the `ptfuzz/_registers` file. Assuming that the `ptrace` syscall is supported on the architecture the port should be simple.

### Static Path Analysis

The fuzzer includes functionality to parse a binary and extract static paths, similarly to the disassembler BinaryNinja. We use the capstone library in order to disassemble the bytes of the binary into instructions. The instructions are then parsed in 2 ways:

1. By looking for jump instructions. The analysis tools keep track of the most recent point in the binary it began searching from (startPoint), and when an unseen jump instruction is found, it stores a 'jump block' which is denoted by startPoint and the address of the instruction that contains the jump. This is done recursively until all jump blocks in the binary are found. From this we are able to build a data structure that represents all blocks in the code that end in a jump.

2. By looking for function calls. When the analysis tool finds a call instruction it stores both the address of the call instruction and the address of the function being called, into a data structure. Once both of these data structures are built. We use pwntools in order to resolve the function names in the function call data structure. We also contextualize each jump block and denote in which function that jump block resides.

Furthermore, this functionality works even with PIE and ASLR enabled. Since we have the PID of the process running the binary, we are able to inspect `/proc/{pid}/maps` before fuzzing begins and find the base address of the binary and shared libraries.

## Project Direction

The project in its current state serves primarily as a POC or perhaps more generously as a MVP for a rudimentary binary fuzzer. For the fuzzer to be functionally useful while still attaining its goal of being highly flexible and easy to use several additions and integrations are needed.

### Roadmap

#### `V2`

-   Convert the coverage module to use a `C` wrapper around `ptrace` which will interface with the existing python bridge
-   Upgrade harness to support this new link
-   Connect the UI coverage adapter to the coverage module to update live runtime pathfinding
-   Use coverage data to establish a input corpus which is fed to generators instead of the initially supplied input corpus
-   Ease of use/extensibility changes
    -   JSON configs for UI
    -   More CLI argument support

### `V3`

-   More complex mutation engine which is both context aware in terms of input corpus file format and coverage data
-   More varied and complex input generation in general
-   More extensive input corpus support
    -   ELF
    -   PNG
    -   Network packets
-   Better fuzzing target support, network fuzzing

## Libraries

-   [rich](https://github.com/willmcgugan/rich) for GUI
-   [python-magic](#) for input file detection

## Project Structure

_Note: soon to change_

```
.
├── fuzzer
├── fuzzybear
│   ├── Aggregator.py
│   ├── coverage
│   │   ├── Coverage.py
│   │   ├── FunctionCall.py
│   │   ├── __init__.py
│   │   ├── JumpBlock.py
│   │   ├── ptfuzz
│   │   │   ├── __init__.py
│   │   │   ├── ptfuzz.py
│   │   │   ├── ptrace
│   │   │   └── README.md
│   │   ├── README.md
│   │   ├── symbols.py
│   │   └── testCoverage.py
│   ├── Harness.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── strategies
│   │   ├── CSV
│   │   │   ├── CSV.py
│   │   │   └── README.md
│   │   ├── ELF
│   │   │   ├── ELF.py
│   │   │   └── README.md
│   │   ├── __init__.py
│   │   ├── JPEG
│   │   │   ├── JPEG.py
│   │   │   └── README.md
│   │   ├── JSON
│   │   │   ├── JSON.py
│   │   │   └── README.md
│   │   ├── PDF
│   │   │   ├── bee.jpg
│   │   │   ├── bee_mov.txt
│   │   │   ├── PDF.py
│   │   │   └── README.md
│   │   ├── README.md
│   │   ├── Strategy.py
│   │   ├── TXT
│   │   │   ├── README.md
│   │   │   └── TXT.py
│   │   └── XML
│   │       ├── README.md
│   │       └── XML.py
│   ├── ui
│   │   ├── Clock.py
│   │   ├── Dashboard.py
│   │   ├── Logs.py
│   │   ├── Stats.py
│   │   ├── Summary.py
│   │   └── UIAdapter.py
│   └── utility
│       ├── codec.py
│       ├── mode.py
│       └── response_codes.py
└── README.md
```
