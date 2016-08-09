import numpy as np
import cv2
from itertools import groupby
from operator import itemgetter
from matplotlib import pyplot as plt
from words_to_line import recog_words_on_line

#check, do we have to swap contours
def checkSwapCond(a,b,lines):
    #if ((b[0]+b[2]/2) < (a[0]+a[2]/2)) and ((b[1]+b[3]/2) - (a[1]+a[3]/2) < (b[3] + a[3])/6):
    #    return 1
    a0 = a[0]+a[2]/2
    b0 = b[0]+b[2]/2
    a1 = a[1]+a[3]/2
    b1 = b[1]+b[3]/2
    #get line that contains first rect

    if (a1 >= lines[len(lines)-1]):
        # swap if lineA > lineB
        if (b1 < lines[len(lines)-1]):
            return 1
        # swap if A and B in same line and b is to the left
        if (b1 >= lines[len(lines)-1]) and a0 > b0:
            return 1
        return 0
    for i in xrange(len(lines)-1):
        if (a1 >= lines[i]) and (a1 <= lines[i+1]):
            # swap if lineA > lineB
            if (b1 < lines[i]):
                return 1
            # swap if A and B in same line and b is to the left
            if (b1 >= lines[i]) and (b1 < lines[i + 1]) and a0 > b0:
                return 1
            return 0
    return 0

#return line number for a letter
def lineNumber(a,lines):
    a1 = a[1]+a[3]/2
    if a1<lines[0]:
        return 0
    for i in reversed(xrange(len(lines))):
        if (a1 >= lines[i]):
            return i + 1

#check, are rectangles close enough to merge them
def needToMerge(a,b):
    if a[0] == 397 and b[0] == 427:
        W1 = distanceBetweenRectanglesX(a,b)
        W2 = min(a[2],b[2])
    if abs(distanceBetweenRectanglesX(a,b)) < min(a[2],b[2]):
        return True
    return False



#intersection of 2 rectangles
def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0:
        return 0
    else:
        return 1

def union(a, b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0] + a[2], b[0] + b[2]) - x
    h = max(a[1] + a[3], b[1] + b[3]) - y
    return (x, y, w, h)

def second_smallest(numbers):
    count = 0
    m1 = m2 = float('inf')
    for x in numbers:
        count += 1
        if x < m2:
            if x <= m1:
                m1, m2 = x, m1
            else:
                m2 = x
    return m2 if count >= 2 else None

def distanceBetweenRectanglesX(a,b):
    # determine, which rectangle is on the left
    if a[0] > (b[0] + b[2]):  # rectangle b is on the left
        return (a[0] - (b[0] + b[2]))
    else:
        return (b[0] - (a[0] + a[2]))

def distanceBetweenRectanglesY(a,b):
    return abs(a[1] + a[3] / 2 - b[1] - b[3] / 2)

def distanceBetweenRectangles(a,b):
    return distanceBetweenRectanglesX(a,b) + distanceBetweenRectanglesY(a,b)


def AcontainsB(a,b):
    #area of intersection
    # 1: a contains b
    # -1: b contains a
    # 0: no containment

    if a[0] > b[0] and a[1] > b[1] and a[0] + a[2] < b[0] + b[2] and a[1] + a[3] < b[1] + b[3]:
        return -1
    if a[0] < b[0] and a[1] < b[1] and a[0] + a[2] > b[0] + b[2] and a[1] + a[3] > b[1] + b[3]:
        return 1
    return 0
#this function deletes rectangles that have to big area or to small
def deleteSmallBig(rect):
    # counting a threshold value (in this case - mean/2 for too small and mean*8 for too big)
    normalHeight = 0
    normalArea = 0
    for i in xrange(len(rect)):
        normalHeight = normalHeight + rect[i][3]
        normalArea = normalArea + rect[i][2] * rect[i][3]
    normalHeight = (normalHeight / len(rect)) / 2
    normalArea = (normalArea / len(rect)) * 8
    # removing some of the rectangles
    for i in reversed(xrange(len(rect))):
        if rect[i][3] < normalHeight:
            del rect[i]
        else:
            if rect[i][2] * rect[i][3] > normalArea:
                del rect[i]
    return rect

#Sort rectangles, by lines and X coordinate (first by line, then by Xcoord in each line)
def sortRect(rect, separatingLines):
    i = 0
    while i < len(rect):
        j = i + 1
        #if second rectangle is in lower line or to the right against the first, swap them
        while j<len(rect):
            if checkSwapCond(rect[i], rect[j], separatingLines):
                tmp = rect[j]
                rect[j] = rect[i]
                rect[i] = tmp
            j = j + 1
        i = i + 1
    return rect

