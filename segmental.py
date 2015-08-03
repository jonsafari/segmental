#!/usr/bin/python3
## By Jon Dehdari, 2015
## Unsupervised segmenter, using bidirectional character backoff models
## Usage: echo 'thisisatest' | python3 segmental.py unsegmented_char_ngram_counts.tsv

import sys
import sqlite3 as db

ngram_order = 8 # replace with command-line argument

counts = {}

con = db.connect(sys.argv[1]) # replace with command-line argument

#with con:

### Read in count files
#for filename in sys.argv:
#    with open(filename) as myfile:
#        for line in myfile:
#            string, count = line.lower().rstrip().split('\t')
#            if int(count) < 7:
#                continue
#            counts[string] = count


def select(key):
    if key == '':
        return 0
    cur = con.cursor()
    cur.execute("SELECT count FROM ngrams WHERE ngram = ?", (key, ))
    row = cur.fetchone()
    if (row == None):
        return 0
    count = row[0]
    return count

## Read in text to be segmented, from stdin
for line in sys.stdin:
    line = line.rstrip().replace(' ', '_')
    len_line = len(line)
    print(line, ':', file=sys.stderr)
    print(line[0], sep='', end='')
    for i in range(1, len_line):
        char_i = line[i]
        #print("char_i=", char_i)
        count_char_i = select(char_i)

        j = max(0, i - ngram_order)
        k = min(len_line, i + ngram_order)
        #while not line[j:i+1] in counts:
        while select(line[j:i+1]) < 1:
            #print("j=", j, "i+1=", i+1, "key=", line[j:i+1])
            j += 1
        while select(line[i-1:k]) < 1:
            #print("i-1=", i-1, "k=", k, "key=", line[i-1:k])
            k -= 1

        forw_hist  = line[j:i]
        forw_joint = line[j:i+1]
        forw_prob = 1.0
        try:
            forw_prob = float(select(forw_joint)) / float(select(forw_hist))
        except:
            pass
        #print(i, 'forw_prob=', forw_prob, '=', select(forw_joint), '/', select(forw_hist), forw_joint, '/', forw_hist, 'k=', k)
        rev_prob = 1.0
        rev_hist = ''
        if (i < len_line):
            rev_joint = line[i-1:k]
            rev_hist  = line[i:k]
            try:
                rev_prob = float(select(rev_joint)) / float(select(rev_hist))
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
