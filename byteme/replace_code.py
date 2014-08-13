from types import CodeType
import opcode
from opcode import opname, opmap

def fact(n, accum):
    if n <= 1:
        return accum
    else:
        return fact(n-1, accum*n)

def make_new_code(fn):
    old_code = fn.__code__
    bytecode = tail_recurse(fn)
    c = CodeType(old_code.co_argcount, old_code.co_nlocals, old_code.co_stacksize,
            old_code.co_flags, bytecode, old_code.co_consts, old_code.co_names,
            old_code.co_varnames, old_code.co_filename, old_code.co_name, old_code.co_firstlineno,
            old_code.co_lnotab)
    return c

def tail_recurse(fn):
    new_bytecode = []
    code_obj = fn.__code__
    for byte, arg in consume(code_obj.co_code):
        name = opcode.opname[byte]
        print name, arg
        # pdb.set_trace()
        if name == "LOAD_GLOBAL" and code_obj.co_names[arg] == fn.__name__:
            pass # come back and fix jump targets
        elif name == "CALL_FUNCTION":
            for i in range(arg): # 0, 1
                new_bytecode.append(opmap["STORE_FAST"])
                new_bytecode += split(arg - i - 1)
            new_bytecode.append(opmap["JUMP_ABSOLUTE"])
            new_bytecode += split(0) # jump to beginning of bytecode
        else:
            new_bytecode.append(byte)
            if arg is not None:
                new_bytecode += split(arg)

    return "".join([chr(b) for b in new_bytecode])

def split(num):
    """ Return an integer as two bytes"""
    return divmod(num, 255)[::-1]


def consume(bytecode):
    bytecode = [ord(b) for b in bytecode]
    i = 0
    while i < len(bytecode):
        op = bytecode[i]
        if op > opcode.HAVE_ARGUMENT:
            args = bytecode[i+1:i+3]
            arg = args[0] + (args[1] << 8)
            yield op, arg
            i += 3
        else:
            yield op, None
            i += 1

if __name__ == '__main__':
    fact.__code__ = make_new_code(fact)
    print fact(1000,1)