#draw rectangles and save result in file
def drawRect(im, words, name_of_file, colour):
    # drawing rectangles
    im = cv2.merge((im, im, im))
    for i in xrange(len(words)):
        cv2.rectangle(im, (words[i][0], words[i][1]), (words[i][0] + words[i][2], words[i][1] + words[i][3]),
                      colour, 1)
        # cv2.putText(im, str(i), (rect[i][0], rect[i][1]+ rect[i][3]), cv2.FONT_ITALIC, 1, 255)
    # show
    #cv2.imshow('image', im)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cv2.imwrite(name_of_file, im)

def mergeRectangles(rect, rectLines):
    # rectWordNumber contains information about which word contains specific letter
    rectWordNumber = [-1 for i in xrange(len(rect))]

    # comparing all rectangles with each other
    # words list contains bounding rectangles of words
    words = []
    words.append(rect[0])
    # wordLines contains information about line that contains specific word rectangle
    wordLines = [rectLines[0]]
    rectWordNumber[0] = 0

    # check all letters
    for i in xrange(1, len(rect)):
        stance = True
        # compare letter number i with existing rectangles
        for j in xrange(len(words)):
            # add letter to a word if they are close enough
            if (wordLines[j] == rectLines[i]) and (needToMerge(words[j], rect[i])):
                words[j] = union(words[j], rect[i])
                rectWordNumber[i] = j
                stance = False
                break
        # if letter is not close enough to all words - create new word
        if stance:
            words.append(rect[i])
            wordLines.append(rectLines[i])
            rectWordNumber[i] = j + 1
    return rectWordNumber, words, wordLines, rectLines, rect

#function that removes rectangles, that are inside other rectangles
def removeInsRect(rect):
    i = 0
    while i < len(rect):
        j = i+1
        while j<len(rect):
            if AcontainsB(rect[i],rect[j]) == 1:
                tmp = rect.pop(j)
                j = j - 1
            if AcontainsB(rect[i],rect[j]) == -1:
                tmp = rect.pop(i)
                #j = len(rect)
                i = i - 1
                break
            j = j + 1
        i = i + 1
    return rect

# !!!!!!! smart compution of windowsize
def findLines(im, windowSize):
    ###Stage 0 - counting sum of pixels by lines
    width = np.size(im, 1)
    height = np.size(im, 0)

    # get sums by rows
    pixelsums = np.array(im.sum(1), dtype=float)

    """
    # convert 3 values for each dot into 1
    pixelsums1 = []
    for i in xrange(height):
        pixelsums1.append(pixelsums[i][1])
    pixelsums = pixelsums1
    """

    # norming values
    maxpixel = max(pixelsums)
    minpixel = min(pixelsums)
    for i in xrange(height):
        pixelsums[i] = (float(pixelsums[i] - minpixel) / float(maxpixel))

    # calculating mean
    mean = np.mean(pixelsums)

    # Grisha approach
    # counting threshold for windows of fixed size
    # Std(buffer, size)*(0.3936f + 0.1829f*log((float)size));
    linesToPrint = []

    i = 0
    while i < (len(pixelsums) - windowSize - 1):
        # copying windows
        buffer = pixelsums[i:(windowSize + i)]
        # finding thresholds
        threshStd = np.std(buffer) * (0.3936 + 0.1829 * np.log(windowSize)) + np.mean(buffer)
        # comparing lines with thresholds
        for j in xrange(windowSize):
            if pixelsums[i + j] > threshStd:
                linesToPrint.append(i + j)
        i = i + windowSize + 1

    # saving central lines of groups
    separatingLines = []
    for k, g in groupby(enumerate(linesToPrint), lambda (i, x): i - x):
        separatingLines.append(int(round(np.mean(map(itemgetter(1), g)))))
    return separatingLines







def findwords(im):
    #convert to grayscale

    #imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    imgray = im

    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    #detecting contours
    contours, im2 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    words = []
    if contours:
        separatingLines = findLines(im, 15)

        ###Stage 1 - drawing rectangles that correspond to contours
        #finding rectangles, that contain contours
        rect = []
        for i in xrange(len(contours)):
            a = cv2.boundingRect(contours[i])
            rect.append(a)

        ###Stage 2 - deleting too small and too big rectangles
        rect = deleteSmallBig(rect)

        ###Stage 3 - removing rectangles that are inside other rectangles
        rect = removeInsRect(rect)

        ###Stage 4 - sorting rectangles
        rect = sortRect(rect, separatingLines)

        ###Stage 5 - finding line numbers
        #rectLines contains information about line that contains specific letter rectangle
        rectLines = [lineNumber(rect[i], separatingLines) for i in xrange(len(rect))]

        ###Stage 6 - merging rectangles into words
        rectWordNumber, words, wordLines, rectLines, rect = mergeRectangles(rect, rectLines)
        word_lists_per_line = recog_words_on_line(words, wordLines, im)

    return words, word_lists_per_line


if __name__ == '__main__':
    words = findwords('binarized3.png')
    im = cv2.imread('binarized3.png')
    drawRect(im, words, "contours_after_after.png", (255, 0, 0))