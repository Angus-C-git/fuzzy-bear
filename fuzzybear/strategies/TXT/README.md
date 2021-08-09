# Plaintext (TXT)

Being a versatile format the TXT generator primarily implements strategies from the superclass for its operations. It does however implement a few specific approaches which target typical usage of text file inputs.

## Key Strategies

### Control Characters

This strategy aims to break programs that display or render the data in some form or which attempt to use the data for control. It may also cause corruption in programs which attempt to encode the data.

### Format Strings

This strategy aims to break programs that render or log data from the read in file directly in a format function like `printf` or `syslog` by injecting format string payloads into the fuzzed file.

### System Words

This strategy aims to break programs that use the data from the received text stream to issue or modify shell or system calls by supplying unix system and shell keywords.

