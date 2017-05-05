# Created by ripopov
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import gdb
import sc_design

print "SystemC Full trace demo"

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
print "SystemC tracing demo finished"
sys.exit(0)
