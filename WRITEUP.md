# Fuzzy Bear

## Design Overview

The fuzzer is designed with three primary components which work together to provide the desired functionality.

+ Harness
+ Strategies
+ Aggregator


Each component and indeed the fuzzer as a whole is designed with a strong focus on modular design. For strategies to be particularly useful they need to be able to be applied with great flexibility. 

## Harness

Second only to the generators themselves is the harness. The harness is the component of the fuzzer which really makes it useful. It is responsible for feeding input to the binary through `stdin` and collecting the response from the binary to return to the aggregator. The harness also implements a **health check** function which aims to detect hangs and infinite loops in the binary. 


## Strategies

## Common

+ Foo bar

### CSV

CSV strategies focus on generating oddball data to place into *sensible* places within a CSV file  

### JSON

+ foo bar


## Aggregator

The aggregator is the component of the fuzzer responsible for bridging the gap between the generators (strategies) and the harness. It functions as the manager for the fuzzing campaign taking in user supplied parameters and orchestrating the calling of generators whose output it then feeds to the harness. 

