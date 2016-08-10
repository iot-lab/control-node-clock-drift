#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re

def extract_timestamps(line):

    tcn = line[22:39]
    timestamp = str(round(float(tcn)))
    node = "A8-50"
    return node, timestamp, tcn


def read_timestamps(input_fd):
    timestamps = []

    for line in input_fd:
        if line[0] == 'm':
            node, timestamp, tcn = extract_timestamps(line)
            timestamp_final = {"tcn": tcn, "timestamp": timestamp, "node": node}
            timestamps.append(timestamp_final)
    return timestamps


def save_timestamps(output_fd, timestamps):
    for timestamp in  timestamps:
        output_fd.write('%s;%s;%s\n' % (timestamp['node'],
                                        timestamp['timestamp'],
                                        timestamp['tcn']))


def main():
    try:
        input_csv = sys.argv[1]
        output = sys.argv[2]
    except IndexError:
        print 'Usage: %s <aggregator_output> <output>' % sys.argv[0]
        exit(1)

    with open(input_csv, "r") as input_fd:
        timestamps = read_timestamps(input_fd)

    with open(output, 'w') as output_fd:
        save_timestamps(output_fd, timestamps)


if __name__ == '__main__':
    main()
