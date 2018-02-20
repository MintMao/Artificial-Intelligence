# -*- coding: utf-8 -*-
import numpy as num
import random
import sys
import time
from collections import defaultdict
import argparse

# 用来储存父节点-子节点键值对
nodes = defaultdict(dict)  # 用来存 节点-节点 键值对 {start:{{end:weight},{end1,weight}}
nodes_amount = 0  # 节点的数量
edges_amount = 0
nodes_set = defaultdict(set)
start_time = 0
end_time = -sys.maxint

# 读入文件部分
def open_network_file(filename):
    global nodes
    global nodes_set
    global nodes_amount
    global edges_amount
    f = open(filename, 'r')
    index = 0
    for line in f:
        if index == 0:
            nodes_amount = int(line.split(' ')[0])
            edges_amount = int(line.split(' ')[1])
        elif index <= edges_amount:
            start = int(line.split(' ')[0])
            end = int(line.split(' ')[1])
            edge_weight = float(line.split(' ')[2])
            nodes[start][end] = edge_weight
            nodes_set[start].add(end)
            # if len(nodes) == 0 or not nodes.has_key(start):
            #     nodes.update({start:{}})
            #     nodes[start].update({end: edge_weight})
            # else:
            #     nodes[start].update({end: edge_weight})


        index += 1


# def open_seed_file(filename):
#     global seed_set
#     f = open(filename, 'r')
#     for line in f:
#         seed_set.append(int(line))


def ise_ic_sample(amount, seed_set):
    result_sum = 0
    for k in range(0, amount):
        nodes_condition = num.zeros(nodes_amount + 1)
        activity_set = seed_set
        for i in seed_set:
            nodes_condition[i] = 1
        count = len(activity_set)
        while activity_set:
            new_activity_set = []
            for i in activity_set:
                    for j in nodes[i]:
                        if nodes_condition[j] == 0:
                            probability = random.random()
                            if probability <= nodes[i][j]:
                                nodes_condition[j] = 1
                                new_activity_set.append(j)
            count = count + len(new_activity_set)
            activity_set = new_activity_set
        for i in range(1, nodes_amount + 1):
            nodes_condition[i] = 0
        result_sum += count
    return float(result_sum)/amount


def ise_lt_sample(amount, seed_set):
    result_sum = 0
    k = 0
    while k < amount:
        activity_set = seed_set
        nodes_condition = num.zeros(nodes_amount+1)
        new_weight = num.zeros(nodes_amount+1)
        threshold = num.zeros(nodes_amount+1)
        for i in seed_set:
            nodes_condition[i] = 1
        count = len(activity_set)
        while activity_set:
            new_activity_set = []
            for i in activity_set:
                    for j in nodes[i]:
                        if nodes_condition[j] == 0:
                            if threshold[j] == 0:
                                threshold[j] = random.random()
                            new_weight[j] += nodes[i][j]
                            if new_weight[j] > threshold[j]:
                                nodes_condition[j] = 1
                                new_activity_set.append(j)
            count += len(new_activity_set)
            activity_set = new_activity_set
        for i in range(1, nodes_amount + 1):
            nodes_condition[i] = 0
        result_sum += count
        k += 1
    return float(result_sum)/amount



def imp_parse_command_line():
    parser = argparse.ArgumentParser(description="IMP -- Influence Maximization Processor")
    parser.add_argument("-i", metavar="<social network>", dest="network", type=str, required=True,
                        help="the absolute path of the social network file.")

    parser.add_argument("-k", metavar="<predefined size of the seed set>", dest="size", type=int, required=True,
                        help="a positive integer.")

    parser.add_argument("-m", metavar="<diffusion model>", dest="model", type=str, required=True,
                        help="diffusion model which can only be IC or LT.")

    parser.add_argument("-b", metavar="<termination type>", dest="termination", type=int, required=True,
                        help="specifies the termination manner and the value can\
                            only be 0 or 1. If it is set to 0, the termination condition is as the same\
                            defined in your algorithm. Otherwise, the maximal time budget specifies\
                            the termination condition of your algorithm.")

    parser.add_argument("-t", metavar="<time budget>", dest="utime", type=int, required=True,
                        help="a positive number which indicates how many seconds\
                            (in Wall clock time, range: [60s, 1200s]) your algorithm can spend on\
                            this instance. If the <termination type> is 0, it still needs to accept -t\
                            <time budget>, but can just ignore it while estimating.")

    parser.add_argument("-r", metavar="<random seed>", dest="rand", type=str, default=None,
                        help="random seed used in the algorithm")
    args = parser.parse_args()
    # print args.network, args.size, args.model, args.termination, args.utime, args.rand
    if args.termination != 0 and args.termination != 1:
        parser.error('argument -b: should be 0 or 1.')
    return args.network, args.size, args.model, args.termination, args.utime, args.rand



