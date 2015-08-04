#!/usr/bin/python3
## By Jon Dehdari, naszka, ... , 2015
## Unsupervised segmenter, using bidirectional character backoff models
## Usage: echo 'thisisatest' | python3 segmental.py unsegmented_char_ngram_shelve_file.db

import sys
import shelve

ngram_order = 8 # replace with command-line argument

## open shelve db
print("file: ", sys.argv[1])
sh = shelve.open(sys.argv[1])

## Read in text to be segmented, from stdin
for line in sys.stdin:
    line = line.rstrip().replace(' ', '_')
    len_line = len(line)
    print(line, ':', file=sys.stderr)
    print(line[0], sep='', end='')
    for i in range(1, len_line):
        j = 0
        k = len_line
        while not line[j:i+1] in sh:
            j += 1
        while not line[i-1:k] in sh:
            k -= 1
        char_i = line[i]
        count_char_i = sh[char_i]
        forw_hist  = line[j:i]
        forw_joint = line[j:i+1]
        forw_prob = 1.0
        try:
            forw_prob = float(sh[forw_joint]) / float(sh[forw_hist])
        except:
            pass
        #print(i, 'forw_prob=', forw_prob, '=', sh[forw_joint], '/', sh[forw_hist], forw_joint, '/', forw_hist, 'k=', k)
        rev_prob = 1.0
        rev_hist = ''
        if (i < len_line):
            rev_joint = line[i-1:k]
            rev_hist  = line[i:k]
            try:
                rev_prob     = float(sh[rev_joint]) / float(sh[rev_hist])
            except:
                pass
            #print('  rev_prob=', rev_prob, '=', rev_joint, '/', rev_hist)

        prod = forw_prob * rev_prob
        #avg  = (forw_prob + rev_prob) / 2
        #print('  ', forw_hist, '|', rev_hist, ': avg=', avg, '; prod=', prod)
        

        if (prod < 0.015):
            print(" ", sep='', end='')
        print(line[i], sep='', end='')
    print()

sh.close()
