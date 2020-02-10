#!/bin/bash

# This script is for Testing purposes only
# Uses ripgrep (rg) to search the corpus for occurences of the argument supplied

rg "$1" --files-with-matches --stats ../cor_pre_proc/corpus/ 
