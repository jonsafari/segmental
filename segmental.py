#!/usr/bin/python3
## By Jon Dehdari, 2015
## Unsupervised segmenter, using bidirectional character backoff models
## Usage: echo 'thisisatest' | python3 segmental.py unsegmented_char_ngram_counts.tsv

import sys

sys.argv.pop(0) # We don't need this filename

counts = {}

## Read in count files
for filename in sys.argv:
    myfile = open(filename)
    for line in myfile:
        string, count = line.lower().rstrip().split('\t')
        if int(count) < 7:
            continue
        counts[string] = count
    myfile.close


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
        for_hist  = line[j:i]
        for_joint = line[j:i+1]
        for_prob = float(counts[for_joint]) / float(counts[for_hist])
        #print(i, 'for_prob=', for_prob, '=', counts[for_joint], '/', counts[for_hist], for_joint, '/', for_hist, 'k=', k)
        rev_prob = 1.0
        rev_hist = ''
        if (i < len_line):
            rev_joint = line[i-1:k]
            rev_hist  = line[i:k]
            rev_prob     = float(counts[rev_joint]) / float(counts[rev_hist])
            #print('  rev_prob=', rev_prob, '=', rev_joint, '/', rev_hist)

        prod = for_prob*rev_prob
        #avg  = (for_prob + rev_prob) / 2
        #print('  ', for_hist, '|', rev_hist, ': avg=', avg, '; prod=', prod)
        

        if (prod < 0.015):
            print(" ", sep='', end='')
        print(line[i], sep='', end='')
    print()
