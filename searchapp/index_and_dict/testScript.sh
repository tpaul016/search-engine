#!/bin/bash

# This script is for Testing purposes only
# Uses ripgrep (rg) to search the corpus for occurences of the argument supplied

rg -w "$1" --files-with-matches --stats ../cor_pre_proc/corpus/ 
