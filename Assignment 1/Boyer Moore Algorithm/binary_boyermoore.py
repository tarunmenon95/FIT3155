import sys
from time import sleep

txt = ""
pat = ""


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


def bm():
    # Pre-Processing - O(n)

    readFiles()
    reversedPattern = pat[::-1]
    reversedZValues = zalg(reversedPattern)
    patArr = []
    txtArr = []

    # Create txt array - O(m)
    for i in txt:
        txtArr.append(int(i))

    # Create pattern array - O(n)
    for i in pat:
        patArr.append(int(i))

    # Get zSuffix values of reversed pat
    zSuffix = reversedZValues[::-1]
    goodSuffix = [0] * (len(pat) + 1)
    posArr = []

    # Position array delete later
    for i in range(0, len(pat) + 1):
        posArr.append(i)

    # Get good suffix values
    for i in range(0, len(pat) - 1):
        pos = len(pat) - zSuffix[i]
        goodSuffix[pos] = i

    matchPrefix = [0] * len(goodSuffix)

    zArr = zalg(pat)

    for i in range(len(patArr) - 1, 0, -1):
        if zArr[i] + i - 1 == len(patArr) - 1:
            matchPrefix[i] = zArr[i]
        else:
            matchPrefix[i] = matchPrefix[i + 1]

    matchPrefix[0] = len(pat)

    print('Position:', posArr)
    print('Pattern: ', patArr)
    print('zSuffix: ', zSuffix)
    print('GoodSfx: ', goodSuffix)
    print('MatchPfx:', matchPrefix)

    # Shifting
    txtEndPointer = len(pat) - 1
    end = len(txtArr) - 1
    matches = 0
    comps = 0
    out = open("output_binary_boyermoore.txt", "w")
    galStart = -100
    galEnd = -100

    while (txtEndPointer < end):

        matchOccured = False
        patRightPointer = len(pat) - 1
        txtRightPointer = txtEndPointer

        #     print('Text:    ',txtArr[txtEndPointer-len(pat)+1:txtEndPointer+1])
        #     print('Pattern: ', patArr)

        #Removed Bad Char shift as useless with Binary Language

        while (patArr[patRightPointer] == txtArr[txtRightPointer]):
            comps += 1
            # Galil Opt skip comps
            if patRightPointer == galEnd:
                if galStart == -1:
                    galStart = 0

                distance = galEnd - galStart + 1
                patRightPointer -= distance
                txtRightPointer -= distance
            else:
                patRightPointer -= 1
                txtRightPointer -= 1

            if patRightPointer == -1:
                matches += 1
                matchOccured = True
                sp = txtEndPointer - len(patArr) + 1
                out.write(str(sp) + '\n')
                break

        if matchOccured == False:

            # Case 1a - Good suffix Shift
            if goodSuffix[patRightPointer + 1] > 0:
                txtEndPointer += len(pat) - goodSuffix[patRightPointer + 1] - 1

                #Set zone for galil optimisation
                galStart = goodSuffix[patRightPointer + 1] - len(pat) + patRightPointer + 1
                galEnd = goodSuffix[patRightPointer + 1]

            # Case 1b Match Prefix Shift
            if goodSuffix[patRightPointer + 1] == 0:
                txtEndPointer += len(pat) - matchPrefix[patRightPointer + 1]

                #Set zone for galil optimisation
                galStart = 0
                galEnd = matchPrefix[patRightPointer + 1]

        # Case 2 - Match Prefix Shift on Matched Pattern
        if matchOccured == True:
            txtEndPointer += len(pat) - matchPrefix[1]

            #Null galil zone after match
            galStart = -10
            galEnd = -10

    print("Comparisons: ", comps)
    out.close()

bm()

