# Created by ripopov
from __future__ import print_function
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import gdb
import sc_design
import gdb_hacks

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

# TODO: Find a better breakpoint for end of elaboration
bp_start = gdb.Breakpoint('*sc_core::sc_start')

gdb.execute("continue")
bp_start.enabled = False

simctx = gdb.lookup_symbol("sc_core::sc_curr_simcontext")[0].value().dereference()

design = sc_design.SCModule(simctx)

if print_hier:
    print (design)

if list_signals:
    design.print_members()

if run_simulation:
    design.trace_all("full_trace")

gdb.execute("continue")
sys.exit(0)
