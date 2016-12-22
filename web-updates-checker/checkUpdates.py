''' 
This script checks if a given website has new updates.
It works by comparing the website at the time of checking
against the cache file of past website archive, saved as "archive"
@author Gan Tu
@version Python 3
'''

import urllib.request

def getArchive():
    try:
        backup = open("archive", "r")
        archive = backup.read()
        backup.close()
        return backup
    except IOError as e:
        print("No archive reference file found.")
        return None

def getLink():
    try:
        link = open("link", "r").read()
        print("Do you still want to check: \n" + link)
        print("yes of no (y/n)?")
        newLink = input()
        if not "y" in newLink:
            link = input("type the full website link to check: ")
            if not "http://" in link:
                link = "http://" + link
            temp = open("link", "w")
            temp.write(str(link))
            temp.close()
            print("updated the link in the database for future reference")
        return link
    except IOError as e:
        link = input("type the full website link to check: ")
        temp = open("link", "w")
        temp.write(link)
        temp.close()
        print("updated the link in the database for future reference")
        return link

if __name__ == "__main__":

    link = getLink()
    try:
        htmltext = urllib.request.urlopen(link).read()
        archive = getArchive()
        if archive == None:
            print("Error: Cannot compare this time due to lack of archive file.")
            archive = open("archive", "w")
            archive.write(str(htmltext))
            archive.close()
            print("Saved the current state of website to 'archive' for future checking.")
            print("Warning: Don't delete 'archive' file.")
        else:
            if archive != htmltext:
                print("new updates!")
                print("go check it out at " + link)
                file = open("archive", "w")
                file.write(str(htmltext))
                file.close()
                print("New website info has been updated in 'archive'")
            else:
                print("no updates")
    except Exception as e:
        print("wrong url given: " + link)
        print(e)
    