# def count_dv(node):
#     has_count = num.zeros(nodes_amount+1)
#     queue = list()
#     count = 0
#     queue.append(node)
#     print node
#     while queue:
#         node = queue.pop(0)
#
#         has_count[node] = 1
#         for i in nodes[node]:
#             if has_count[i] == 0:
#                 queue.append(i)
#                 count += 1
#     return count


def ic_model(size, p):
    # {v:{{dv: },{tv: },{ddv: }}
    set_v = set()
    set_s = set()
    degree = defaultdict(dict)
    global end_time
    for i in nodes.keys():
        # number = count_dv(i)
        degree[i]["dv"] = len(nodes[i])
        degree[i]["tv"] = 0
        degree[i]["ddv"] = len(nodes[i])
        set_v.add(i)
    print set_v
    k = 0
    while end_time-start_time <= u_time-3 and k<size :

        max_num = 0
        vertex = None
        for element in set_v:
            if degree[element]["ddv"] > max_num:
                max_num = degree[element]["ddv"]
                vertex = element
        set_s.add(vertex)
        print vertex
        set_v.remove(vertex)
        for element in nodes[vertex]:
            if element in degree:
                dv = degree[element]["dv"]
                degree[element]["tv"] = len(nodes_set[element]&set_s)
                tv = degree[element]["tv"]
                degree[element]["ddv"] =2*tv+(dv-tv)*tv*p
        if termination == 1:
            end_time = time.time()
        k += 1
    return set_s


def lazy_forward(k, model_type, sample_type):
    new_seed_set = set()
    vertex_set = set()
    cost_function = {}
    cur_s = {}
    global end_time
    for i in nodes:
        if nodes[i]:
            vertex_set.add(i)
            cost_function.update({i: sys.maxint})
            cur_s.update({i: sys.maxint})
    while len(new_seed_set)+1 <= k and end_time-start_time <= u_time-3:
        for s in vertex_set - new_seed_set:
            cur_s[s] = 0
        combine_set_a = []
        for s in new_seed_set:
            combine_set_a.append(s)
        if sample_type == "IC":
            round_test = ise_ic_sample(1000, combine_set_a)
        else:
            round_test = ise_lt_sample(1000,combine_set_a)
        while 1:
            max_value = -sys.maxint
            seed_star = None
            for s in vertex_set - new_seed_set:
                if model_type == "UC":
                    if max_value<cost_function[s]:
                        max_value  = cost_function[s]
                        seed_star = s
                if model_type == "CB":
                    if max_value < cost_function[s]/(len(nodes[s])+1):
                        max_value = cost_function[s]
                        seed_star = s
            if cur_s[seed_star] == 1:
                new_seed_set.add(seed_star)
                vertex_set.remove(seed_star)
                break
            else:
                combine_set = []
                for i in new_seed_set:
                    combine_set.append(i)
                combine_set.append(seed_star)
                if sample_type == "IC":
                    cost_function[seed_star] = ise_ic_sample(1000, combine_set) - round_test
                    cur_s[seed_star] = 1
                else:
                    cost_function[seed_star] = ise_lt_sample(1000, combine_set) - round_test
                    cur_s[seed_star] = 1
        if termination ==1:
            end_time = time.time()
    seed_set = []
    for i in new_seed_set:
        seed_set.append(i)
    return seed_set


def cost_effective_lazy_forward(k, sample_type):
    seed_set1 = lazy_forward(k, "UC", sample_type)
    seed_set2 = lazy_forward(k ,"CB", sample_type)
    if sample_type == "IC":
        result1 = ise_ic_sample(10000, seed_set1)
        result2 = ise_ic_sample(10000, seed_set2)
        if result1 > result2:
            return seed_set1
        else:
            return seed_set2
    if sample_type == "LT":
        result1 = ise_ic_sample(10000, seed_set1)
        result2 = ise_ic_sample(10000, seed_set2)
        if result1 > result2:
            return seed_set1
        else:
            return seed_set2


if __name__ == "__main__":
    network, size, model, termination, u_time, rand = imp_parse_command_line()
    open_network_file(network)
    random.seed(rand)
    if termination == 1:
        start_time = time.time()
        if edges_amount>1000:
            get_seed_set = ic_model(size, 0.01)
        else:
            get_seed_set = cost_effective_lazy_forward(size, model)
        for get_seed in get_seed_set:
            print get_seed
    else:
        end_time = -sys.maxint
        start_time = 0
        get_seed_set = cost_effective_lazy_forward(size, model)
        for get_seed in get_seed_set:
            print get_seed
    # open_network_file("C:\Users\THINKPAD\PycharmProjects\IMP\AI_IMP\AI_IMP\\network.txt")
    # print nodes
    # termination = 0
    # u_time = sys.maxint
    # seed_set = ic_model(4, 0.01)
    # print ise_lt_sample(1000, seed_set)













