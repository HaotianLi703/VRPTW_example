import math
import re

class Data:
    def __init__(self, customerNum = 0):
        self.customerNum = customerNum
        self.nodeNum = self.customerNum + 2
        self.vehicleNum = 0
        self.capacity = 0
        self.cor_X = []
        self.cor_Y = []
        self.demand = []
        self.serviceTime = []
        self.readyTime = []
        self.dueTime = []
        self.disMatrix = [[]]

    def readData(self, path):

        with open(path, 'r') as f:
            lines = f.readlines()

        cnt = 0
        # read the info
        for line in lines:
            cnt += 1
            if cnt == 5:
                # [:-1]， 最后一个是-1
                line = line[:-1]
                # " +"表示若干个空格
                str = re.split(" +", line)
                str = [temp_str for temp_str in str if temp_str]
                self.vehicleNum = int(str[0])
                self.capacity = float(str[1])
            elif cnt >= 10 and cnt <= 10 + self.customerNum:
                line = line[:-1]
                str = re.split(" +", line)
                str = [temp_str for temp_str in str if temp_str]
                self.cor_X.append(float(str[1]))
                self.cor_Y.append(float(str[2]))
                self.demand.append(float(str[3]))
                self.readyTime.append(float(str[4]))
                self.dueTime.append(float(str[5]))
                self.serviceTime.append(float(str[6]))

        self.cor_X.append(self.cor_X[0])
        self.cor_Y.append(self.cor_Y[0])
        self.demand.append(self.demand[0])
        self.readyTime.append(self.readyTime[0])
        self.dueTime.append(self.dueTime[0])
        self.serviceTime.append(self.serviceTime[0])

        # compute the distance matrix
        self.disMatrix = [[0 for i in range(self.nodeNum)] for g in range(self.nodeNum)]
        for i in range(0, self.nodeNum):
            for j in range(0, self.nodeNum):
                temp = (self.cor_X[i] - self.cor_X[j])**2 + (self.cor_Y[i] - self.cor_Y[j])**2
                self.disMatrix[i][j] = math.sqrt(temp)

        return None