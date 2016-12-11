'''
This script helps you scrap stock data avaliable on Bloomberg Finance
and store them locally.

Please obey applicable local and federal laws and applicable API term of use
when using this scripts. I, the creater of this script, will not be responsible
for any legal issues resulting from the use of this script.

@author Gan Tu
@version python 2 or python 3

[HOW TO CHANGE PYTHON VERSION]

This script by default should be run by Python 2.
To use this in Python 3, change the followings:

1) change ALL occurrences of "urllib" to "urllib.request". 
'''

import urllib
import re
import json
import os


# Stock Symbols Initialization
# Feel free to modify the file source to contain stock symbols you plan to scrap fro
stocks = open("nasdaq_symbols.txt", "r").read().split("\n")

# URL Initialization
urlPrefix = "http://www.bloomberg.com/markets/api/bulk-time-series/price/"
urlAffix = "%3AUS?timeFrame="

# Only four of these are valid options for now
# 1_Day will scrap minute by minute data for one day, while others will be daily close price
# Feel free to modify them for your own need
options = ["1_DAY", "1_MONTH", "1_YEAR", "5_YEAR"]

def setup():
    try:
        os.mkdir("data")
    except Exception as e:
        pass
    for option in options:
        try:
            os.mkdir("data/" + option + "/")
        except Exception as e:
            pass

def scrap():
    i = 0
    while i < len(stocks):
        for option in options:
            file = open("data/" + option + "/" + stocks[i] + ".txt", "w")
            file.close()
            htmltext = urllib.urlopen(urlPrefix + stocks[i] + urlAffix + option)
            try:
                data = json.load(htmltext)[0]["price"]
                key = "date"
                if option == "1_DAY":
                    key = "dateTime"
                file = open("data/" + option + "/" + stocks[i] + ".txt", "a")
                for price in data:
                    file.write(stocks[i] + "," + price[key] + "," + str(price["value"]) + "\n")
                file.close()
            except Exception as e:
                pass
        i += 1


if __name__ == "__main__":
    setup()
    scrap()

