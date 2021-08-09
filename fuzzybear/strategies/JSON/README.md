# JSON

Similarly to the CSV based strategies the JSON generator attempts to create sane json structures with unnatural and unexpected fields which may cause a parser to break and  memory corruption to occur. 

## Key Strategies

### Random Field Replacement

A key strategy that the JSON mutator implements is the ability to select a random field to alter with other tactics data primarily from the super class.

### Extra Fields

The JSON generator also implements a function to add a large number of extra fields in the hopes of causing overflow based crashes to occur. This could arise when the program attempts to read the entire JSON data object into a stack based buffer or into heap memory.