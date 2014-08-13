from types import CodeType
import opcode
import dis
from opcode import opname, opmap

def make_tail_recursive(fn):
    old_code = fn.__code__
    bytecode = tail_recurse(fn)
    c = CodeType(old_code.co_argcount, old_code.co_nlocals, old_code.co_stacksize,
            old_code.co_flags, bytecode, old_code.co_consts, old_code.co_names,
            old_code.co_varnames, old_code.co_filename, old_code.co_name, old_code.co_firstlineno,
            old_code.co_lnotab)
    fn.__code__ = c
    return fn

def tail_recurse(fn):
    new_bytecode = []
    jump_displacement = 0
    jump_list = []
    code_obj = fn.__code__
    for byte, arg in consume(code_obj.co_code):
        name = opcode.opname[byte]
        if name == "LOAD_GLOBAL" and code_obj.co_names[arg] == fn.__name__:
            jump_displacement -= 3
        elif name == "CALL_FUNCTION":
            for i in range(arg): # 0, 1
                new_bytecode.append(opmap["STORE_FAST"])
                new_bytecode += split(arg - i - 1)
            new_bytecode.append(opmap["JUMP_ABSOLUTE"])
            new_bytecode += split(0) # jump to beginning of bytecode
            jump_displacement += 3 * arg
        else:
            new_bytecode.append(byte)
            if arg is not None:
                new_bytecode += split(arg)
        if byte > opcode.HAVE_ARGUMENT:
            jump_list.append(jump_displacement)
            jump_list.append(jump_displacement)
        jump_list.append(jump_displacement)

    newer_bytecode = []
    for byte, arg in consume(new_bytecode):
        if byte in opcode.hasjabs:
            arg = arg + jump_list[arg]

        newer_bytecode.append(byte)
        if arg is not None:
            newer_bytecode += split(arg)

    return "".join([chr(b) for b in newer_bytecode])

def split(num):
    """ Return an integer as two bytes"""
    return divmod(num, 255)[::-1]


def consume(bytecode):
    if isinstance(bytecode[0], str):
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

@make_tail_recursive
def fact(n, accum):
    if n <= 1:
        return accum
    else:
        return fact(n-1, accum*n)

def fact2(n, accum):
    if n > 1:
        return fact2(n-1, accum*n)
    else:
        return accum

def fact3(n, accum):
    x = fact3
    if n <= 1:
        return accum
    else:
        return fact3(n-1, accum*n)




if __name__ == '__main__':
    # print fact(1000,1)
    # print dis.dis(fact)

    fact2 = make_tail_recursive(fact2)
    dis.dis(fact2)
    print fact2(1000, 1)
    # fact3 = make_tail_recursive(fact3)
