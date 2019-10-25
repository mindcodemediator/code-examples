import random
import time
import numpy as np     # installed with matplotlib
import matplotlib.pyplot as plt
from decimal import *
import winsound


 #################Heap sort########################## 

def maxHeapify(heap, index, size):
    ###recursively make into heap###

    left = getLeft(index)
    right = getRight(index)

    if left < size and heap[left] > heap[index]:
        max = left
    else:
        max = index

    if right < size and heap[right] > heap[max]:
        max = right

    if max != index:
        heap[index], heap[max] = heap[max], heap[index]
        heap = maxHeapify(heap, max, size)
    
    return heap;

def getLeft(index):
    return 2 * index + 1

def getRight(index):
    return 2 * index + 2


def buildMaxHeap(heap):
    #create a heap to bring highest nodes to be on top
    size = len(heap)

    for i in range(int(size/2), -1, -1):
        maxHeapify(heap, i, size)

    return size

def sortHeap(heap):
    #initiates sort heap from array
    size = buildMaxHeap(heap)

    for i in range (size - 1, 0, -1):
        heap[i], heap[0] = heap[0], heap[i]
        size = size - 1
        heap = maxHeapify(heap, 0, size)
    return heap


##########################Binary Search Tree####################################
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def makeBST(textFile):
    ##main call to create BST from a text file of numbers in string form
    root = BSTNode(int(textFile.readline()))

    for line in textFile:
        root = insertNode(root, int(line))

    return root

def insertNode(root, num ):
    ##recursively inserts in order as per BST rules
   if root == None:
       root = BSTNode(num)
       return root
   current = root;
   parent = root;

   while current is not None:
       parent = current
       if num <= current.value:
           current = current.left
       else:
           current = current.right
   if num <= parent.value:
       parent.left = BSTNode(num)
   else:
       parent.right = BSTNode(num)
    
   return root


# Iterative function for inorder tree traversal since recursion was causing issues with ascending and descending lists
def MorrisTraversal(root, sorted): 
    #FYI this function was copied from https://www.geeksforgeeks.org/inorder-tree-traversal-without-recursion-and-without-stack/
    # see below function for commented out recursive inorder that I wrote. Because BST was extra feature not required in assignment and in 
    # the interest of time, I copied an iterative version in order to get time to compare
    
    #####MY FUNCTION#####
    #def inOrder(root, sorted):  written by me, iteration for this throws exception because of stack overflow
    #   if root.left is not None:
    #       sorted = inOrder(root.left, sorted)
    #       sorted.append(root.value)
    #       if root.right is not None:
    #           sorted = inOrder(root.right, sorted)
    #   return sorted
    #####################
      
    # Set current to root of binary tree 
    current = root  
      
    while(current is not None): 
          
        if current.left is None: 
            sorted.append(current.value) 
            current = current.right 
        else: 
            # Find the inorder predecessor of current 
            pre = current.left 
            while(pre.right is not None and pre.right != current): 
                pre = pre.right 
   
            # Make current as right child of its inorder predecessor 
            if(pre.right is None): 
                pre.right = current 
                current = current.left 
                  
            # Revert the changes made in if part to restore the  
            # original tree i.e., fix the right child of predecssor 
            else: 
                pre.right = None
                sorted.append(current.value)  
                current = current.right
    return sorted




###########################################QUICK SORT#################################################
def quickMedianThree(arr, left, right):
    #helper function, finds pivot from last, first and middle. moves pivot to 1 before the end and ensures first and last are lowest and highest of the three respectively
    mid = (left + right) // 2

    #swap elements so that of the three, on the right is the smallest, 
    #at the middle is next and at the end is the biggest element
    if arr[mid] < arr[left]:
        arr[left], arr[mid] =  arr[mid], arr[left]
    if arr[right] < arr[left]:
        arr[left] , arr[right] = arr[right] , arr[left]
    if arr[right] < arr[mid]:
        arr[right] , arr[mid] = arr[mid] , arr[right]

    #move medium element to one before end
    arr[right - 1] , arr[mid] = arr[mid] , arr[right - 1]
    return arr[right-1]

