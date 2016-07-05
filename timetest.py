#! /usr/bin/env python
# -*- coding:utf-8 -*-

# This file is a part of IoT-LAB aggregation-tools
# Copyright (C) 2015 INRIA (Contact: admin@iot-lab.info)
# Contributor(s) : see AUTHORS file
#
# This software is governed by the CeCILL license under French law
# and abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# http://www.cecill.info.
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""
Serial aggregator
=================

Take an experiment description as input.
Gather all nodes output to stdout, prefixed by the node number and timestamp.

    1395240359.286712;node46; Type Enter to stop printing this help
    1395240359.286853;node46;
    1395240359.292523;node9;
    1395240359.292675;node9;Senslab Simple Demo program

Usage
-----

On each server your experiment is run on:

    $ ./serial_aggregator.py [opts]
    1395240359.286712;node46; Type Enter to stop printing this help
    1395240359.286853;node46;
    1395240359.292523;node9;
    1395240359.292675;node9;Senslab Simple Demo program


Warning
-------

If a node sends only characters without newlines, the output is never printed.
To give a 'correct' looking output, only lines are printed.


### Multi sites experiments ###

The script will get the serial links current site nodes.
For multi-sites experiments, you should run the script on each site server.
"""
# pylint versions have different outputs...
# pylint:disable=too-few-public-methods
# pylint:disable=too-many-public-methods

# use readline for 'raw_input'
# noqa  # pylint:disable=unused-import


import time
from iotlabaggregator.serial import SerialAggregator
import sys

def main(args=None):
    """ Aggregate all nodes sniffer """
    args = args or sys.argv[1:]
    opts = SerialAggregator.parser.parse_args(args)
    try:
        # Parse arguments
        nodes_list = SerialAggregator.select_nodes(opts)
        # Run the aggregator
        with SerialAggregator(nodes_list, print_lines=True,
                              color=opts.color) as aggregator:
            while True:
                message = 'd'
                for node in aggregator.keys():
                    aggregator._send(node, message)
                    time.sleep(0.1) 
    except (ValueError, RuntimeError) as err:
        sys.stderr.write("%s\n" % err)
        exit(1)

if __name__ == '__main__':
    main()
