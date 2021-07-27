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

class node:
    """
    Node class for huffman character in tree representation
    """
    def __init__(self, name, count, leftChild, rightChild):
        self.name = name
        self.count = count
        self.leftChild = leftChild
        self.rightChild = rightChild

codewords = []
currentCodeWord = ""

def huffman(inputString):
    """
    Function huffman takes in an input string and creates a list containing a character and its designated code word
    based on frequency of the character
    :param inputString: String to encode characters
    :return: List of encoded characters
    """

    #Get frequencies of characters in string
    characterArray = []
    frequencyArray = []

    for i in inputString:
        if i not in characterArray:
            characterArray.append(i)
            frequencyArray.append([i,1])
        else:
            for k in frequencyArray:
                if k[0] == i:
                    k[1] = k[1] + 1
                    break

    frequencyArray.sort(key = lambda x: x[1])

    #Make nodes
    freqNodeArray = []
    for i in frequencyArray:
        newNode = node(i[0],i[1],None,None)
        freqNodeArray.append(newNode)

    #Make tree with frequency array
    while(len(freqNodeArray) > 1):

        #Get 2 lowest frequent nodes
        firstNode = freqNodeArray[0]
        secondNode = freqNodeArray[1]

        #Merge
        mergeName = firstNode.name + secondNode.name
        mergeCount = firstNode.count + secondNode.count
        mergeNode = node(mergeName,mergeCount,firstNode,secondNode)

        freqNodeArray.remove(firstNode)
        freqNodeArray.remove(secondNode)
        freqNodeArray.append(mergeNode)
        freqNodeArray.sort(key=lambda x: x.count)

    finalTree = freqNodeArray[0]

    traverseStart(finalTree)
    returnArray = codewords

    #Return codewords
    return returnArray


def traverse(aNode, visited):
    """
    Function to traverse huffman tree and create codewords
    :param aNode: Current node
    :param visited: Set of visited nodes
    """
    global currentCodeWord

    #Traverse children creating code words depending on left/right traversal direction
    if aNode.leftChild != None:
        currentCodeWord += "0"
        visited.add(aNode.leftChild)
        traverse(aNode.leftChild,visited)
    else:
        codewords.append([aNode.name,currentCodeWord])
        currentCodeWord = currentCodeWord[0:len(currentCodeWord)-1]
        return

    if aNode.rightChild != None:
        visited.add(aNode.rightChild)
        currentCodeWord += "1"
        traverse(aNode.rightChild,visited)
    else:
        codewords.append([aNode.name, currentCodeWord])
        currentCodeWord = currentCodeWord[0:len(currentCodeWord) - 1]
        return

    if(aNode.leftChild in visited and aNode.rightChild in visited):
        currentCodeWord = currentCodeWord[0:len(currentCodeWord) - 1]

def traverseStart(aNode):
    visited = set()
    traverse(aNode, visited)

def intToBinary(num):
    return "{0:b}".format(num)

def elias(aNum):
    """
    Function to encode input number into elias encoding
    :param aNum: Input number to encode
    :return: Elias encoded number
    """

    #Binary Representation
    binarynum = intToBinary(aNum)

    lengthComponents = []

    curLength = len(binarynum) - 1

    #Base case of 0 len
    if curLength == 0:
        return "1"

    while curLength > 0:
        #Get binary representation
        binaryLength = intToBinary(curLength)
        #Flip first bit
        binaryLength = "0" + binaryLength[1:]

        lengthComponents.append(binaryLength)

        curLength = len(binaryLength) - 1


    eliasOutput = ""
    lengthComponents.reverse()
    for i in lengthComponents:
        eliasOutput += i

    eliasOutput += binarynum

    return eliasOutput

def createHeader():
    """
    Function createHeader uses huffman and elias encoding to transform a string from a file
    into an encoded number and outputs to another file
    """
    #Read sys arg
    inputString = readWord()

    #Get huffman encoded chars of input word
    huffmanCharacters = huffman(inputString)

    huffmanCharacters.sort(key=lambda x: x[0])

    #Get number of unique chars
    uniqueChars = len(huffmanCharacters)

    #Encode unique chars with elias
    eliasLength = elias(uniqueChars)

    #Add to header
    headerOutputString = eliasLength

    #Add each encoded char/ascii/length to header
    for i in huffmanCharacters:
        headerOutputString += intToBinary(ord(i[0]))
        headerOutputString += elias(len(i[1]))
        headerOutputString += i[1]

    file = open("output_header.txt", "w")
    file.write(headerOutputString)
    file.close()


createHeader()


