#!/usr/bin/python3
## By Jon Dehdari, 2015
## Unsupervised segmenter, using bidirectional character backoff models
## Usage: echo 'thisisatest' | python3 segmental.py unsegmented_char_ngram_counts.tsv

import sys
import sqlite3

sys.argv.pop(0) # We don't need this filename

counts = {}

## Read in count files
for filename in sys.argv:
    with open(filename) as myfile:
        for line in myfile:
            string, count = line.lower().rstrip().split('\t')
            if int(count) < 7:
                continue
            counts[string] = count


## Read in text to be segmented, from stdin
for line in sys.stdin:
    line = line.rstrip().replace(' ', '_')
    len_line = len(line)
    print(line, ':', file=sys.stderr)
    print(line[0], sep='', end='')
    for i in range(1, len_line):
        j = 0
        k = len_line
        while not line[j:i+1] in counts:
            j += 1
        while not line[i-1:k] in counts:
            k -= 1
        char_i = line[i]
        count_char_i = counts[char_i]
        forw_hist  = line[j:i]
        forw_joint = line[j:i+1]
        forw_prob = float(counts[forw_joint]) / float(counts[forw_hist])
        #print(i, 'forw_prob=', forw_prob, '=', counts[forw_joint], '/', counts[forw_hist], forw_joint, '/', forw_hist, 'k=', k)
        rev_prob = 1.0
        rev_hist = ''
        if (i < len_line):
            rev_joint = line[i-1:k]
            rev_hist  = line[i:k]
            rev_prob     = float(counts[rev_joint]) / float(counts[rev_hist])
            #print('  rev_prob=', rev_prob, '=', rev_joint, '/', rev_hist)

        prod = forw_prob * rev_prob
        #avg  = (forw_prob + rev_prob) / 2
        #print('  ', forw_hist, '|', rev_hist, ': avg=', avg, '; prod=', prod)
        

        if (prod < 0.015):
            print(" ", sep='', end='')
        print(line[i], sep='', end='')
    print()
