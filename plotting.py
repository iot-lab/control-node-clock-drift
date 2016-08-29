#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys

import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal

treshold =  0.0020
average = 5

def most_common(lst):
    return max(set(lst), key=lst.count)

def plot_nodes_time(input_fd):
    node_time = {}
    for line in input_fd:
        node, timestamp, tcn = line.split(";")
        try:
            node_time[node][0].append(Decimal(timestamp))
            node_time[node][1].append(Decimal(tcn))
        except:
            node_time[node] = [[], []]
    

    plt.figure(1)

    node_drift = {}
    deriv_values = {}
    difference = []
    t = []
    for node in node_time:
        difference = np.subtract(node_time[node][1],node_time[node][0])
        for i in range(len(difference)):
            difference[i] = float(difference[i])
        t = range(len(node_time[node][0]))
        t = np.divide(t, 60.0)
        
        derivative = [(difference[i+1] - difference[i]) / (t[i+1] - t[i]) for i in range(len(node_time[node][0]) - 1)]
 
        for i in range(1, len(derivative)):
            if abs(derivative[i]) > treshold:
                derivative[i] = 0


        deriv_i = [derivative[i:] for i in range(0, average + 1)]
        deriv_average = [sum(v) / float(len(v)) for v in zip(*deriv_i)]

        node_drift[node] = (difference[-1] - difference[0]) / (t[-1] - t[0]) * 1000000 / 60
        deriv_values[node] = most_common(deriv_average) * 1000000 / 60
        plt.plot(t, difference, color = np.random.rand(3,1)) 
        plt.plot(t[0:-average-1], deriv_average, color = np.random.rand(3,1))
        plt.xlabel("time (minutes)")
        plt.ylabel("Drift: tcn - timestamp (seconds)")

    print "drift microseconds / second \n"
    mean = 0.0
    std = 0.0
    for key in node_drift:
        print key + ": " + str(node_drift[key]) 
        mean = mean + node_drift[key]

    for key in deriv_values:
        print key + ": " + str(deriv_values[key]) 

    mean = mean / len(node_drift)
    for key in node_drift:
        std = std +  (node_drift[key] - mean) ** 2;

    std = np.sqrt(std)
    spread = std / mean * 100

    print "Mean: " + str(mean) + "\n" + "Std: " + str(std) + "\n" + "Spread: " + str(spread) + "%"
 
    plt.show()

def main():
    try:
        input_csv = sys.argv[1]
    except IndexError:
        print 'Usage: %s <input>' % sys.argv[0]
        exit(1)

    with open(input_csv, 'r') as input_fd:
        plot_nodes_time(input_fd)


if __name__ == '__main__':
    main()
