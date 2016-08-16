#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""Display all files timestamps or drift.

usage: plot_a8_pps.py [-h] [--time | --diff] pps_log_file [pps_log_file ...]

positional arguments:
  pps_log_file  A8 pps log file

optional arguments:
  -h, --help    show this help message and exit

Plot selection:
  --time        Default
  --diff
"""

# Author: Gaëtan Harter <gaetan.harter@inria.fr>

import os
import sys

import argparse
from matplotlib import pyplot as plt


PARSER = argparse.ArgumentParser()
PARSER.add_argument('files', metavar='pps_log_file', nargs='+',
                    help='A8 pps log file')
PARSER.add_argument('--column', '--timestamp-column',
                    dest='column', type=int, default=0,
                    help='timestamp column')

_PLOT = PARSER.add_argument_group(title='Plot selection')

_PLOT = _PLOT.add_mutually_exclusive_group()
PARSER.set_defaults(select='time')
_PLOT.add_argument('--time', dest='select', action='store_const', const='time',
                   help='Default')
_PLOT.add_argument('--diff', dest='select', action='store_const', const='diff')


def extract_float_column(line, column=0, separator=' '):
    """Extract timestamp from line

    >>> extract_float_column('1471020670.018622479 PPS 15')
    1471020670.0186224

    # Allow unclean lines and select column
    >>> extract_float_column('firt_entry 1471020670.018622479 PPS 15\\n',
    ...                      column=1)
    1471020670.0186224

    # Select separator
    >>> extract_float_column('1471020670.018622479;PPS;15', separator=';')
    1471020670.0186224

    # Errors
    >>> extract_float_column('Notfloat PPS 12')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    """
    entries = line.strip().split(separator)
    timestamp = entries[column]
    return float(timestamp)


def _check_missing_pps(entries):
    """Detect if some pps where dropped."""
    for prev, current in zip(entries, entries[1:]):
        diff = current - prev
        if diff > 1.5:
            raise ValueError('Lost some PPS, difference == %f' % diff)


def extract_timestamps(pps_file, column=0):
    entries = []
    for line in pps_file:
        try:
            entries.append(extract_float_column(line, column=column))
        except ValueError:
            continue

    if not entries:
        raise ValueError('No valid measures')
    _check_missing_pps(entries)

    return entries


def parse_files(files, column=0):
    timestamps_dict = {}
    for pps_file in files:
        try:
            with open(pps_file, 'r') as pps_fd:
                timestamps_dict[pps_file] = extract_timestamps(pps_fd, column)
        except ValueError as err:
            print('Error in file: %s, ignore: %s' % (pps_file, err))
    return timestamps_dict


def plot_timestamps(timestamps_dict):
    print('Displaying %s files' % len(timestamps_dict))

    for filename, timestamps in timestamps_dict.items():
        plt.plot(timestamps)
    plt.show()


def timestamps_to_diff(timestamps):
    """Convert timestamps list to diff from expected value."""
    t_s_0 = timestamps[0]
    t_pps_0 = round(t_s_0)

    diffs = []
    for count, t_s in enumerate(timestamps):
        t_s = t_s - t_pps_0 - count
        diffs.append(t_s)
    return diffs


def _info_timestamps_drift(filename, timestamps):
    """Print timestamps drift."""
    drift = (timestamps[-1] - timestamps[0]) / (len(timestamps) - 1)

    drift_ppm = drift * 1000000
    print('Drift %s: %f ppm' % (filename, drift_ppm))


def info_dict_drifts(diff_dict):
    """Print drift infos for diff dicts."""
    for filename, timestamps in diff_dict.items():
        _info_timestamps_drift(filename, timestamps)


def main():
    """Display all files timestamps or drift."""
    opts = PARSER.parse_args()

    timestamps_dict = parse_files(opts.files, opts.columen, skip)

    if opts.select == 'time':
        plot_timestamps(timestamps_dict)

    elif opts.select == 'diff':
        diff_dict = {k: timestamps_to_diff(v) for k, v in
                     timestamps_dict.items()}
        info_dict_drifts(diff_dict)
        plot_timestamps(diff_dict)

    else:
        raise ValueError('Unsupported plot selection: %s' % opts.select)

if __name__ == '__main__':
    main()
