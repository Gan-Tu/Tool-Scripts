# Introduction
This tool helps you check whether if a website has new updates.

# Mechanism
It compares the HTML source files of the current website against past backup copies saved in the cache file named 'archive', which will be generated after first running of the script.

The link used in the last time will be saved in 'link' cache file. If it is your first running, the script will generate this file for you as well.

# Usage
You need at least Python 3 to run this.

To check updates, run the following line and then following instructions prompted on your terminal command:
```
$ python3 checkUpdates.py
```

To clean the cahce files ('archive' and 'link'), you can run:
```
$ python3 cleanUp.py
```
