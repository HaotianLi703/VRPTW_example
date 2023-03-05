from __future__ import print_function
from gurobipy import *
import re
from Data import Data
from Solution import Solution

if __name__ == '__main__':
    # 读取和初始化数据
    customerNum = 100
    data = Data(customerNum=customerNum)
    path = 'c101.txt'
    data.readData(path)

    # 建立模型
    bigM = 10000
    model = Model('VRPTW')
    # 创建变量 X_ijk
    X = [[[[] for k in range(data.vehicleNum)] for j in range(data.nodeNum)] for i in range(data.nodeNum)]

    # S_ik
    S = [[[] for k in range(data.vehicleNum)] for i in range(data.nodeNum)]

    for i in range(data.nodeNum):
        for k in range(data.vehicleNum):
            name1 = 's_' + str(i) + '_' + str(k)
            S[i][k] = model.addVar(lb=data.readyTime[i], ub=data.dueTime[i], vtype=GRB.CONTINUOUS, name=name1)
            for j in range(data.nodeNum):
                name2 = 'x_' + str(i) + '_' + str(j) + '_' + str(k)
                X[i][j][k] = model.addVar(vtype=GRB.BINARY, name=name2)

    # 添加约束
    # 创建目标函数
    obj = LinExpr()
    for i in range(data.nodeNum):
        for j in range(data.nodeNum):
            if i != j:
                for k in range(data.vehicleNum):
                    obj.addTerms(data.disMatrix[i][j], X[i][j][k])
    # 打印目标函数
    print(model.getObjective())
    # 将目标函数加入到模型中
    model.setObjective(obj, GRB.MINIMIZE)

    # 约束1
    for i in range(1, data.nodeNum-1):
        expr = LinExpr()
        for j in range(1, data.nodeNum):
            if i != j:
                for k in range(data.vehicleNum):
                    expr.addTerms(1, X[i][j][k])
        model.addConstr(expr == 1, "c1")
        expr.clear()

    # 约束2
    for k in range(data.vehicleNum):
        expr = LinExpr()
        for i in range(1, data.nodeNum-1):
            for j in range(1, data.nodeNum):
                if i != j:
                    expr.addTerms(data.demand[i], X[i][j][k])
        model.addConstr(expr <= data.capacity, 'c2')
        expr.clear()

    # 约束3
    for k in range(data.vehicleNum):
        expr = LinExpr()
        for j in range(1, data.nodeNum):
            expr.addTerms(1.0, X[0][j][k])
        model.addConstr(expr == 1.0, 'c3')
        expr.clear()

    # 约束4
    for k in range(data.vehicleNum):
        for h in range(1, data.nodeNum-1):
            expr1 = LinExpr()
            expr2 = LinExpr()
            for i in range(data.nodeNum-1):
                if h != i:
                    expr1.addTerms(1, X[i][h][k])
            for j in range(1, data.nodeNum):
                if h != j:
                    expr2.addTerms(1, X[h][j][k])

            model.addConstr(expr1 == expr2, 'c4')
            expr1.clear()
            expr2.clear()

    # 约束5
    for k in range(data.vehicleNum):
        expr = LinExpr()
        for i in range(data.nodeNum - 1):
            expr.addTerms(1, X[i][data.nodeNum - 1][k])
        model.addConstr(expr == 1, 'c5')
        expr.clear()

    # 约束6
    for k in range(data.vehicleNum):
        for i in range(data.nodeNum-1):
            for j in range(1, data.nodeNum):
                if i != j:
                    model.addConstr((S[i][k]) + data.disMatrix[i][j] - S[j][k] <= bigM - bigM * X[i][j][k], 'c6')

    # 求解问题
    model.write('a.lp')
    model.optimize()
    print("\n\n---optimal value---")
    print(model.ObjVal)

    # 打印结果
    # for m in model.getVars():
    #     if m.x == 1:
    #         print ("%s \t %d" % (m.varName, m.x))

    # get the optimal solution in matrix form
    solution = Solution(data)

    for m in model.getVars():
        temp_str = re.split(r'_', m.VarName)
        if temp_str[0] == 'x' and m.x == 1:
            solution.X[int(temp_str[1])][int(temp_str[2])][int(temp_str[3])] = m.x
        elif temp_str[0] == 's' and m.x == 1:
            solution.S[int(temp_str[1])][int(temp_str[2])] = m.x

    solution.get_route()

    # get the route of the vehicle

