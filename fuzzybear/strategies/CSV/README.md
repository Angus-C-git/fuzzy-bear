# Comma Separated Values (CSV)

CSV strategies focus on generating oddball data to place into *sensible* places within a CSV file. Currently this mainly revolves around loading the input file into memory and then mutating that data structures fields using tactics implemented in the super class.


## Key Strategies

### Add Entries

The CSV strategy implements `add_entries` which focuses on creating a large valid csv structure with many rows/columns. This has the goal of causing memory corruption on the stack or heap if a program does not properly sanitize the amount of data it receives.

### Negate

This strategy is implemented in the super class but is of particular importance to CSV files which often contain numerical data. The strategy takes single fields from the input sample and inserts their negated counterparts where the data can be interpreted as a integer or float or otherwise prepends the `-` char to the data. This strategy has the goal of causing memory corruptions due to out of bounds reads, created when a value from the CSV is expected/assumed to be positive and then is not properly enforced by the program. 
