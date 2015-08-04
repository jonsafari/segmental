#!/usr/bin/python3
## By Jon Dehdari, naszka, ... , 2015
## Counts character n-grams and puts them into persistent shelved file.  If you want lower/upper-case merged, do it beforehand
## Usage: cat text.txt | python3 txt2chardb.py ngrams.db

import sys
import shelve

ngram_order = 8 # replace with command-line argument
min_count   = 5 # replace with command-line argument

db_filename = sys.argv[1] # replace with command-line argument

# Count character ngrams from stdin, removing whitespace
counts = {}
for line in sys.stdin:
    line = line.rstrip().replace(' ', '') # probably should use a unicode character class for whitespace
    for i in range(0, len(line)):
        j = max(0, i - ngram_order) # the full ngram spans from j to i; intermediate ngram spans from k to i
        for k in range(j,i):
            if line[k:i] in counts:
                counts[line[k:i]] += 1
            else:
                counts[line[k:i]] = 1


with shelve.open(db_filename) as sh:
    for k, v in counts.items():
        if v >= min_count: # discard singleton ngrams
         sh[k]=v
