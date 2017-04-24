# Extended scraping function of any file format
import os # To format file name
import shutil # To copy file object from python to disk
import requests
import bs4 as bs

def py_file_scraper(url, html_tag='img', source_tag='src', file_type='.jpg',max=-1):
    
    '''
    Function that scrapes a website for certain file formats.
    The files will be placed in a folder called "files" in the working directory.
    
    url = the url we want to scrape from
    html_tag = the file tag (usually img for images or a for file links)
    source_tag = the source tag for the file url (usually src for images or href for files)
    file_type = .png, .jpg, .pdf, .csv, .xls etc.
    max = integer (max number of files to scrape, if = -1 it will scrape all files)
    '''
    
    # make a directory called 'files' for the files if it does not exist
    if not os.path.exists('files/'):
        os.makedirs('files/')

    source = requests.get(url).content
    soup = bs.BeautifulSoup(source,'lxml')
    
    i = 0
    for link in soup.find_all(html_tag):
        file_url=link.get(source_tag)
        
        
        if 'http' in file_url: # check that it is a valid link

            if file_type in file_url: #only check for specific file type

                file_name = os.path.splitext(os.path.basename(file_url))[0] + file_type 
                #extract file name from url

                file_source = requests.get(file_url, stream = True)
                # open new stream connection

                with open('./files/'+file_name, 'wb') as file: 
                    # open file connection, create file and write to it
                    shutil.copyfileobj(file_source.raw, file) # save the raw file object
                    print('DOWNLOADED:',file_name)
                    
                    i+=1
                    
                del file_source # delete from memory
            else:
                print('EXCLUDED:',file_url) # urls not downloaded from
                
        if i==max:
            print('Max reached')
            break  

    print('Done!')