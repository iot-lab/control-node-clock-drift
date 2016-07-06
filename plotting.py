#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys

import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal

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
    for node in node_time:
        difference = np.subtract(node_time[node][1],node_time[node][0])
        t = range(len(node_time[node][0]))
        t = np.multiply(t, len(node_time) * 0.1)
        t = np.divide(t, 60.0)
        node_drift[node] = (float(difference[-1]) - float(difference[0])) / (t[-1] - t[0]) * 1000000 / 60
        plt.plot(t, difference, color = np.random.rand(3,1)) 
        plt.xlabel("time (minutes)")
        plt.ylabel("Drift: tcn - timestamp (seconds)")

    print "drift microseconds / second \n"
    mean = 0.0
    std = 0.0
    for key in node_drift:
        print key + ": " + str(node_drift[key]) 
        mean = mean + node_drift[key]

    mean = mean / len(node_drift)
    for key in node_drift:
        std = std +  (node_drift[key] - mean) ** 2;

    std = np.sqrt(std)
    spread = std / mean * 100

    print "Mean: " + str(mean) + "\n" + "Std: " +str(std) + "\n" + "Spread: " + str(spread) + "%"
 
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
