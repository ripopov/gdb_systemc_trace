# Created by ripopov
import gdb


def is_type_compatible(val_type, name):
    real_type = val_type.strip_typedefs()

    if real_type.name == name:
        return True

    if real_type.code != gdb.TYPE_CODE_STRUCT:
        return False

    for field in real_type.fields():
        if field.is_base_class:
            if is_type_compatible(field.type, name):
                return True

    return False


# http://stackoverflow.com/questions/22774067/gdb-python-api-is-it-possible-to-make-a-call-to-a-class-struct-method
def call_method(val, method_name):
    eval_string = "(*(" + str(val.dynamic_type) + "*)(" + str(val.address) + "))." + method_name + "()"
    return gdb.parse_and_eval(eval_string)


def call_method_param(val, method_name, param):
    eval_string = "(*(" + str(val.dynamic_type) + "*)(" + str(val.address) + "))." + method_name + "(" + param + ")"
    return gdb.parse_and_eval(eval_string)


def lookup_global_function(name):
    res = gdb.lookup_global_symbol(name, gdb.SYMBOL_FUNCTIONS_DOMAIN)

    if not res or not res.is_function:
        raise RuntimeError("Function " + name + " lookup failed. Please check README")

    return res.value()


def __get_data_fields_rec(mtype, res):
    for field in mtype.fields():
        if field.is_base_class:
            __get_data_fields_rec(field.type, res)
        elif not field.artificial:
                res.append(field)
    return res


def get_data_member_list(gdb_value):
    members = []
    fields = []
    __get_data_fields_rec(gdb_value.type.strip_typedefs(), fields)

    for field in fields:
        members.append((gdb_value[field.name], field.name))

    return members
