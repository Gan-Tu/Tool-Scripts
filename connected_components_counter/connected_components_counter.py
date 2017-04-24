'''
This script contains a function that helps you find the number of connected 
components in a 2-D array. 

This is useful for grey-scale image processing purposes.
By default, we treat background values as 0 and non-background as 1.

@author Gan Tu
@version Python 3

[HOW TO CHANGE PYTHON VERSION]

This script by default should be run by Python 3.
To use this in Python 2, add the following line at the beginning 
of the file:
    from __future__ import print_function
'''

def connected_components(datum):
    numRow = len(datum)
    numCol = len(datum[0])

    labels = []
    for i in range(numRow):
        labels.append([])
        for j in range(numCol):
            labels[i].append(0)


    equivalenceTable = dict()
    labelNum = 1

    datum = datum > 0

    def smallestNeighborLabel(arr, row, col):
        smallest = 0
        dr = [0, -1, 1]
        dc = [0, -1, 1]
        for c in dc:
            for r in dr:
                if not (c == 0 and r == 0):
                    x = min(max(row + r, 0), numRow - 1)
                    y = min(max(col + c, 0), numCol - 1)
                    if arr[x][y] and labels[x][y] != 0:
                        if smallest == 0:
                            smallest = labels[x][y]
                        else:
                            smallest = min(labels[x][y], smallest)
        return smallest

    def associateNeighborLabel(arr, row, col, label, dictionary):
        dr = [0, -1, 1]
        dc = [0, -1, 1]
        for c in dc:
            for r in dr:
                if not (c == 0 and r == 0):
                    x = min(max(row + r, 0), numRow - 1)
                    y = min(max(col + c, 0), numCol - 1)
                    if arr[x][y] and labels[x][y] != 0:
                        dictionary[label].append(labels[x][y])
                        dictionary[labels[x][y]].append(label)
        return dictionary                            

    for i in range(numRow):
        for j in range(numCol):
            if datum[i][j]:
                newLabel = smallestNeighborLabel(datum, i, j)
                if newLabel == 0:
                    labels[i][j] = labelNum
                    newLabel = labelNum
                    equivalenceTable[labelNum] = [labelNum]
                    labelNum += 1
                else:
                    labels[i][j] = newLabel
                    associateNeighborLabel(datum, i, j, newLabel, equivalenceTable)

    finalLabels = dict()
    for key in equivalenceTable.keys():
        finalLabels[key] = min(equivalenceTable[key])

    return len(set(finalLabels.values()))


### UNCOMMENT THE FOLLOWING IF YOU WANT TO TEST THE CODE ###

# if __name__ == '__main__':
    
#     import numpy as np

#     def printArray(arr):
#         for i in arr:
#             print(i)

#     def testResult(data):
#         print("Testing")
#         printArray(data)
#         print("connected: " + str(connected_components(data)) + "\n")

#     testResult(np.array([[0,1,2,0],[0,4,0,2]]))
#     testResult(np.array([[0,1,0,0],[0,4,0,2]]))
#     testResult(np.array([[0,1,0,2],[0,4,0,2]]))
#     testResult(np.array([[0,1,2,2],[0,4,0,2]]))
#     testResult(np.array([[0,0,0,0], [0,1,1,0], [0,0,0,0], [0,1,0,0],\
#                             [0,1,1,0],[0,0,1,0],[1,0,0,0],[0,1,0,1],\
#                             [0,0,0,0]]))
