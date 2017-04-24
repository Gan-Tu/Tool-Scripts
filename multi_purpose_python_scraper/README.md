# Introduction
This is a python scrapper that helps you scrap all specified targets from given websites

# Usage
You need Python3 or above to use this tool, and you need to download these packages:
shutil

The files will be placed in a folder called "files" in the working directory.
```
py_file_scraper(url, html_tag='img', source_tag='src', file_type='.jpg',max=-1)
```
url = the url we want to scrape from
html_tag = the file tag (usually img for images or a for file links)
source_tag = the source tag for the file url (usually src for images or href for files)
file_type = .png, .jpg, .pdf, .csv, .xls etc.
max = integer (max number of files to scrape, if = -1 it will scrape all files)

