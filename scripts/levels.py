import csv
import json
import sys

try: 
    src  = sys.argv[1]
    dest = sys.argv[2]

except:
    print("usage: $ python this.py <src.csv> <dest.{csv, json}>")

def row (name):
    name = name.replace('\n', '')
    return dict(
        filename=name,
        key=(name
            .replace(".txt", "")
            .replace("_", "-")
            .lower())
    )

def aggregate (rows, f):
    count = {}
    filt  = {}
    for r in rows:
        fr = r[f]
        if fr in count:   
            count[fr] += 1
        else:  
            count[fr] = 1  
            filt[fr] = r
    for k, ck in count.items():
        filt[k]["count"] = ck
    return list(filt.values())


rows   = [row(n) for n in open(src, "r").readlines()]
table  = aggregate(rows, "filename")


if dest[-4:] == ".csv":
    out = csv.DictWriter(open(dest, "w"), ["filename", "key", "count"])
    out.writeheader()
    out.writerows(table)

elif dest[-5:] == ".json":
    json.dump(table, open(dest, "w"))
