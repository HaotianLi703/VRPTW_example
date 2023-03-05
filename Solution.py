class Solution:
    def __init__(self, data):
        self.X = [[[0 for k in range(data.vehicleNum)] for j in range(data.nodeNum)] for i in range(data.nodeNum)]
        self.S = [[0 for k in range(data.vehicleNum)] for i in range(data.nodeNum)]
        self.route = []
        self.vehicleNum = data.vehicleNum
        self.nodeNum = data.nodeNum

    def get_route(self):
        for k in range(self.vehicleNum):
            i = 0
            subRoute = []
            subRoute.append(i)
            finish_flag = False
            while not finish_flag:
                for j in range(1, self.nodeNum):
                    if self.X[i][j][k] > 0:
                        subRoute.append(j)
                        i = j
                        if j == self.nodeNum - 1:
                            finish_flag = True
            if len(subRoute) > 2:
                self.route.append(subRoute)
        i = 1
        for temp_route in self.route:
            temp_str = 'Route %s : %s' % (i, temp_route)
            print(temp_str)
            i += 1