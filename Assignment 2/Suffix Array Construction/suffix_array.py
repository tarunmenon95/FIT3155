import sys

def readWord():
    """
    Function to read input file and return word
    """
    txtfile = sys.argv[1]
    t = open(txtfile, "r")

    #Add dollar $
    out = t.readline()
    out += '$'

    return out

#Global list variable for implicit rule 1 extension
globalEnd = [-1]
temp = readWord()

class suffixtree:
    """
    A class definining a suffix tree data structure. This contains the core logic and functionallity
    where we utilise Ukkonen's algorithm, Depth First Search to create a suffix tree and from that,
    a suffix array.
    """


    def __init__(self, word):
        """
        Initialiser for a suffix tree, the tree simply begins with a single root node with no parent
        All other flags/arrays begin empty/at zero.
        """
        self.root = node(0,None)
        self.word = word
        self.lastj = 0
        self.showstopper = False
        self.rule2 = False
        self.rule3 = False
        self.retStr = ""
        self.outArr = []
        self.curWordLength = 0


    def searchPath(self,start,end,someNode):

        #The current suffix to insert
        currentSuffix = self.word[start:end]

        #Check current node for path, if not there, traverse correct neighbouring nodes until found
        while len(currentSuffix) != 0 and self.rule2 == False and self.rule3 == False:

            currentSuffix = currentSuffix[:-1]

            #Search neighbours
            for curnode in someNode.children:
                if self.word[curnode.start] == self.word[start]:


                    nodeStr = self.word[curnode.start:curnode.end[0]]
                    sufStr = self.word[start:end]
                    pos = 0

                    #If suffix path longer then current node suffix, traverse child node
                    if len(sufStr) > len(nodeStr):
                        someNode = curnode
                        self.searchPath(start + len(nodeStr),end,someNode)
                        break

                    #Check whether Rule 3 should occur (Suffix already exists)
                    for i in range(len(sufStr)):
                        if sufStr[i] == nodeStr[i]:
                            pos +=1
                            self.rule3 = True
                        else:
                            self.rule3 = False
                            break

                    #Rule 3
                    if self.rule3 == True:
                        self.showstopper = True
                        return

                    #Rule 2
                    else:
                        #Make Connecting Node
                        r2Node = node(curnode.start,curnode.parent)
                        r2Node.setEnd([r2Node.start + pos])
                        curnode.parent.children.append(r2Node)

                        #Make New Child Node
                        r2Node.addChild(start+pos,r2Node)

                        #Change old suffix node values and connect to new connecting node
                        curnode.start = curnode.start + pos
                        curnode.parent.children.remove(curnode)
                        curnode.parent = r2Node

                        r2Node.children.append(curnode)
                        self.rule2 = True

                        return



        #Rule 2 - Root Node
        if currentSuffix == '' and someNode.parent == None:
            someNode.addChild(start,self.root)
            self.rule2 = True

        #Rule 2 - Adding node from leaf
        elif self.rule3 == False and self.rule2 == False:
            someNode.addChild(start,someNode)
            self.rule2 = True

    def ukkonen(self):
        """
        Function utilising Ukkonnen's algorithm to populate our suffix tree with all suffixes
        from given string. Stored in index form to save on space.
        :return: The completed suffix tree
        """

        #Get input word
        word = self.word

        n = len(word)

        for i in range(n + 1):

            #Rule 1 - Implicit
            globalEnd[0] = globalEnd[0] + 1

            #Iterate from LastJ to i
            for j in range(self.lastj,i):

                #Define suffix bounds for the current phase
                suffixStart = j
                suffixEnd = i

                #Explicit Work - Rule 2 and 3
                self.searchPath(suffixStart,suffixEnd,self.root)

                #If rule 2 occured, change last j
                if self.rule2 == True:
                    self.lastj = j+1

                #Reset rule2 and 3 flags
                self.rule2 = False
                self.rule3 = False

                #If showstopper rule applies, end phase
                if self.showstopper == True:
                    self.showstopper = False
                    break

        return self

    def traverse(self, aNode, visited):
        """
        Function that traverses our suffix tree via DFS to retrieve suffixes.
        :param aNode: Node to search
        :param visited: Set containing already searched nodes
        """

        #Length of current word
        self.curWordLength = len(self.word[aNode.start:aNode.end[0]])

        #Concatenate output string
        if aNode.parent != None:
            self.retStr += self.word[aNode.start:aNode.end[0]]

        visited.add(aNode)

        #Search neighbouring nodes
        for i in aNode.children:
            if i not in visited:
                self.traverse(i,visited)

                #If end of tree, append to output array
                if len(i.children) == 0:
                    self.outArr.append(self.retStr)

                self.retStr = self.retStr[0:len(self.retStr) - self.curWordLength]
                self.curWordLength = len(self.word[aNode.start:aNode.end[0]])


    def depthfirstsearch(self,aNode):
        """
        Function to utilise DFS to navigate our completed suffix tree as to retrieve all
        suffixes for creation of our suffix array. This is the caller function to traverse
        which contains the the actual dfs.
        :param aNode: Node to search
        :return: List of suffixes
        """

        visited = set()

        self.traverse(aNode,visited)

        return self.outArr

