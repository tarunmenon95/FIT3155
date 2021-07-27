import random
import math
import sys

"""
Tarun Menon 29739861
"""


#Dictionary for non-retry optimisation
attempted = {}

#Convert int to binary form
def intToBinary(num):
    return "{0:b}".format(num)


def repeatedSquare(a,s,t,n):
    """
    repeatedSquare function builds sequence <x0 ... xs> on which we test for primality
    :param a: The chosen witness
    :param s: S value from (n-1) -> 2^s*t form
    :param t: T value from (n-1) -> 2^s*t form
    :param n: The number we are checking for primality
    :return: A list containing our built sequence
    """
    sequence = []
    binrep = str(intToBinary(int(t)))
    result = 1

    #Get first term in sequence
    for i in range(len(binrep) -1, -1, -1):

        # a^(2^0)*t % n - Initial
        if i == len(binrep) -1:
            curTerm = int(a % n)

        #Repeated Squaring
        else:
            curTerm = ((curTerm % n) * (curTerm % n)) % n

        #Build result on "1"
        if binrep[i] == "1":
            result = (result * curTerm) % n

    #Add x^0 to sequence
    sequence.append(int(result))

    #Repeated square remaining terms
    for j in range(s):
        nextTerm = ((sequence[j] % n)*(sequence[j] % n)) % n
        sequence.append(nextTerm)

    #Return sequence
    return sequence


def millerrabin(n, iteration):
    """
    Miller rabin function which checks built sequence from repeatedSquaring function over set iterations
    and validates whether n is prime
    :param n: Number we are checking for primality
    :param iteration: Number of iterations we are looping
    :return: Boolean whether n is prime
    """
    #Check if prime
    if n%2 ==0:
       return False


   # (n-1) -> 2^s*t form
    s = 0
    t = n-1

    while(t%2 == 0):
        s = s+1
        t = t//2


    #Run for set iterations
    for i in range(iteration):
        #Select witness
        witness = random.randint(2,n-2)
        seq = repeatedSquare(witness,s,t,n)

        #Fermat
        if seq[-1] != 1:
            return False

        #Check sequence
        for j in range(1,len(seq)):
            if (seq[j] == 1):
                if seq[j-1] == 1:
                    pass
                elif seq[j-1] == n-1:
                    pass
                else:
                    return False

    return True

def twinprime():
    """
    Function twinprime calls miller rabin over a random integer in a range set by sys arg user input. When a prime
    is found in the range, we then check 2 integers higher and lower for a "twin prime". Repeat unit twin prime is found
    :return: Output twin prime numbers to output file
    """
    file = open("output_twin_prime.txt", "w")

    m = int(sys.argv[1])
    isTwin = False

    #Generate random number of m bits length
    rangeStart = int(math.pow(2,m-1))
    rangeEnd = int(math.pow(2,m) -1)

    #Run until twin prime is found
    while isTwin != True:
        newNumber = False

        #Optimisation to not retry old attempted numbers
        while newNumber is False:
            randomNumber = random.randint(rangeStart, rangeEnd)
            if randomNumber in attempted:
                pass
            else:
                newNumber = True

        #Check randomNumber for primality
        result = millerrabin(randomNumber, 100)

        #Add attempted number to dict
        attempted[randomNumber] = "Yes"

        # If n is prime
        if result == True:

            #Check for twin prime
            lowerNum = randomNumber - 2
            upperNum = randomNumber + 2
            lowerNeighbor = millerrabin(lowerNum, 100)
            upperNeighbor = millerrabin(upperNum, 100)

            #Check up for twin prime in upper neighbour
            if upperNeighbor == True:
                print(randomNumber, randomNumber+2)
                file.write(str(randomNumber) + '\n')
                file.write(str(randomNumber+2))
                isTwin = True
                return

            #Check down for twin prime in lower neighbour
            if lowerNeighbor == True:
                print(randomNumber-2, randomNumber)
                file.write(str(randomNumber-2) + '\n')
                file.write(str(randomNumber))
                isTwin = True
                return

twinprime()