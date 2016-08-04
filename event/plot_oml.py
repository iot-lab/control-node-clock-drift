#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os

import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal

def plot_nodes_time(node_time):
    plt.figure(1)

    node_drift = {}

    for node in node_time:
        t0 = node_time[node][0][1][0] if node_time[node][0][1][1] < 500000 else node_time[node][0][1][0] + 1
        pps_time = range(int(t0), int(t0 + node_time[node][-1][0])) 
        
        tcn_double = [node_time[node][i][1] for i in range(len(node_time[node]))]
        tcn_values = [tcn_double[i][0] + (tcn_double[i][1] / 1000000.) for i in range(len(tcn_double))]

        difference = np.subtract(tcn_values, pps_time) * 1000

        t = range(len(node_time[node]))
        t = np.divide(t, 60.0)
        node_drift[node] = (float(difference[-1]) - float(difference[0])) / (t[-1] - t[0]) * 1000 / 60
        plt.plot(t, difference, color = np.random.rand(3,1)) 
        plt.xlabel("time (minutes)")
        plt.ylabel("Drift: tcn - timestamp (milliseconds)")

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

def extract_timestamps_oml(line):
    oml_values = line.split()
    tcn = [float(oml_values[3]), float(oml_values[4])]
    stamp = float(oml_values[2])
    
    return stamp, tcn

def read_timestamps(input_fd):
    timestamps = []

    for line in input_fd:
        stamp, tcn = extract_timestamps_oml(line)
        timestamp = [stamp, tcn]
        timestamps.append(timestamp)
    return timestamps

def main():

    node_time = {}
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".oml"):
            with open(filename, "r") as input_fd:
                for _ in xrange(9):
                    next(input_fd)
                node_time[filename] = read_timestamps(input_fd)

    plot_nodes_time(node_time)

if __name__ == '__main__':
    main()