class node:
    """
    A class defining a node data structure that is used to populate our suffix tree
    """

    def __init__(self,start,parent):
        """
        Initialiser of the node class
        :param start: Start index value from the text
        :param parent: Parent node of the child
        """
        self.children = []
        self.start = start
        self.end = globalEnd
        self.parent = parent

    def addChild(self,start, parent):
        """
        Function to add a child node to the suffix tree
        :param start: Start index value from the text
        :param parent: Parent node of the child
        """
        self.children.append(node(start,parent))

    def setEnd(self, val):
        """
        Function to statically define the end of a node (Instead of the global end)
        :param val: New end value of the node
        """
        self.end = val

    def delChild(self, someNode):
        """
        Function to delete a node
        :param someNode: Node to delete
        """
        self.children.remove(someNode)

    def output(self):
        """
        Function to output suffix tree to console
        """

        if self.parent != None:
            print(temp[self.start:self.end[0]])

        for i in self.children:
            i.output()




def outputSuffixArray(aSuffixTree):
    """
    :param a suffix tree to convert
    createSuffixArray function calls our ukkonen's algorithm function from our suffix tree class. It then
    takes the resultant suffixtree and uses a DFS traversal to navigate the suffix tree and return the suffixes
    which we use to create our final output suffix array which is output to the txt file.
    """

    #Create suffix tree then sort into a suffix list
    baseTree = aSuffixTree
    suffixTree = baseTree.ukkonen()
    unsortedArray = suffixTree.depthfirstsearch(suffixTree.root)
    lenSortedList = (sorted(unsortedArray, key=len))
    lenSortedList = lenSortedList[::-1]
    unsortedSufArray = []

    #Create indexed unsorted suffix array
    for i in range(len(lenSortedList)):
        unsortedSufArray.append([i,lenSortedList[i]])

    suffixTupleArray = sorted(unsortedSufArray, key=lambda suffixIndex: suffixIndex[1])
    suffixArray = []

    #Create suffix array
    for i in suffixTupleArray:
        suffixArray.append(i[0])
    print(suffixArray)

    file = open("output_suffix_array.txt", "w")

    for i in suffixArray:
        file.write(str(i) + '\n')

    file.close()


def createSuffixArray(aSuffixTree):
    """
    :param a suffix tree to convert
    Same as above function except used to return the suffix array instead of outputting
    to txt file. (For question 3)
    :return Returns the suffix array
    """

    #Create suffix tree then sort into a suffix list
    baseTree = aSuffixTree
    suffixTree = baseTree.ukkonen()
    unsortedArray = suffixTree.depthfirstsearch(suffixTree.root)
    lenSortedList = (sorted(unsortedArray, key=len))
    lenSortedList = lenSortedList[::-1]
    unsortedSufArray = []

    #Create indexed unsorted suffix array
    for i in range(len(lenSortedList)):
        unsortedSufArray.append([i,lenSortedList[i]])

    suffixTupleArray = sorted(unsortedSufArray, key=lambda suffixIndex: suffixIndex[1])
    suffixArray = []

    #Create suffix array
    for i in suffixTupleArray:
        suffixArray.append(i[0])
    print(suffixArray)

    for i in (suffixArray):
        print(suffixTree.word[i:globalEnd[0]])

    return suffixArray



def main():
    sTree = suffixtree(readWord())
    outputSuffixArray(sTree)

if __name__ == "__main__":
   main()
