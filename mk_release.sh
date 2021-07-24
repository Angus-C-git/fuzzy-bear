#!/bin/bash

echo
echo "Creating a new release for fuzzybear ..."
echo

# probably want to pip freeze into requirments too 

tar -cf releases/fuzzer.tar fuzzer fuzzybear/ install.sh README.md requirements.txt