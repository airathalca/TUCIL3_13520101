from queue import PriorityQueue
import numpy as np

final = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]])

class Puzzle:
    def __init__(self, matrix = np.copy(final), empty_x = 3, empty_y = 3, cost = 0, level = 0, parent = None, path = None):
        self.matrix = np.copy(matrix)
        self.empty_x = empty_x
        self.empty_y = empty_y
        self.cost = cost
        self.level = level
        self.parent = parent
        self.path = path

    def __lt__(self, other):
        if (self.cost + self.level == other.cost + other.level):
            return self.cost <= other.cost
        return self.cost + self.level < other.cost + other.level

    def Cost(self):
        result = 0
        for i in range(4):
            for j in range(4):
                current = self.matrix[i][j]
                if(current != 16 and current != final[i][j]):
                    result += 1
        return result

    def findNumber(self, number):
        ans = [-1,-1]
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == number:
                    ans = [i,j]
        return ans

    #calculate Kurang(i)
    def Kurang(self, number):
        if(number == 16):
            location = [self.empty_x,self.empty_y]
        else:
            location = self.findNumber(number)
        res = 0
        for i in range(location[0]*4+location[1]+1,16):
            if self.matrix[i//4][i%4] < self.matrix[location[0]][location[1]]:
                res += 1
        return res
    
    #calculate sigma Kurang(i) + X to
    def KurangTotal(self):
        res = 0
        for i in range(1,17):
            res += self.Kurang(i)
        if (self.empty_x + self.empty_y) % 2 != 0:
            res += 1
        return res

    #function to check if matrix solveable or not
    def Cek(self):
        return (self.KurangTotal() % 2 == 0)
    
    #check if matrix valid (contain all number from 1...16 exactly once)
    def Valid(self):
        countInput = [0 for i in range(17)]
        for i in range(4):
            for j in range(4):
                if (self.matrix[i][j] > 16 or self.matrix[i][j] <= 0):
                    return False
                else :
                    countInput[self.matrix[i][j]] += 1
        for i in range(1,17):
            if (countInput[i] != 1):
                return False
        return True
    
    #function to read the input from file and move it to attribute matrix
    def readFile(self, file):
        try:
            f = open(file, "r")
            for i in range(4):
                temp = f.readline()
                self.matrix[i] = temp.split()
                for j in range(4):
                    self.matrix[i][j] = int(self.matrix[i][j])
                    if (self.matrix[i][j] == 16):
                        self.empty_x = i
                        self.empty_y = j
            self.matrix = np.array(self.matrix)
            self.cost = self.Cost()
        except:
            pass
    
    #function to read the input from console and move it to attribute matrix
    def inputCommand(self, input):
        try:
            inputmatrix = []
            inputmatrix = input.split()
            for i in range(16):
                self.matrix[i//4][i%4] = int(inputmatrix[i])
                if (self.matrix[i//4][i%4] == 16):
                        self.empty_x = i//4
                        self.empty_y = i%4
            self.matrix = np.array(self.matrix)
            self.cost = self.Cost()
        except:
            pass
        
    #function to move the puzzle
    def Move(self, x, y):
        self.matrix[self.empty_x][self.empty_y], self.matrix[self.empty_x+x][self.empty_y+y] = self.matrix[self.empty_x+x][self.empty_y+y], self.matrix[self.empty_x][self.empty_y] 
        self.empty_x += x
        self.empty_y += y

    #function to generate new Puzzle (child) and calculate the cost
    def MakeChild(self, move_x, move_y, path):
        child = Puzzle(self.matrix, self.empty_x, self.empty_y, self.cost, self.level + 1, self, path)
        if(child.matrix[child.empty_x + move_x][child.empty_y + move_y] == (child.empty_x + move_x) * 4 + child.empty_y + move_y + 1):
            child.cost += 1
        elif(child.matrix[child.empty_x + move_x][child.empty_y + move_y] == (child.empty_x) * 4 + child.empty_y + 1):
            child.cost -= 1
        child.Move(move_x, move_y)
        return child

    def Up(self):
        if(self.empty_x - 1 >= 0):
            return self.MakeChild(-1,0,"Up")
        return None

    def Down(self):
        if(self.empty_x + 1 < 4):
            return self.MakeChild(1,0,"Down")
        return None
    
    def Left(self):
        if(self.empty_y - 1 >= 0):
            return self.MakeChild(0,-1,"Left")
        return None
    
    def Right(self):
        if(self.empty_y + 1 < 4):
            return self.MakeChild(0,1,"Right")
        return None

def printMatrix(matrix):
    print("|-------|-------|-------|-------|")
    for i in range(4): 
        print("|", end = " ")
        for j in range(4): 
            if(matrix[i][j] != 16):
                print(" ",matrix[i][j],"\t|", end = " ") 
            else:
                print("  \t|", end = " ")
        print() 
        print("|-------|-------|-------|-------|")

def newNode(child, Visited, bangkit, Q):
    #check if child node already visited, if visited, dont enqueue to PrioQueue
    matrix_hash = child.matrix.tobytes()
    if(not matrix_hash in Visited):
        bangkit += 1
        Visited[matrix_hash] = 1
        Q.put(child)
    return Visited, bangkit, Q

#function to solve puzzle using Branch and Bound
def SolvePuzzle(root, iterationnumber):
    for i in range(1,16):
        print(f"Kurang({i}) = {root.Kurang(i)}\n")
    print(f"Nilai dari sum_{1}^{16} kurang(i)+X adalah = {root.KurangTotal()}\n")
    Visited = {} #to check if node is already visited
    Q = PriorityQueue()
    iterationnumber = 1
    matrix_hash = root.matrix.tobytes() 
    Visited[matrix_hash] = 1
    Q.put(root)
    while (not(Q.empty())): #while Queue still has node to check, dequeue from the queue
        now = Q.get()
        if (np.array_equal(final, now.matrix)): #if node now equal goal node, finish the algorithm
            print("Jumlah node yang dibangkitkan adalah = ", iterationnumber)
            return now, iterationnumber
            break
        else:
            childUp = now.Up() #generate all child possible from node now
            childDown = now.Down()
            childLeft = now.Left()
            childRight = now.Right()
            if (childUp != None): 
                Visited, iterationnumber, Q = newNode(childUp, Visited, iterationnumber, Q)
            if (childDown != None):
                Visited, iterationnumber, Q = newNode(childDown, Visited, iterationnumber, Q)
            if (childLeft != None):
                Visited, iterationnumber, Q = newNode(childLeft, Visited, iterationnumber, Q)
            if (childRight != None):
                Visited, iterationnumber, Q = newNode(childRight, Visited, iterationnumber, Q)