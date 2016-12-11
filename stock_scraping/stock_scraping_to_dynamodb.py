'''
This script helps you scrap today's minute by minute stock data avaliable up until now
from Yahoo Finance and store them to a DynamoDB NoSQL table you created on your AWS DynamoDB.

Please obey applicable local and federal laws and applicable API term of use
when using this scripts. I, the creater of this script, will not be responsible
for any legal issues resulting from the use of this script.

It assumes that you have necessary instructions setted up already for your
AWS credentials, as well as boto3 library by AWS.
For more information, check out AWS offical documentation online.
@author Gan Tu
@version python 3
'''

import boto3
import urllib.request
import json
import datetime
import time

# Access dynamodb for use.
dynamodb = boto3.resource('dynamodb')

# Feel free to change the table to the one you will use to store the data.
table = dynamodb.Table('stock-v1')

# Stock Symbols Initialization
# Feel free to modify the file source to contain stock symbols you plan to scrap from
stocks = open("s&p500_symbols.txt", "r").read().split("\n")

# URL Initialization
urlPrefix = "https://query2.finance.yahoo.com/v7/finance/chart/"
url2 = "?period="
url3 = "&interval="
interval = "1m"
url4 = "&indicators=quote&includeTimestamps=true&includePrePost=true&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com"
today = str(time.mktime(datetime.date.today().timetuple()))


i = 0
while i < len(stocks):
    symbol = stocks[i]
    url = urlPrefix + symbol + url2 + today + url3 + interval + url4
    htmltext = urllib.request.urlopen(url).read().decode('utf8')
    try:
        print("adding values for " + symbol +" stock quotes ... ")
        data = json.loads(htmltext)["chart"]["result"][0]
        quote = data["indicators"]["quote"][0]
        with table.batch_writer(overwrite_by_pkeys=['symbol', 'timestamp']) as batch:
            for j in range(len(data["timestamp"])):
                _timestamp = str(data["timestamp"][j])
                _close = str(quote["close"][j])
                _high = str(quote["high"][j])
                _low = str(quote["low"][j])
                _open = str(quote["open"][j])
                _volume = str(quote["volume"][j])
                if _timestamp != 'None' and _close != 'None' and _high != 'None':
                    if _low != 'None' and _open != 'None' and _volume != 'None':
                        batch.put_item(
                            Item={
                                'symbol': symbol,
                                'timestamp': _timestamp,
                                'close': _close,
                                'high': _high,
                                'low': _low,
                                'open': _open,
                                'volume': _volume
                            }
                        )
        print("success \n")
    except Exception as e:
        print(str(e))
    i += 1

