# coding=utf-8
# Created by ripopov

import sys
import gdb
import gdb.types
import stdlib_hacks
import gdb_hacks
import sc_trace


def is_sc_object(val_type):
    return gdb_hacks.is_type_compatible(val_type, "sc_core::sc_object")


def is_sc_module(val_type):
    return gdb_hacks.is_type_compatible(val_type, "sc_core::sc_module")


def __is_module_or_interface(mtype):
    tname = mtype.strip_typedefs().name
    return tname in ("sc_core::sc_module", "sc_core::sc_interface")


def __get_plain_data_fields_rec(mtype, res):
    for field in mtype.fields():
        if field.is_base_class:
            if not __is_module_or_interface(field.type):
                __get_plain_data_fields_rec(field.type, res)
        elif not field.artificial:
            if not is_sc_object(field.type):
                res.append(field)

    return res


def get_plain_data_fields(mtype):
    res = []
    __get_plain_data_fields_rec(mtype, res)
    return res


class SCModuleMember:
    def __init__(self, val, name):
        self.value = val
        self.name = name

    def basename(self):
        return str(self.name).split('.')[-1]


class SCModule:

    def __init__(self, gdb_value):
        self.child_modules = []
        self.members = []
        self.name = ""
        self.value = gdb_value.cast(gdb_value.dynamic_type.strip_typedefs())

        if gdb_value.type.name == 'sc_core::sc_simcontext':
            self.__init_from_simctx()
        elif is_sc_module(gdb_value.type):
            self.__init_from_sc_module()
        else:
            assert False

    def __init_from_simctx(self):
        m_child_objects = stdlib_hacks.StdVectorView(self.value['m_child_objects'])
        self.name = "SYSTEMC_ROOT"

        for child_ptr in m_child_objects:
            child = child_ptr.dereference()
            child = child.cast(child.dynamic_type.strip_typedefs())

            if is_sc_module(child.type):
                self.child_modules.append(SCModule(child))
            else:
                self.members.append(SCModuleMember(child, str(child['m_name'])[1:-1]))

    def __init_from_sc_module(self):
        self.name = str(self.value['m_name'])[1:-1]

        m_child_objects_vec = stdlib_hacks.StdVectorView(self.value['m_child_objects'])

        for child_ptr in m_child_objects_vec:
            child = child_ptr.dereference()
            child = child.cast(child.dynamic_type)

            if is_sc_module(child.dynamic_type):
                self.child_modules.append(SCModule(child))
            else:
                self.members.append(SCModuleMember(child, str(child['m_name'])[1:-1]))

        for field in get_plain_data_fields(self.value.type):
            self.members.append(SCModuleMember(self.value[field.name], self.name + "." + field.name))

    def basename(self):
        return str(self.name).split('.')[-1]

    def __to_string(self, prefix):
        res = self.basename() + '    (' + str(self.value.dynamic_type.name) + ')'

        n_child_mods = len(self.child_modules)

        member_prefix = "│" if n_child_mods else " "

        for member in self.members:

            icon = " ○ "
            if is_sc_object(member.value.type):
                icon = " ◘ "

            res += "\n" + prefix + member_prefix + icon + member.basename() + "    (" + str(
                member.value.type.name) + ")     " + str(gdb_hacks.code_str(member.value.type.code))

        for ii in xrange(0, n_child_mods):

            pref0 = "├"
            pref1 = "│"

            if ii == n_child_mods - 1:
                pref0 = "└"
                pref1 = " "

            res += "\n" + prefix + pref0 + "──" + self.child_modules[ii].__to_string(prefix + pref1 + "  ");

        return res

    def __str__(self):
        return self.__to_string("")

    def print_members(self):
        for member in self.members:
            print member.name, " : ", member.value.type.name

        for child_mod in self.child_modules:
            child_mod.print_members()

    def trace_all_tf(self, tracer):
        for member in self.members:
            tracer.trace(member.value, member.name)

        for child_mod in self.child_modules:
            child_mod.trace_all_tf(tracer)

    def trace_all(self, trace_file_name):

        print "Tracing all members"

        tf = sc_trace.SCTrace(trace_file_name)

        self.trace_all_tf(tf)

        pass
