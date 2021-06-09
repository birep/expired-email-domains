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
import tldextract
import sys
import os
from multiprocessing import Pool

if len(sys.argv) != 3:
    print("USAGE: ./countdomains.py [path to breach data] [path to generated counts file]")
    exit()

c = Counter()

infns = []

for root, unused_dirs, files in os.walk(sys.argv[1]):
   for name in files:
      infns.append(os.path.join(root, name))

pattern = r"(?i)@([a-z0-9\-\.\_]+\.(?:com|org|net))(?::|;)"
valid = re.compile(pattern)

def stripsubdomains(domain):
    unused_sub,dom,suf = tldextract.extract(domain)
    return f"{dom}.{suf}"

def countdomains(infn):
    print(f"file: {infn}")
    with open(infn,'r') as creds:
        for cred in creds:
            result = valid.search(cred)
            if result:
                c[stripsubdomains(result.groups()[0].lower())] += 1

if __name__ == '__main__':
    with Pool() as pool:
        pool.map(countdomains, infns)
    with open(sys.argv[2], 'w') as outfile:
        outfile.write(json.dumps(sorted(c.items(), key=lambda x: x[1], reverse=True)))