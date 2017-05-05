# Created by ripopov
import gdb
import stdlib_hacks
import gdb_hacks


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
        members.append( (gdb_value[field.name], field.name))

    return members


class SCTrace:

    def __init__(self, trace_file_name):
        self.sc_create_vcd_trace_file = lookup_global_function('sc_core::sc_create_vcd_trace_file(char const*)')
        self.sc_close_vcd_trace_file = lookup_global_function('sc_core::sc_close_vcd_trace_file(sc_core::sc_trace_file*)')

        self.sc_trace_char_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, char const*, std::string const&, int)')
        self.sc_trace_short_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, short const*, std::string const&, int)')
        self.sc_trace_int_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, int const*, std::string const&, int)')
        self.sc_trace_long_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, long const*, std::string const&, int)')
        self.sc_trace_long_long_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, long long const*, std::string const&, int)')

        self.sc_trace_unsigned_char_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned char const*, std::string const&, int)')
        self.sc_trace_unsigned_short_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned short const*, std::string const&, int)')
        self.sc_trace_unsigned_int_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned int const*, std::string const&, int)')
        self.sc_trace_unsigned_long_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned long const*, std::string const&, int)')
        self.sc_trace_unsigned_long_long_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned long long const*, std::string const&, int)')

        self.sc_trace_bool_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, bool const*, std::string const&)')
        self.sc_trace_float_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, float const*, std::string const&)')
        self.sc_trace_double_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, double const*, std::string const&)')

        self.sc_trace_sc_bit_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_bit const*, std::string const&)')
        self.sc_trace_sc_logic_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_logic const*, std::string const&)')
        self.sc_trace_sc_int_base_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_int_base const*, std::string const&)')
        self.sc_trace_sc_uint_base_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_uint_base const*, std::string const&)')
        self.sc_trace_sc_signed_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_signed const*, std::string const&)')
        self.sc_trace_sc_unsigned_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_unsigned const*, std::string const&)')

        self.sc_trace_sc_bv_base_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_bv_base const*, std::string const&)')
        self.sc_trace_sc_lv_base_ptr = lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_lv_base const*, std::string const&)')

        self.tf = self.sc_create_vcd_trace_file(trace_file_name)

    def trace(self, gdb_value, name):
        real_type = gdb_value.type.strip_typedefs()

        size_bit = 8 * real_type.sizeof

        if real_type.name:
            if real_type.name == "char":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_char_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "signed char":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_char_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "short":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_short_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "int":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_int_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "long":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_long_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "long long":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_long_long_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned char":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_char_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned short":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_short_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned int":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_int_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned long":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_long_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned long long":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_long_long_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "bool":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_bool_ptr(self.tf, gdb_value.address, name_str)

            elif real_type.name == "float":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_float_ptr(self.tf, gdb_value.address, name_str)

            elif real_type.name == "double":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_double_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_bit"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_bit_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_logic"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_logic_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_int_base"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_int_base_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_uint_base"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_uint_base_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_signed"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_signed_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_unsigned"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_unsigned_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_bv_base"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_bv_base_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_lv_base"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_lv_base_ptr(self.tf, gdb_value.address, name_str)

            elif real_type.name == "sc_core::sc_clock" or real_type.name.startswith("sc_core::sc_signal<"):
                m_cur_val = gdb_value['m_cur_val']
                self.trace(m_cur_val, name)

            elif gdb_hacks.is_type_compatible(real_type, "sc_core::sc_method_process"):
                pass

            elif gdb_hacks.is_type_compatible(real_type, "sc_core::sc_thread_process"):
                pass

            elif real_type.name.startswith("sc_core::sc_in<") or real_type.name.startswith("sc_core::sc_out<"):
                m_interface = gdb_value['m_interface']
                m_interface = m_interface.reinterpret_cast(m_interface.dynamic_type);
                sig_val = m_interface.dereference()
                self.trace(sig_val, name)

            elif real_type.name.startswith("sc_core::sc_in<") or real_type.name.startswith("sc_core::sc_out<"):
                m_interface = gdb_value['m_interface']
                m_interface = m_interface.reinterpret_cast(m_interface.dynamic_type);
                sig_val = m_interface.dereference()
                self.trace(sig_val, name)

            elif real_type.code == gdb.TYPE_CODE_STRUCT and not real_type.name.startswith("sc_core::") \
                    and not real_type.name.startswith("sc_dt::"):
                for member in get_data_member_list(gdb_value):
                    self.trace(member[0], name + "*" + member[1])

            else:
                print "Type not supported yet: " + real_type.name


