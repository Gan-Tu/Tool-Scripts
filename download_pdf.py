'''
This script helps you download pdf files from remote destinations
@author Gan Tu
@version python 2

[HOW TO CHANGE PYTHON VERSION]

This script by default should be run by Python 2.
To use this in Python 3, change the followings:

1) change ALL occurrences of "urllib" to "urllib.request". 
2) change print "success." to  print("sucess")
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