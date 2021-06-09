# Finding Available Domain in Breach Data

This is the project code from a <a href="https://birep.net/blog1.html">series of blog posts</a> on finding expired email domains using breach data and the Namecheap API.

countdomains.py is used to generate a counts.json file that contains a popularity ranked list of email domains spotted in breach data (BYOBD, none included here)

availabledomains.py uses the Namecheap api to check domain name availibility, and includes tools for querying the counts.json data.
