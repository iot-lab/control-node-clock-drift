#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re

def read_timestamps(input_fd, input_csv):
    timestamps = []
    timestamp, tcn = extract_timestamps_oml(input_fd.readline())
    t0 = round(tcn)
    timestamp = {"tcn": tcn, "timestamp": t0, "node": input_csv}
    timestamps.append(timestamp)

    while True:
        line = input_fd.readline()
        if not line: break
        timestamp, tcn = extract_timestamps_oml(line)
        timestamp = t0 + timestamp
        timestamp_final = {"tcn": tcn, "timestamp": timestamp, "node": input_csv}
        timestamps.append(timestamp_final)
    return timestamps


def save_timestamps(output_fd, timestamps):
    for timestamp in  timestamps:
        output_fd.write('%s;%f;%f\n' % (timestamp['node'],
                                        timestamp['timestamp'],
                                        timestamp['tcn']))

def extract_timestamps_oml(line):
    oml_values = line.split()
    tcn = [float(oml_values[3]), float(oml_values[4])]
    time = tcn[0] + tcn[1] / 1000000.
    stamp = float(oml_values[2])
    
    return stamp, time

def main():
    try:
        output = sys.argv[-1]
    except IndexError:
        print 'Usage: %s <oml_file>+ <output>' % sys.argv[0]
        exit(1)

    oml_files = []
    for i in range(1,len(sys.argv) - 1):
        try:
            oml_files.append(sys.argv[i])
        except IndexError:
            print 'Usage: %s <oml_file>+ <output>' % sys.argv[0]
            exit(1)

    output_fd = open(output, 'w') 
    for input_csv in oml_files:   
        with open(input_csv, "r") as input_fd:
            for _ in xrange(9):
                input_fd.readline()
            timestamps = read_timestamps(input_fd, input_csv)
       
        save_timestamps(output_fd, timestamps)


if __name__ == '__main__':
    main()
