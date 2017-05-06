# Created by ripopov
from __future__ import print_function
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import gdb
import sc_design

print ("SystemC Full trace")
# if sys.version_info[0] > 2:
#     raise RuntimeError("Python 3.x is not supported yet")

# Intermediate breakpoint at main required for dynamic linking
bp_main = gdb.Breakpoint("main")
gdb.execute('run')
bp_main.enabled = False

bp_start = gdb.Breakpoint('*sc_core::sc_start')

gdb.execute("continue")
bp_start.enabled = False

simctx = gdb.parse_and_eval("sc_get_curr_simcontext()").dereference()
design = sc_design.SCModule(simctx)

design.trace_all("full_trace");

gdb.execute("continue")
sys.exit(0)
