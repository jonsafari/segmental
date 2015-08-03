#!/usr/bin/python3
## By Jon Dehdari, 2015
## Counts character n-grams and puts them into an sqlite3 database
## Usage: cat text.txt | python3 char_ngram2sqlite.py ngrams.db

import sys
import sqlite3 as db

ngram_order = 5 # replace with command-line argument

db_filename = sys.argv[1] # replace with command-line argument

counts = {}
for line in sys.stdin:
    line = line.rstrip().replace(' ', '')
    for i in range(0, len(line)):
        j = max(0, i - ngram_order) # the ngram spans from j to i
        for k in range(j,i):
            if line[k:i] in counts:
                counts[line[k:i]] += 1
            else:
                counts[line[k:i]] = 1


con = db.connect(db_filename)

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS ngrams")
    cur.execute("CREATE TABLE ngrams (ngram text, count int)")
    cur.executemany("INSERT INTO ngrams VALUES(?, ?)", counts.items())
    cur.execute("create index ngram_index on ngrams (ngram)")
    cur.execute("vacuum ngrams")
