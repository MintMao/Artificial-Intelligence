# -*- coding: utf-8 -*-
import sys
from numpy import *
import numpy as num
import copy
import random
import getopt
import os
import re
import time

information = {}
nodes = {}
cost = {}
demand = {}
nodes_amount = 0
initial_route = {}  # 用来存路径
initial_load = {}  # 用来存储每次出车的initial_load
initial_route_cost = {}  # 用来存储每次出车的cost
all_distance = {}
total_demand = 0
total_cost = 0
all_cost = 0
# start = 0
# remind_time = 0


def dijkstra():
    distance = {}  # 从起点到这一点的最小cost
    for index in range(1, nodes_amount+1):
        depot = index
        distance[index] = {}
        searched = {}  # 记录走过的点为1,没走过的为0
        unsearched = set()  # 遍历过的点的集合
        for i in range(1, nodes_amount+1):
            distance[index][i] = sys.maxint
            searched[i] = 0
            unsearched.add(i)
        # 原点的cost设为0
        distance[index][depot] = 0
        searched[depot] = 1
        unsearched.remove(depot)

        # 将原点的能走的点的前驱设为原点并将距离设为相应的cost
        for i in range(1, nodes_amount+1):
            if nodes[depot, i] == 1:
                distance[index][i] = cost[depot, i]
        # 算法主体
        while len(unsearched) > 0:
            # 找出没走过的节点距离最小的
            min_distance = sys.maxint
            min_node = 0  # 新的起点
            for i in range(1, nodes_amount+1):
                if distance[index][i] < min_distance and searched[i] == 0:
                    min_distance = distance[index][i]
                    min_node = i
            unsearched.remove(min_node)
            searched[min_node] = 1
            for i in range(1, nodes_amount+1):
                if nodes[min_node, i] == 1:
                    # 拓展边（min_node,node)，如果最短路径比原来的小就更新
                    if distance[index][i] > distance[index][min_node]+cost[min_node, i]:
                        distance[index][i] = distance[index][min_node]+cost[min_node, i]
    return distance


# 读入文件部分
def open_file(filename):
    f = open(filename, 'r')
    # 0-7是信息
    # 8 是 NODES COST DEMAND
    # 9- while not end 是节点信息
    index = 0
    global information   # 用来存 文件头信息
    global nodes
    global cost
    global demand
    global nodes_amount
    global total_demand
    global total_cost
    for line in f:
        if index < 8:
            key = line.split(' : ')[0]
            value = line.split(' : ')[1]
            information[key] = value
        elif index == 8:
            nodes_amount = int(information["VERTICES"])
            nodes = num.zeros((nodes_amount+1, nodes_amount+1))
            cost = num.zeros((nodes_amount+1, nodes_amount+1))
            demand = num.zeros((nodes_amount+1, nodes_amount+1))

        elif index > 8:
            if line != 'END':
                length = 0
                father_node = int(line.split('   ')[0])
                length = length+len(line.split('   ')[0])+3
                child_node = int(line.split('   ')[1])
                length = length + len(line.split('   ')[1])+3
                nodes_cost = int(line.split('   ')[2])
                length = length + len(line.split('   ')[3])
                cost[father_node, child_node] = nodes_cost
                cost[child_node, father_node] = nodes_cost
                nodes_demand = int((line[length:]).split('       ')[1])
                demand[father_node, child_node] = nodes_demand
                demand[child_node, father_node] = nodes_demand
                if nodes_demand > 0:
                    total_demand = total_demand+nodes_demand
                    total_cost = total_cost+nodes_cost
                nodes[father_node, child_node] = 1
                nodes[child_node, father_node] = 1
            else:
                break
        index = index+1
    return information, nodes, cost, demand


