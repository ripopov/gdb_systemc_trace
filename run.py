#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import argparse
from subprocess import call

parser = argparse.ArgumentParser(description='GDB SystemC tracing')
parser.add_argument("-l", "--list_signals", help="print all signals in design without running simulation", action="store_true")
parser.add_argument("-p", "--print_hier", help="print design tree", action="store_true")
parser.add_argument("-f", "--signals_file", help="file with list of signals to trace", type=str)
parser.add_argument("sim_exe", help="SystemC simulation executable", type=str)

args, unknownargs = parser.parse_known_args()

trace_script = (os.path.dirname(os.path.abspath(__file__)))+"/run_trace.py"

argdict = {'list_signals': args.list_signals, 'print_hier': args.print_hier, 'signals_file': args.signals_file}
argstring = "py argdict = " + str(argdict) + ""

call_list = ["gdb", "-ex", argstring, "-x", trace_script, "--args", args.sim_exe] + unknownargs

call(call_list)
