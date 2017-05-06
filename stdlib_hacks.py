# Created by ripopov
from __future__ import print_function
import sys
import gdb
import gdb_hacks


class StdVectorIterator(object):
    def __init__(self, begin, end):
        self.cur = begin
        self.end = end

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.cur != self.end:
            val = self.cur.dereference()
            self.cur += 1
            return val
        else:
            raise StopIteration()


class StdVectorView(object):
    def __init__(self, val):
        assert val.dynamic_type.name.startswith('std::vector<')

        self.val = val
        self.begin = val['_M_impl']['_M_start']
        self.end = val['_M_impl']['_M_finish']
        self.size = self.end - self.begin

    def __iter__(self):
        return StdVectorIterator(self.begin, self.end)

    def prnt(self):
        print ("size ", self.size)

        for i in range(0, self.size - 1):
            print ((self.begin + i).dereference().dereference().dynamic_type.name)

    def __str__(self):
        res = 'vector ' + self.val.dynamic_type.name + '\n'
        for ii in range(0, self.size):
            element = (self.begin + ii).dereference()
            element_type = element.dynamic_type

            if element_type.code == gdb.TYPE_CODE_PTR:
                res += '[' + str(ii) + '] type = ' + element.dereference().dynamic_type.name + ' *\n'
            else:
                res += '[' + str(ii) + '] type = ' + element.dynamic_type.name() + '\n'

        return res

    def __getitem__(self, key):
        assert key < self.size
        return (self.begin + key).dereference()


# http://stackoverflow.com/questions/7429462/creating-c-string-in-gdb
def create_std_string(val):
    res_ptr = gdb.parse_and_eval('(std::string*) malloc(sizeof(std::string))')
    res = res_ptr.dereference()
    gdb_hacks.call_method(res, "basic_string")
    gdb_hacks.call_method_param(res, "assign", '"' + val + '"')
    return res