def path_scanning(start, remind_time, termination):
    global all_distance
    all_distance = dijkstra()
    free_edges = []
    global initial_route
    global initial_load
    for i in range(1, nodes.shape[0]):
        for j in range(i+1, nodes.shape[0]):
            if nodes[i, j] == 1 and demand[i, j] != 0:
                free_edges.append((i, j))
    capacity = int(information["CAPACITY"])

    ''' 
    copy all required arcs in a list
    '''
    free = copy.deepcopy(free_edges)
    global all_cost
    global initial_route_cost
    remain_demand = copy.deepcopy(total_demand)
    index = 0

    min_cost = sys.maxint
    min_route = {}
    while termination - remind_time > time.time() - start:
        free = copy.deepcopy(free_edges)
        all_cost = 0
        initial_route={}
        k = 0
        while len(free) > 0:
            depot = int(information["DEPOT"])
            initial = depot
            initial_load[k] = 0
            initial_route[k] = []
            initial_route[k].append(0)
            initial_route_cost[k] = 0
            alpha = 1.5
            u_optimal = (0, 1)
            while len(free) > 0:
                '''
                这里需要添加一个条件：
                当车子快要满了的时候，应该只能走到最近的地方了
                '''
                find = False
                if capacity - initial_load[k] > alpha * total_demand / len(free_edges):
                    edge_select = []
                    min_distance = sys.maxint
                    for i in range(0, len(free)):
                        u = free[i]
                        begin = u[0]
                        end = u[1]
                        # 起点到边的距离也就是起点到两个端点的距离，所以要判断一下哪个是端点
                        if all_distance[depot][begin] > all_distance[depot][end]:
                            begin = u[1]
                            end = u[0]
                        if initial_load[k] + demand[begin, end] <= capacity:
                            if all_distance[depot][begin] < min_distance:
                                u_optimal = u
                                min_distance = all_distance[depot][begin]
                                find = True
                            if all_distance[depot][begin] == min_distance:
                                find = True
                                random_number = random.randint(0, 4)
                                if random_number == 4:
                                    if initial_load[k] < capacity/2:
                                        random_number = 2
                                    else:
                                        random_number = 3
                                if random_number == 0:
                                    if remain_demand-demand[begin, end]>0 and remain_demand-demand[u_optimal[0], u_optimal[1]]>0:
                                        if float(cost[begin, end])/(remain_demand-demand[begin, end]) > float(cost[u_optimal[0], u_optimal[1]])/(remain_demand-demand[u_optimal[0], u_optimal[1]]):
                                           u_optimal = (begin, end)
                                if random_number == 1:
                                    if remain_demand - demand[begin, end] > 0 and remain_demand - demand[u_optimal[0], u_optimal[1]] > 0:
                                        if float(cost[begin, end])/(remain_demand-demand[begin, end]) < float(cost[u_optimal[0], u_optimal[1]])/(remain_demand-demand[u_optimal[0], u_optimal[1]]):
                                            u_optimal = (begin, end)
                                if random_number == 2:
                                    if all_distance[initial][begin] < all_distance[u_optimal[0]][u_optimal[1]]:
                                        u_optimal = (begin, end)
                                if random_number == 3:
                                    if all_distance[initial][begin] > all_distance[u_optimal[0]][u_optimal[1]]:
                                        u_optimal = (begin, end)
                    if find:
                        edge_select.append(u_optimal)
                else:
                    min_distance = sys.maxint
                    edge_select = []
                    for j in range(0, len(free)):
                        u = free[j]
                        begin = u[0]
                        end = u[1]
                        if all_distance[depot][begin] > all_distance[depot][end]:
                            begin = u[1]
                            end = u[0]
                        if all_distance[depot][begin] + cost[begin, end] + all_distance[end][initial] <= float(total_cost) / len(free_edges) + all_distance[initial][depot]:
                            if all_distance[depot][begin] <= min_distance and initial_load[k]+demand[begin,end]<capacity:
                                min_distance = all_distance[depot][begin]
                                u_optimal = u
                                find = True
                        # 起点到边的距离也就是起点到两个端点的距离，所以要判断一下哪个是端点
                        # if all_distance[depot][begin]+cost[begin, end]+all_distance[end][initial] <= float(total_cost)/len(free_edges)+all_distance[initial][depot]:
                    if find:
                        edge_select.append(u_optimal)
                if len(edge_select) > 0:
                    if len(edge_select) > 1:
                        # random.seed()
                        random_number = random.randint(0, len(edge_select)-1)
                    else:
                        random_number = 0
                    u_optimal = edge_select[random_number]
                    initial_route[k].append(u_optimal)
                    find = False
                    for i in range(0, len(free)):
                        if free[i] == u_optimal:
                            find = True
                    if find:
                        free.remove(u_optimal)
                    else:
                        free.remove((u_optimal[1], u_optimal[0]))
                    all_cost = all_cost + all_distance[depot][u_optimal[0]]+cost[u_optimal[0], u_optimal[1]]
                    remain_demand = remain_demand - demand[u_optimal[0], u_optimal[1]]
                    initial_route_cost[k] = initial_route_cost[k]+all_distance[depot][u_optimal[0]]+cost[u_optimal[0], u_optimal[1]]
                    initial_load[k] = initial_load[k] + demand[u_optimal[0], u_optimal[1]]
                    depot = u_optimal[1]
                    if len(free) == 0:
                        initial_route[k].append(0)
                else:
                    initial_route[k].append(0)
                    all_cost = all_cost + all_distance[initial][u_optimal[1]]
                    initial_route_cost[k] = initial_route_cost[k]+all_distance[initial][u_optimal[1]]
                    k = k+1
                    break
        index = index + 1
        if all_cost<min_cost:
            min_cost = all_cost
            all_cost = min_cost
            min_route = initial_route
            initial_route = min_route
    return min_cost, min_route


