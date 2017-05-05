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
