import sys
import logging
import os

logging.basicConfig(filename="a.log", level=logging.DEBUG)

files = []
CONCURRENTIAL = False
for o in sys.argv()[1:]:
    if o[0] != "-":
        files.append[o]
    elif o = "-c":
        CONCURRENTIAL = True

datadata = []

for f in files:
    try:
        datadata.append(open(f))
    except IOError:
        logging.error("Il file %s non esiste", f)
    else:
        logging.info("Il file %s è stato aperto correttamente", f)

count = dict()

if !CONCURRENTIAL:
    for data in datadata:
        for r in data:
            r = r.strip().split()
            if ( r[1] not in count.keys() ):
                count[r[1]] = 1
            else:
                count[r[1]] += 1
        
