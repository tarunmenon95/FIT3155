import sys

"""
Tarun Menon 29739861
"""


def readWord():
    """
    Function to read input file and return word
    """

    txtfile = sys.argv[1]
    t = open(txtfile, "r")

    out = t.readline()
    return out

def eliasDecoder(codeword):
    """
    Function eliasDecoder takes in a binary string and returns a tuple containing the decoded word and its length
    :param codeword: Codeword to decode
    :return: Tuple containing decoded word and length of encoded form
    """

    found = False
    pos = 0
    readLength = 1
    totalLen = 0

    #Loop until significant bit is 1
    while not found:
        code = codeword[pos:pos + readLength]
        totalLen += len(code)

        sigBit = str(code[0])
        if sigBit == "1":
            return [code,totalLen]

        else:
            flipBitCode = "1" + code[1:]
            pos = pos + readLength
            readLength = int(flipBitCode, 2) + 1




def decode():
    """
    Function decode reads a string from a file and decodes the huffman/elias encoded string and outputs the
    decoded string to another file
    """

    #Read input
    inputString = readWord()

    #Decode Header

    #Get number of unique chars
    numUniqChar = int(eliasDecoder(inputString)[0],2)

    #Get length of binary rep of unique chars
    lenOfUniqCharString = int(eliasDecoder(inputString)[1])
    inputString = inputString[lenOfUniqCharString:]

    #Instatiate empty array for code words
    codewords = []

    for i in range(numUniqChar):

        #Get Ascii Code of Character, Then remove from input string
        uniqChar = chr(int(inputString[0:7],2))
        inputString = inputString[7:]

        #Decode Elias Length of code word
        lengthOfCodeword = int(eliasDecoder(inputString)[0], 2)
        lengthOfElias = int(eliasDecoder(inputString)[1])
        inputString = inputString[lengthOfElias:]

        #Append code word to codewords array
        codewords.append([uniqChar,inputString[0:lengthOfCodeword], lengthOfCodeword])
        inputString = inputString[lengthOfCodeword:]


    #Decode data

    #Get number of format fields
    numFormatFields = int(eliasDecoder(inputString)[0],2)
    lenFormatField =  int(eliasDecoder(inputString)[1])

    inputString = inputString[lenFormatField:]

    decodeString = ""

    #Loop through number of format fields
    for i in range(numFormatFields):

        #Format 1 - <1,char>
        if inputString[0] == "1":
            inputString = inputString[1:]

            #Find codeword then add to decoded string
            for j in codewords:
                currentCodeWord = inputString[0:j[2]]

                if currentCodeWord == j[1]:
                    decodeString += j[0]
                    inputString = inputString[len(j[1]):]
                    break

        #Format 0 - <0,offset,length>
        else:

            inputString = inputString[1:]

            #Get offset and length of
            offsetTuple = (eliasDecoder(inputString))
            offset = int(offsetTuple[0],2)
            offSetLength = int(offsetTuple[1])

            inputString = inputString[offSetLength:]

            #Get length and length of
            lengthTuple = (eliasDecoder(inputString))
            lengthSize = int(lengthTuple[0],2)
            lengthOfAbove = int(lengthTuple[1])

            inputString = inputString[lengthOfAbove:]

            #Decode by offset and length

            pos = len(decodeString)

            #Add to decode string
            while lengthSize != 0:

                charToAdd = decodeString[pos - offset]
                decodeString += charToAdd
                lengthSize -=1
                pos +=1


    file = open("output decoder_lzss.txt", "w")
    file.write(decodeString)
    file.close()

    print(decodeString)



decode()