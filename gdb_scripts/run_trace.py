# Created by ripopov
from __future__ import print_function

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import gdb


def is_libstdcxx_installed():
    for pp in gdb.pretty_printers:
        try:
            if pp.name.startswith("libstdc++"):
                return True
        except AttributeError:
            pass
    return False


print ("SystemC Full trace")

# Check dependencies
if not is_libstdcxx_installed():
    raise RuntimeError("STL Pretty printers not installed")

# Command line options
print_hier = False
list_signals = False
signals_file = None
run_simulation = True

# Check if arguments were passed
try:
    print_hier = argdict['print_hier']
    list_signals = argdict['list_signals']
    signals_file = argdict['signals_file']
    if list_signals or print_hier:
        run_simulation = False
except NameError:
    pass


# Intermediate breakpoint at main required for dynamic linking, otherwise required systemc symbols won't be found
bp_main = gdb.Breakpoint("main")
gdb.execute('run')
bp_main.enabled = False

bp_start = gdb.Breakpoint('*sc_core::sc_simcontext::prepare_to_simulate')

gdb.execute("continue")
bp_start.enabled = False

simctx = gdb.lookup_symbol("sc_core::sc_curr_simcontext")[0].value().dereference()

import sc_design

design = sc_design.SCModule(simctx)

if print_hier:
    print (design)

if list_signals:
    print("\nList of all detected signals:\n")
    design.print_members()

if run_simulation:
    if signals_file:
        signals = open(signals_file).read().splitlines()
        design.trace_signals("systemc_trace", signals)
    else:
        design.trace_all("systemc_trace")
    gdb.execute("continue")

sys.exit(0)
