'''
This script helps you download pdf files from remote destinations
@author Gan Tu
@version python 2
'''

import urllib
import re

# change this to the source url you are scrapping from
source = 'http://inst.eecs.berkeley.edu/~ee16a/fa16/dis/'

html = urllib.urlopen(source).read()

# change this to your target regex
regex = '<a href="(ans.+?.pdf)">.+</a>'
pattern = re.compile(regex)
titles = re.findall(pattern, html)

for pdf in titles:
    url = source + pdf
    print "downloading " + pdf + "..."
    file = open(pdf, "w")
    file.write(urllib.urlopen(url).read())
    file.close()
    print "success."