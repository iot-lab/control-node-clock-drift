#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re

def extract_timestamps(line):
    """Extract node and timestamp from raw csv line

    >>> line = ('1467723748.145115;m3-5;'
    ...         'Control Node time: 1467723748.499522. '
    ...         'Date is: UTC 2016-07-05 13:02:28.499522')
    >>> extract_timestamps(line)
    ('m3-5', '1467723748.145115', '1467723748.499522')
    """

    tcn = re.search(r'\s(\d+\.\d+)', line).group(1)
    timestamp = re.search(r'\d+.\d+', line).group()
    node = re.search(r'\;(.*?)\;', line).group(1)
    return node, timestamp, tcn


def read_timestamps(input_fd):
    timestamps = []

    for line in input_fd:
        node, timestamp, tcn = extract_timestamps(line)
        timestamp = {"tcn": tcn, "timestamp": timestamp, "node": node}
        timestamps.append(timestamp)
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
