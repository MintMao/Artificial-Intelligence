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
end_time = 0
seed_set = []

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


def open_seed_file(filename):
     global seed_set
     f = open(filename, 'r')
     for line in f:
         seed_set.append(int(line))


def ise_ic_sample(amount):
    result_sum = 0
    global  end_time
    k = 0
    while k < amount and end_time - start_time < u_time - 2:
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
        k += 1
        if termination == 1:
            end_time = time.time()
    return float(result_sum)/k



def ise_lt_sample(amount):
    result_sum = 0
    k = 0
    global end_time
    while k < amount and end_time-start_time<u_time-2:
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
        if termination == 1:
            end_time = time.time()
    return float(result_sum)/k


def ise_parse_command_line():
    parser = argparse.ArgumentParser(description="ISE -- Influence Spread Estimator")
    parser.add_argument("-i", metavar="<social network>", dest="network", type=str, required=True,
                        help="the absolute path of the social network file.")

    parser.add_argument("-s", metavar="<seed set>", dest="seed", type=str, required=True,
                        help="the absolute path of the seed set file.")

    parser.add_argument("-m", metavar="<diffusion model>", dest="model", type=str, required=True,
                        help="diffusion model which can only be IC or LT.")

    parser.add_argument("-b", metavar="<termination type>", dest="termination", type=int, required=True,
                        help="specifies the termination manner and the value can\
                        only be 0 or 1. If it is set to 0, the termination condition is as the same\
                        defined in your algorithm. Otherwise, the maximal time budget specifies\
                        the termination condition of your algorithm.")

    parser.add_argument("-t", metavar="<time budget>", dest="u_time", type=int, required=True,
                        help="a positive number which indicates how many seconds\
                        (in Wall clock time, range: [60s, 1200s]) your algorithm can spend on\
                        this instance. If the <termination type> is 0, it still needs to accept -t\
                        <time budget>, but can just ignore it while estimating.")

    parser.add_argument("-r", metavar="<random seed>", dest="rand", type=str, default=None,
                        help="random seed used in the algorithm")
    args = parser.parse_args()
    # print args.network, args.seed, args.model, args.termination, args.utime, args.rand
    if args.termination != 0 and args.termination != 1:
        parser.error('argument -b: should be 0 or 1.')
    return args.network, args.seed, args.model, args.termination, args.u_time, args.rand


if __name__ == "__main__":
    network, seed, model, termination, u_time, rand = ise_parse_command_line()
    open_network_file(network)
    open_seed_file(seed)
    if termination == 1:
        start_time = time.time()
        if model == "IC":
            print ise_ic_sample(10000)
        else:
            print ise_lt_sample(10000)
    else:
        end_time = -sys.maxint
        start_time = 0
        if model == "IC":
            print ise_ic_sample(10000)
        else:
            print ise_lt_sample(10000)