def quickSort(arr, left, right):
  # function called to sort using quick sort. calls heapsort when list is very small 
    if left == right: return arr
    if left + 5 <= right:  #as per book, QS is not efficient for very small lists, borrow from heapSort when sections are small
        
        pivot = quickMedianThree(arr, left, right)

        i = left + 1
        j = right - 2


        while(i != j):
            
            
            while(arr[i]< pivot and i!= j):
                i+=1
            while(arr[j] > pivot and i!=j):
                j-=1
            if(arr[i] == arr[j] and i < j):
                i+=1
            arr[i], arr[j] = arr[j], arr[i] # swap
            if(j - 1 == i): i+=1

        
        arr[i] , arr[right-1] = arr[right-1] , arr[i]
        arr = quickSort(arr, left, i - 1)
        arr = quickSort(arr, i+1, right)


    else:
        arr[left:right+1] = sortHeap(arr[left:right+1])
    return arr
     
#############################################Helper functions########################################################
def makeIntList(file_object):
    #takes file and converts to a list of integers
    intList = list()
    for line in file_object:
        intList.append(int(line))
    return intList

def writeFiles():
 #Function creates files to sort
    #create files to write numbers into
    smlFileRnd = open("smallFileRandom.txt", "w+")
    smlFileAsd = open("smallFileAscending.txt", "w+")
    smlFileDsd = open("smallFileDescending.txt", "w+")
    medFileRnd = open("mediumFileRandom.txt", "w+")
    medFileAsd = open("mediumFileAscending.txt", "w+")
    medFileDsd = open("mediumFileDescending.txt", "w+")
    lrgFileRnd = open("largeFileRandom.txt", "w+")
    lrgFileAsd = open("largeFileAscending.txt", "w+")
    lrgFileDsd = open("largeFileDescending.txt", "w+")
    ginFileRnd = open("ginormousFileRandom.txt", "w+")
    ginFileAsd = open("ginormousFileAscending.txt", "w+")
    ginFileDsd = open("ginormousFileDescending.txt", "w+")


    #for the first 5000, add to all size files to save iterations
    for i in range(0, 5000):
        smlFileAsd.write("%d\n" % i)
        smlFileDsd.write("%d\n" % (5000-i))
        smlFileRnd.write("%d\n" % random.randrange(5000))
        medFileAsd.write("%d\n" % i)
        medFileDsd.write("%d\n" % (10000-i))
        medFileRnd.write("%d\n" % random.randrange(10000))
        lrgFileAsd.write("%d\n" % i)
        lrgFileDsd.write("%d\n" % (50000 - i))
        lrgFileRnd.write("%d\n" % random.randrange(50000))
        ginFileAsd.write("%d\n" % i)
        ginFileDsd.write("%d\n" % (500000 - i))
        ginFileRnd.write("%d\n" % random.randrange(500000))
    
    #continue to add to medium and large files
    for i in range(5001, 10000):
        medFileAsd.write("%d\n" % i)
        medFileDsd.write("%d\n" % (10000-i))
        medFileRnd.write("%d\n" % random.randrange(10000))
        lrgFileAsd.write("%d\n" % i)
        lrgFileDsd.write("%d\n" % (50000 - i))
        lrgFileRnd.write("%d\n" % random.randrange(50000))
        ginFileAsd.write("%d\n" % i)
        ginFileDsd.write("%d\n" % (500000 - i))
        ginFileRnd.write("%d\n" % random.randrange(500000))

    #add the rest of the numbers to the largest file
    for i in range(10001, 50000):
        lrgFileAsd.write("%d\n" % i)
        lrgFileDsd.write("%d\n" % (50000 - i))
        lrgFileRnd.write("%d\n" % random.randrange(50000))
        ginFileAsd.write("%d\n" % i)
        ginFileDsd.write("%d\n" % (500000 - i))
        ginFileRnd.write("%d\n" % random.randrange(500000))

    for i in range (50001,500000):
        ginFileAsd.write("%d\n" % i)
        ginFileDsd.write("%d\n" % (500000 - i))
        ginFileRnd.write("%d\n" % random.randrange(500000))

    smlFileRnd.close()
    smlFileAsd.close()
    smlFileDsd.close()
    medFileRnd.close()
    medFileAsd.close()
    medFileDsd.close()
    lrgFileRnd.close()
    lrgFileAsd.close()
    lrgFileDsd.close()
    ginFileRnd.close()
    ginFileAsd.close()
    ginFileDsd.close()
