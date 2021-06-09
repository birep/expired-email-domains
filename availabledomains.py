#!/usr/bin/python3

# Using the Namecheap API to find available domains in breach data emails
# For more info see blog post at https://birep.net/blog2.html

# Example usage:

# >>> checkall(query('gmail',500,10))

# This will return any available domains found in the first
# 500 most-popular domains that match our querystring 'gmail',
# skipping the 10 most-popular domains.

# >>> checkall(query(''))

# This will run through the entire list of domain counts,
# returning any available domains.

import json
import xml.etree.ElementTree as ET
from math import ceil
import requests
import tldextract

infn = "/path/to/domain_counts.json"

ncuser = "[your namecheap user name]"
ncapikey = "[your namecheap api key]"
ip = "[your already-whitelisted IP address]"

with open(infn,'r') as countsjson:
    counts = json.load(countsjson)

def query(querystring,maxresults=0,skip=0):
    out = []
    for count in counts:
        if maxresults != 0 and len(out) >  maxresults + skip:
            return out[skip:]
        if querystring in count[0]:
            out.append(count[0])
    return out[skip:]

def stripsubs(domains):
    out = []
    for domain in domains:
        sub,dom,suf = tldextract.extract(domain)
        out.append(f"{dom}.{suf}")
    return list(set(out))

def getn(n,domains,startpos=0):
    if len(domains[startpos:]) >= n:
        return domains[startpos:startpos+n]
    else:
        return domains[startpos:]

def apirequesturl(domains):
    if type(domains) == list:
        domains = ",".join(domains)
    apihead = f"https://api.namecheap.com/xml.response?ApiUser={ncuser}&ApiKey={ncapikey}&UserName={ncuser}&ClientIp={ip}&Command=namecheap.domains.check&DomainList="
    return apihead+domains

def checkdomains(domains,offset=0):
    apirequest = apirequesturl(getn(50,stripsubs(domains),offset))
    resp = requests.get(apirequest) 
    root = ET.fromstring(resp.content)
    normal = []
    premium = []
    for item in root.getchildren()[3].getchildren():
        if item.attrib['Available'] == 'true':
            if item.attrib['IsPremiumName'] == 'false':
                normal.append(item.attrib['Domain'])
            else:
                premium.append((item.attrib['Domain'],item.attrib['PremiumRegistrationPrice']))
    if normal != []:
        for dom in normal:
            print(f'{dom} https://web.archive.org/web/*/{dom}')
    if premium != []:  
        for dom in premium:
            print(f"{'*'*80}\nPremium domain {dom} https://web.archive.org/web/*/{dom}\n{'*'*80}")
    return normal + premium

def checkall(domains):
    out = []
    total = len(domains)
    pages = ceil(total/50.0)
    for page in range(pages):
        for domain in checkdomains(domains,page*50):
            out.append(domain)
    return out