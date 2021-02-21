POSSIBLE_COMMANDS = ['add', 'sub', 'and', 'or', 'neg', 'not', 'eq', 'gt', 'lt']
BOOLEAN_OPERATOR_COUNTER = 0


def two_var_bool_op(jmp_operator):
    global BOOLEAN_OPERATOR_COUNTER
    BOOLEAN_OPERATOR_COUNTER += 1
    return [
        "\t@SP",
        "\tAM=M-1",
        "\tD=M",
        "\tA=A-1",
        "\tD=D-M",
        "\t@SP",
        "\tA=M-1",
        "\tM=-1",
        "\t@BOOL.OP.END." + str(BOOLEAN_OPERATOR_COUNTER),
        "\tD;" + jmp_operator,
        "\t@SP",
        "\tA=M-1",
        "\tM=0",
        "(BOOL.OP.END." + str(BOOLEAN_OPERATOR_COUNTER) + ")"
    ]


def new_bool_op(jmp_operator):
    global BOOLEAN_OPERATOR_COUNTER
    BOOLEAN_OPERATOR_COUNTER += 1
    first, second, JMP_CMD = "0", "0", "JLT"
    if jmp_operator == "gt":
        JMP_CMD = "JLT"
        first = "0"
        second = "-1"
    if jmp_operator == "lt":
        JMP_CMD = "JGT"
        first = "-1"
        second = "0"
    return [
        "\t@SP",
        "\tA=M-1",
        "\tD=M",  # D=y
        "\t@POSITIVE.Y." + str(BOOLEAN_OPERATOR_COUNTER),
        "\tD;JGE",  # if y>=0
        "\t@SP",
        "\tA=M-1",
        "\tA=A-1",  # get X
        "\tD=M",
        "\t@REG.COMP." + str(BOOLEAN_OPERATOR_COUNTER),
        "\tD;JLT",
        "\t@SP",  # return first result
        "\tAM=M-1",
        "\tA=A-1",
        "\tM=" + second,
        "\t@END.BOOL." + str(BOOLEAN_OPERATOR_COUNTER),
        "\t0;JMP",
        "\t@END.BOOL." + str(BOOLEAN_OPERATOR_COUNTER),
        "\t0;JMP",
        "(POSITIVE.Y." + str(BOOLEAN_OPERATOR_COUNTER) + ")",
        "\t@SP",
        "\tA=M-1",
        "\tA=A-1",  # get X
        "\tD=M",
        "\t@REG.COMP." + str(BOOLEAN_OPERATOR_COUNTER),
        "\tD;JGE",
        "\t@SP",  # return first result
        "\tAM=M-1",
        "\tA=A-1",
        "\tM=" + first,
        "\t@END.BOOL." + str(BOOLEAN_OPERATOR_COUNTER),
        "\t0;JMP",
        "(REG.COMP." + str(BOOLEAN_OPERATOR_COUNTER) + ")",
        "\t@SP",
        "\tAM=M-1",
        "\tD=M",
        "\tA=A-1",
        "\tD=D-M",
        "\t@SP",
        "\tA=M-1",
        "\tM=-1",
        "\t@END.BOOL." + str(BOOLEAN_OPERATOR_COUNTER),
        "\tD;" + JMP_CMD,
        "\t@SP",
        "\tA=M-1",
        "\tM=0",
        "(END.BOOL." + str(BOOLEAN_OPERATOR_COUNTER) + ")"
    ]


def two_var_arithmetic_op(operator):
    return [
        "\t@SP",
        "\tAM=M-1",
        "\tD=M",
        "\tA=A-1",
        "\tM=M" + operator + "D"
    ]


def one_var_arithmetic_op(operator):
    return [
        "\t@SP",
        "\tA=M-1",
        "\tM=" + operator + "M"
    ]


def parse(line):
    if line == 'add':
        return two_var_arithmetic_op('+')
    if line == 'sub':
        return two_var_arithmetic_op('-')
    if line == 'and':
        return two_var_arithmetic_op('&')
    if line == 'or':
        return two_var_arithmetic_op('|')
    if line == 'neg':
        return one_var_arithmetic_op('-')
    if line == 'not':
        return one_var_arithmetic_op('!')
    if line == 'eq':
        return two_var_bool_op('JEQ')
    if line == 'gt':
        return new_bool_op(line)
    if line == 'lt':
        return new_bool_op(line)
