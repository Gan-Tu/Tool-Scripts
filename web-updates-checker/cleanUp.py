'''
This file helps clean the cache files used for the checkUpdates script.
It cleans the "link" and "archive" files, if they exist.
@author Gan Tu
@version Python
'''

import os
try:
    os.remove("link")
except FileNotFoundError as e:
    pass
try:
    os.remove("archive")
except FileNotFoundError as e:
    pass
