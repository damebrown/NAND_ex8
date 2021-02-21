import memory_parser as mp

RET_ADDRESS = 'ret_address'

VAR_NAME = 'frame'

FUNC_OR_CALL_LEN = 3

POSSIBLE_COMMANDS = ['call', 'function', 'return']

FUNCTION_COUNTER = 0


def parse(line):
    """
    parses a function command line, returns an array of the suitable .asm code.
    :param line: the line recognizes previously as a function command line.
    :return: an array of the suitable .asm code
    """
    if len(line.split()) == FUNC_OR_CALL_LEN:
        if line.startswith(POSSIBLE_COMMANDS[0]):
            return call_cmd(line)
        elif line.startswith(POSSIBLE_COMMANDS[1]):
            return function_cmd(line)
    elif line == POSSIBLE_COMMANDS[2]:
        return return_cmd()


def call_cmd(line):
    """
    handles a line of type "call functionName n_args"
    :param line: an array of the line's separate strings
    :return: the .asm code suitable to this command
    """
    global FUNCTION_COUNTER
    FUNCTION_COUNTER += 1
    str_arr = line.split()
    function_name, n_args = str_arr[1], str_arr[2]
    return_address = RET_ADDRESS + str(FUNCTION_COUNTER)
    asm_lines = mp.virtual_push(return_address, "A")
    for key, val in mp.SOLID_MEMORY_segmentS.items():
        asm_lines += mp.virtual_push(val, "M")
    asm_lines += move_arg(n_args)
    asm_lines += assign_rhs_to_lhs("SP", "LCL")
    asm_lines += goto_label(function_name)
    asm_lines += ["(" + return_address + ")"]
    return asm_lines


def goto_label(label_name):
    return [
        "\t@" + label_name,
        "\t0;JMP"
    ]


def move_arg(n_args):
    return [
        "\t@SP",
        "\tD=M",
        "\t@5",
        "\tD=D-A",
        "\t@" + n_args,
        "\tD=D-A",
        "\t@ARG",
        "\tM=D"
    ]


def assign_rhs_to_lhs(rhs, lhs):
    return [
        "\t@" + rhs,
        "\tD=M",
        "\t@" + lhs,
        "\tM=D"
    ]


def function_cmd(line):
    """
    handles a line of type "function functionName nVars"
    :param line: an array of the line's separate strings
    :return: the .asm code suitable to this command
    """
    str_arr = line.split()
    function_name, n_vars = str_arr[1], str_arr[2]
    asm_lines = ["(" + function_name + ")"]
    for var in range(int(n_vars)):
        asm_lines += mp.virtual_push('0', 'A')
    return asm_lines


def goto_content(content):
    return [
        "\t@" + content,
        "\tA=M",
        "\t0;JMP"
    ]


def return_cmd():
    """
    handles a line of type "return"
    :return: the .asm code suitable to this command
    """
    asm_lines = assign_rhs_to_lhs("LCL", VAR_NAME)
    asm_lines += assign_rhs_minus_num_to_lhs(VAR_NAME, 5, RET_ADDRESS)
    asm_lines += pop_to_dereference("ARG")
    asm_lines += sp_is_seg_plus_num("ARG", str(1))
    i = 4
    for key, val in mp.SOLID_MEMORY_segmentS.items():
        asm_lines += assign_rhs_minus_num_to_lhs(VAR_NAME, i, val)
        i -= 1
    asm_lines += goto_content(RET_ADDRESS)
    return asm_lines


def pop_to_dereference(memory_seg):
    """
    translating the line " *MEMORY_SEG = pop()"
    :param memory_seg: a memory seg that the address of dereferencing it is the address to put pop's value
    :return: array
    """
    return [
        "\t@SP",
        "\tAM=M-1",
        "\tD=M",
        "\t@" + memory_seg,
        "\tA=M",
        "\tM=D"
    ]


def sp_is_seg_plus_num(memory_seg, num):
    return [
        "\t@" + memory_seg,
        "\tD=M",
        "\t@" + str(num),
        "\tD=D+A",
        "\t@SP",
        "\tM=D"
    ]


def assign_rhs_minus_num_to_lhs(rhs, num, lhs):
    return [
        "\t@" + rhs,
        "\tD=M",
        "\t@" + str(num),
        "\tA=D-A",
        "\tD=M",
        "\t@" + lhs,
        "\tM=D"
    ]