# JPEG

While JPEG fuzzer is in its infancy, we still implemented strategies which attempt to flip bits and replace bytes with bad bytes known to break jpeg files, such as `0x00` and `0xFF`, and other large numbers. Unfortunately, this often causes the JPEG file to be invalidated by parsers before the fuzzed data can reach further into the program. Afterwards, we attempted to also only fuzz bits which were a certain "distance" away from the markers `(0xFF)`, but still the fuzzed file was invalid 20% of the time. Thus the JPEG fuzzing strategy is a work in progress.

## Key Strategies

### Bit Flips

Focuses on flipping bits in known sections of the JPEG file format which may result in parser memory corruption when attempting to interpret the malicious JPEG.

### Byte Swaps

The byte swap strategy involves replacing bytes in known sections and key areas of the binary with bad bytes which may result in memory corruption when the JPEG parser attempts to understand the fuzzed file.