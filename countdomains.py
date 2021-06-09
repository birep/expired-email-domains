#!/usr/bin/python3

# Using a path to a breach data directory which contains
# directories of text files, where each line of each file
# is 'username:password' or 'username:hash', outputs a
# json file that contains a list of counts of each .com,
# .net, or .org domain name, sorted from most- to least-popular.

# for more info see blog post: https://birep.net/blog1.html


import re
from collections import Counter
import json
import glob

c = Counter()

breachdatapath = "/home/taylor/breachdata/"
outfn = "/home/taylor/breachdata/domain_counts_all.json"
infns = glob.glob(f"{breachdatapath}//**/*")

pattern = r"(?i)@([a-z0-9\-\.\_]+\.(?:com|org|net))(?::|;)"
valid = re.compile(pattern)

for infn in infns:
    print(f"file: {infn}")
    try:
        with open(infn,'r') as creds:
            for cred in creds:
                result = valid.search(cred)
                if result:
                    c[result.groups()[0].lower()] += 1
    except KeyboardInterrupt:
        # This will run for a while, so let's allow ourselves to escape with ctrl-c
        break
    except Exception as e:
        # Many breach data text files will have non-utf-8 characters and null bytes
        # that will cause errors. To avoid the errors you can use iconv to convert your
        # files to utf-8 before scanning.
        print(f"error in file: {infn}")
        print(e)

with open(outfn, 'w') as outfile:
    outfile.write(json.dumps(sorted(c.items(), key=lambda x: x[1], reverse=True)))