def command_line_reader(argv):
    try:
        if len(argv) != 5:
            raise getopt.GetoptError("The argument count should be 5, and now is {}.".format(len(argv)))

        file_name = argv[0]
        if not os.path.isfile(file_name):
            raise IOError("The carp instance file does not exist.")

        termination = ''
        seed = ''
        opts, args = getopt.getopt(argv[1:], "t:s:")
        for opt, arg in opts:
            if opt == '-t':
                termination = int(arg)
            elif opt == '-s':
                pattern = '^[0-9]+$'
                match = re.findall(pattern, arg)
                if len(match) != 0:
                    seed = long(arg)
                else:
                    seed = arg

        return file_name, termination, seed

    except getopt.GetoptError as err:
        print str(err)
        print 'The argument should be <carp instance file> -t <termination> -s <random seed>'
        sys.exit(2)
    except ValueError as err:
        print("Termination argument should be an integer.")
        print 'The argument should be <carp instance file> -t <termination> -s <random seed>'
        sys.exit(2)
    except IOError as err:
        print str(err)
        print 'The argument should be <carp instance file> -t <termination> -s <random seed>'
        sys.exit(2)


if __name__ == "__main__":
    file_name, termination1, seed = command_line_reader(sys.argv[1:])
    open_file(file_name)
    random.seed(seed)
    start1 = time.time()
    remind_time1 = 2
    cost1, route1 = path_scanning(start1, remind_time1, termination1)
    result = "s "
    for r in range(0, len(route1)-1):
        result = result+"0,"
        for m in range(1, len(route1[r])-1):
            result = result+"("+str(route1[r][m][0])+","+str(route1[r][m][1])+")"+","
        result = result+"0,"
    result = result + "0,"
    for m in range(1, len(route1[len(route1)-1]) - 1):
        result = result + "(" + str(route1[len(route1)-1][m][0]) + "," + str(route1[len(route1)-1][m][1]) + ")" + ","
    result = result + "0\n"
    result = result+"q "+str(int(cost1))
    print result





