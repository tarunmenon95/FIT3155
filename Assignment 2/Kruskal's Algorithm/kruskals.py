import sys


def readFileEdges():
    """
    Function to read input file and return list of edge objects
    :return: A list of edge objects
    """
    edges = []
    txtfile = sys.argv[2]
    t = open(txtfile, "r")

    for i in t:
        vals = i.split()
        edge1 = vals[0]
        edge2 = vals[1]
        weight = vals[2]
        newEdge = edge(edge1,edge2,weight)
        edges.append(newEdge)

    return edges


class edge:
    """
    Simple edge class to create edge object in form [vertex1,vertex2,weight]
    """
    def __init__(self, edgeFrom, edgeToo, weight):
        self.edgeFrom = int(edgeFrom)
        self.edgeToo = int(edgeToo)
        self.weight = int(weight)


    def __str__(self):
        return (str(self.edgeFrom) + " " + str(self.edgeToo) + " " + str(self.weight))


class graph:

    def __init__(self):
        """
        Init function reads first terminal value as total vertices, next calls
        readFileEdges function to create list of all edged
        """
        self.vertices = int(sys.argv[1])
        self.edges = readFileEdges()
        pass

    def __str__(self):
        print(self.vertices)
        for i in self.edges:
            print(i)
        return ""


    def find(self, parentArray, vertexId):
        """
        Function find recursivly calls until it finds the parent of a given vertex
        :param parentArray: Parent array containing the parents of a vertex
        :param vertexId: Vertex id array
        :return: The parent vertex id
        """

        if parentArray[vertexId] == vertexId:
            return vertexId
        else:
            return self.find(parentArray, parentArray[vertexId])

    def union(self,vertex1,vertex2,parentArray):
        """
        Function union checks whether two vertices exist in same set, if not we combine
        the sets by changing the value one parent to point to the other
        :param vertex1: First vertex in the edge
        :param vertex2: Second vertex in the edge
        :param parentArray: Parent array
        """
        if self.find(parentArray,vertex1) != self.find(parentArray,vertex2):
            v1Parent = self.find(parentArray,vertex1)
            v2Parent = self.find(parentArray, vertex2)
            parentArray[v1Parent] = v2Parent


    def kruskal(self):
        #init mst
        self.mst = []
        mstweight = 0

        # unionfind datastructure base
        vertexID = [0] * self.vertices
        parent = [0] * self.vertices

        #init ids / parents
        for i in range(self.vertices):
            vertexID[i] = i
            parent[i] = i

        #sort graph by edge weights
        self.edges.sort(key=lambda edge : edge.weight)


        #add edges aslong as no cycle is created from lowest weight up
        for i in self.edges:
            if self.find(parent,i.edgeFrom) != self.find(parent, i.edgeToo):
                self.union(i.edgeFrom,i.edgeToo,parent)
                self.mst.append(i)


        #output mst to output file
        file = open("output_kruskals.txt", "w")

        #get mst total weight
        for i in self.mst:
            mstweight += i.weight

        file.write(str(mstweight) + '\n')

        for i in self.mst:
            file.write(str(i.edgeFrom) + " " + str(i.edgeToo) + " " + str(i.weight) + '\n')

        file.close()

g = graph()
g.kruskal()