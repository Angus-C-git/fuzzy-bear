# XML

The XML generator modifies valid XML files by appending elements, inserting sub elements and overwriting elements/attributes with data from the strategy generator. This generator also creates files that include other files such as dev/random with the intention of creating buffer overflows in the target program. 

## Key Strategies

### Deep Nesting

The deep nesting strategy builds a deep set of nested tags into the input file by recursing to a `MAX_DEPTH` building up a tree like structure that hopes to break parsers and/or cause memory corruption to occur by exceeding buffer sizes, overflowing counters and wasting program cycles.

### Repeated Tags

We employee repeated tags as a strategy to increase the size of the XML document for the parser in the hopes that it will cause an overflow to occur on the stack or in heap memory.


### Format Strings

Since XML documents have a tendency to be rendered, displayed and used by format functions we employ the format string tactic in the hopes of causing memory corruption by writing to memory with `%n` and `%n` family of specifiers.