######################################################################################################################################




############################################  MAIN   #############################################
def main():
###With more time, I would create more abstraction here and have main doing less.

    print('creating files size 5000, 10,000, 50,000 & 500,000.\nwait a moment please')
    writeFiles()

    # of times to run search. NOTE: over 2 or 3 will take a long time
    iterations = 3



    #INCLUDING MY TEST LIST FOR TESTING SMALL LIST IN QUICKSORT
   # testList = [2, 4, 7, 14, 93, 18, 35, 46, 32, 54, 6, 12, 27, 15, 18, 54, 35]
   # testQuickSort = quickSort(testList, 0, len(testList) -1 )
   # print(testQuickSort)

    
   #dictionary with file information 
   fileInfo = {'smallFileRandom':{'size':5000, 'numtype':'random'}, 'smallFileAscending':{'size':5000, 'numtype':'ascending'}, 'smallFileDescending':{'size':5000, 'numtype':'descending'}, 
                      'mediumFileRandom':{'size':10000, 'numtype':'random'}, 'mediumFileAscending':{'size':10000, 'numtype':'ascending'}, 'mediumFileDescending':{'size':10000, 'numtype':'descending'},
                      'largeFileRandom':{'size':50000, 'numtype':'random'}, 'largeFileAscending':{'size':50000, 'numtype':'ascending'}, 'largeFileDescending':{'size':50000, 'numtype':'descending'},
                      'ginormousFileRandom':{'size':500000, 'numtype':'random'}, 'ginormousFileAscending':{'size':500000, 'numtype':'ascending'}, 'ginormousFileDescending':{'size':500000, 'numtype':'descending'}}
    print('Processing {} times to get an average... what a great time to practice meditation!'.format(iterations))
    
    #two dimensional dictionary to track each run time and then get averages
    tracker = {'bst':{},'heap':{},'quick':{}}
    for j in tracker:
        tracker[j]['averagesInOrder'] = list()
    
    ###iterate over all of the files, running all three sort types on each file the amount of times specified in iterations. Keeps track of times and averages     
    for i in fileInfo.keys(): 
        with open(i + '.txt', "r") as file_object:
            for j in tracker:  #add entry for file name
                tracker[j][i] = {'avg':0, 'runs':list()}
            print(i)
            for x in range(0, iterations):
                print(x)
                                
                ##BST###
                print('bst')
                if(i == 'largeFileAscending' or i == 'largeFileDescending' or i == 'ginormousFileAscending' or i == 'ginormousFileDescending'):
                    #the BST takes A LONG time for big ordered files so we can skip these and count these as completely not efficient
                    print("{} is too lopsided and large for BST.".format(i))
                    tracker['bst'][i]['runs'].append(0)
                else:

                    file_object.seek(0)
                    timer = time.time()
                    root = makeBST(file_object)               
                    orderList = list()
                    orderList = MorrisTraversal(root , orderList);
                    timer = round(time.time() - timer, 5) # round to 5 decimal places
                    tracker['bst'][i]['runs'].append(timer)

                ##Heap sort##            
                print('heap')
                file_object.seek(0)
                timer = time.time()
                intList = makeIntList(file_object) #include file parsing time for both quad sorts that need the array because BST takes raw file and parses per line
                heapList = sortHeap(intList)
                timer = round(time.time() - timer, 5) # round to 5 decimal places
                tracker['heap'][i]['runs'].append(timer)

                ##quick sort##
                print('quick')
                file_object.seek(0)
                timer = time.time()
                intList = makeIntList(file_object)
                quickList = quickSort(intList, 0 , len(intList) - 1)
                timer = round(time.time() - timer, 5) # round to 5 decimal places
                tracker['quick'][i]['runs'].append(timer)
            

            #get average of runs for that file name
            for j in tracker:  
                print(j)
                tracker[j][i]['average'] = np.mean(tracker[j][i]['runs'])
            
                tracker[j]['averagesInOrder'].append(tracker[j][i]['average']) 
                print(tracker[j]['averagesInOrder'])
                
            #make a list for matplotlib, would do this cleaner with more time
            bstAvgList = tracker['bst']['averagesInOrder']
            heapAvgList = tracker['heap']['averagesInOrder']
            quickAvgList = tracker['quick']['averagesInOrder']
    
    
    #labels for matplotlib
    labelstuff = list()
    for n in fileInfo:
        labelstuff.append('size: ' + str(fileInfo[n]['size']) + ', type: ' + fileInfo[n]['numtype'])

    title = 'Average sort times of {} attempts\n Note: Largest inorder lists are not sorted by BST because they are too inefficient'.format(iterations)

    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 100  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

    #################################################
    #Plot 1 large scale
    index = np.arange(12)      
    bar_width = 0.30  # the width of the bars

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15,6))

    ax1.bar(index - bar_width/2, bstAvgList, bar_width, color='b',
            label='BST')
    ax1.bar(index + bar_width/2, heapAvgList, bar_width, color='r',
            label='heap')
    ax1.bar(index + 1.5 * bar_width, quickAvgList, bar_width, color='g',
            label='quick')

    ax1.set_xlabel('Files')
    ax1.set_ylabel('Time')
    ax1.set_title(title)
    ax1.set_xticks(index + bar_width / 12)
    ax1.set_xticklabels(labelstuff, rotation='vertical')
    ax1.legend()


    ####################################
    #Plot 2 Micro scale
    
    #have to make new lists because matplotlib doesn't like list slice as argument
    # this is so we can see the ones that are a little closer in scale
    bstAvgList2 = list()
    heapAvgList2 = list()
    quickAvgList2 = list()
    labelstuff2 = list()
    closeraces = (0,1,2,3,6) #graphs that are close so we want to see them in scale
    
    for i in closeraces:
         #hard code this for simplicity. This could be cleaner.  we want to just see the ones that are close. 
            bstAvgList2.append(bstAvgList[i])
            heapAvgList2.append(heapAvgList[i])
            quickAvgList2.append(quickAvgList[i])
            labelstuff2.append(labelstuff[i])


    index2 = np.arange(5)      
    bar_width2 = 0.30  # the width of the bars
    title = 'Close up of the shorter searches'
    
    ax2.bar(index2 - bar_width2 / 2, bstAvgList2, bar_width2, color='b',
               label='BST')
    ax2.bar(index2 + bar_width2 / 2, heapAvgList2, bar_width2, color='r',
               label='heap')
    ax2.bar(index2 + 1.5 * bar_width2, quickAvgList2, bar_width2, color='g',
               label='quick')

    ax2.set_xlabel('Files')
    ax2.set_ylabel('Time')
    ax2.set_title(title)
    ax2.set_xticks(index2 + bar_width2 / 5)
    ax2.set_xticklabels(labelstuff2, rotation='vertical')
    ax2.legend()

    fig.tight_layout()

    plt.show()

    #print raw data
    print("For {} iterations:".format(iterations))
    for i in range(0,12):
        print(labelstuff[i])
        print("   BST Insert average: {}".format(round(bstAvgList[i],3)))
        print("   Heap sort average: {}".format(round(heapAvgList[i], 3)))
        print("   Quick sort average: {}".format(round(quickAvgList[i],3)))
        print("------------------------------------")






                              
if __name__ == "__main__":
    main()
