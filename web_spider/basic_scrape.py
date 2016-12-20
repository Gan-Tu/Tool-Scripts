# This script contains various basics of web spider tool for practice
# and educational purposes.
# @author Gan Tu
# @version Python 3

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

def dummyGetUrls(url, maxDisplay=50):
    urls = [url]
    visited = [url]
    couter = 0
    stop = False
    while len(urls) > 0:
        try:
            htmltext = urllib.request.urlopen(urls[0]).read()
        except:
            print("error url: " + urls[0])
        soup = BeautifulSoup(htmltext, "html.parser")
        urls.pop(0)
        for tag in soup.findAll('a', href=True):
            # Make sure all urls have root url domain name
            tag["href"] = urllib.parse.urljoin(url, tag["href"])
            if url in tag["href"] and tag["href"] not in visited:
                urls.append(tag['href'])
                visited.append(tag['href'])
                couter = couter + 1
            if couter > maxDisplay:
                stop = True
                break
        if stop:
            print(visited)
            break

def dummyGetUrls2(url, maxDisplay=50):
    htmltext = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(htmltext, "html.parser")
    count = 0
    for tag in soup.findAll('a', href=True):
        raw = tag['href']

        # Get rid of browser added random affix
        b1 = urllib.parse.urlparse(tag['href']).hostname
        if b1 == None:
            # Make sure all urls have root url domain name
            tag["href"] = urllib.parse.urljoin(url, tag["href"])
            b1 = urllib.parse.urlparse(tag['href']).hostname
        b2 = urllib.parse.urlparse(tag['href']).path
        print("http://" + b1 + b2)
        count += 1
        if count > maxDisplay:
            return

def cycleGetUrls(url, maxDisplay=50):
    urls = [url]
    visited = []
    count = 0
    stop = False
    while len(urls) > 0:
        thisUrl = urls.pop(0)
        print(thisUrl)
        htmltext = urllib.request.urlopen(thisUrl).read()
        visited.append(thisUrl)
        soup = BeautifulSoup(htmltext, "html.parser")
        for tag in soup.findAll('a', href=True):
            raw = tag['href']

            # Get rid of browser added random affix
            b1 = urllib.parse.urlparse(tag['href']).hostname
            if b1 == None:
                # Make sure all urls have root url domain name
                tag["href"] = urllib.parse.urljoin(thisUrl + "/", tag["href"])
                b1 = urllib.parse.urlparse(tag['href']).hostname
            print("b1: " + b1)
            b2 = urllib.parse.urlparse(tag['href']).path
            print("b2: " + b2)
            newUrl = "http://" + b1 + b2
            if newUrl not in visited and newUrl not in urls:
                urls.append(newUrl)
            count += 1
            if count > maxDisplay:
                stop = True
            if stop:
                print(urls)
                return

if __name__ == "__main__":
    nyt = "http://nytimes.com"
    sample = "https://tugan0329.bitbucket.io/testing-htmls/web-spider"
    cycleGetUrls(sample)

