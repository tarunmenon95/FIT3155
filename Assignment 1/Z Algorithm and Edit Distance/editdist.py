import sys
from time import sleep

txt = ""
pat = ""



def zalg(text):
    n = len(text)

    zValues = [0] * n
    zValues[0] = -1

    leftPointer = -1
    rightPointer = -1

    # Skip 0th index as it is omitted in alg
    for i in range(1, n):

        kPointer = i
        textPointerOne = 0
        textPointerTwo = i
        zValue = 0

        # Case 2 -- Within Z-Box

        if kPointer <= rightPointer:

            #Case 2a - Prefix of box

            if zValues[kPointer - leftPointer] < rightPointer - kPointer + 1:

                zValues[kPointer] = zValues[kPointer - leftPointer]


            #Case 2b - Box+

            else:

                textPointerOne = rightPointer - kPointer + 1

                textPointerTwo = rightPointer + 1

                while (textPointerTwo < n) and (text[textPointerOne] == text[textPointerTwo]):
                    textPointerOne += 1

                    textPointerTwo += 1

                zValues[i] = textPointerTwo - kPointer

                rightPointer = textPointerTwo - 1

                leftPointer = kPointer

        # Case 1 -- Outside Z-Box

        if kPointer > rightPointer:

            while (textPointerTwo < n) and (text[textPointerOne] == text[textPointerTwo]):
                textPointerOne += 1
                textPointerTwo += 1
                zValue += 1
            zValues[i] = zValue

            if zValue > 0:

                rightPointer = textPointerTwo - 1
                leftPointer = kPointer


    return zValues

def readFiles():
    global txt, pat
    txtfile = sys.argv[1]
    patfile = sys.argv[2]

    t = open(txtfile, "r")
    p = open(patfile, "r")

    for i in t:
        txt = txt + i

    for k in p:
        pat = pat + k

    t.close()
    p.close()


def editdist():
    # run z alg for abcd , then all 3 letter variants > abc , abc, bcd. Then mabe finally ab?cd
    readFiles()
    distance = len(pat)
    listOfPhrases = [pat]
    outputArr = []

    #List of patterns of length n(for edit distance 0) and n-1 (for edit distance 1)
    for i in range(len(pat)):
        phrase = pat[:i] + pat[(i+1):]
        listOfPhrases.append(phrase)

    #Run Z alg on all patterns
    for i in listOfPhrases:

        zArr = zalg(i+txt)

        for k in range(len(zArr)):
            #0 Edit Distance
            if zArr[k] == distance:
                outputArr.append([k - distance,0])
            #1 Edit Distance
            if zArr[k] == distance - 1:
                outputArr.append([k - distance+1,1])

    returnArray = []

    #Remove redundant matches
    if outputArr[0][1] == 0:
        location = outputArr[0][0]
        returnArray.append(outputArr[0])
        for i in range(1,len(outputArr)-1):
            if outputArr[i][0] >= location - 1 and outputArr[i][0] <= location + 1:
                pass
            else:
                returnArray.append(outputArr[i])

    returnArray = sorted(returnArray, key=lambda x: x[0])

    #Write results
    out = open("output_editdist.txt", 'w')

    for i in returnArray:
        out.write(str(i[0]) + "  " + str(i[1]) + '\n')



editdist()
