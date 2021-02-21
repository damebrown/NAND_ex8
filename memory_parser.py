BASE_TEMP_ADR = 5
PUSH_CMD = "push"
POP_CMD = "pop"
POSSIBLE_COMMANDS = [PUSH_CMD, POP_CMD]
SOLID_MEMORY_segmentS = {"local": "LCL",
                         "argument": "ARG",
                         "this": "THIS",
                         "that": "THAT"}
VIRTUAL_MEMORY_segmentS = ["constant", "static", "pointer", "temp"]
POINTER = ["THIS", "THAT"]


def solid_memory_segment_parser(command, segment, value):
    if command == PUSH_CMD:
        return [
            "\t@" + SOLID_MEMORY_segmentS[segment],
            "\tD=M",
            "\t@" + value,
            "\tA=D+A",
            "\tD=M",
            "\t@SP",
            "\tM=M+1",
            "\tA=M-1",
            "\tM=D"
        ]
    if command == POP_CMD:
        return [
            "\t@" + SOLID_MEMORY_segmentS[segment],
            "\tD=M",
            "\t@" + value,
            "\tD=D+A",
            "\t@SP",
            "\tA=M",
            "\tM=D",
            "\tA=A-1",
            "\tD=M",
            "\tA=A+1",
            "\tA=M",
            "\tM=D",
            "\t@SP",
            "\tM=M-1"
        ]


def virtual_push(symbol, register):
    return [
        "\t@" + symbol,
        "\tD=" + register,
        "\t@SP",
        "\tM=M+1",
        "\tA=M-1",
        "\tM=D",
    ]


def virtual_pop(symbol):
    return [
        "\t@SP",
        "\tM=M-1",
        "\tA=M",
        "\tD=M",
        "\t@" + symbol,
        "\tM=D"
    ]


def virtual_memory_segment_parser(command, segment, value, name):
    if segment == "pointer":
        if command == PUSH_CMD:
            return virtual_push(POINTER[int(value)], "M")
        if command == POP_CMD:
            return virtual_pop(POINTER[int(value)])
    if segment == "constant":
        # always a push command when segment is constant
        return virtual_push(value, "A")
    if segment == "static":
        if command == PUSH_CMD:
            return virtual_push(name + "." + value, "M")
        if command == POP_CMD:
            return virtual_pop(name + "." + value)
    if segment == "temp":
        if command == PUSH_CMD:
            return virtual_push('R' + str(BASE_TEMP_ADR + int(value)), "M")
        if command == POP_CMD:
            return virtual_pop('R' + str(BASE_TEMP_ADR + int(value)))


def parse(line, name):
    command, segment, value = line.split(" ")
    if segment in SOLID_MEMORY_segmentS:
        return solid_memory_segment_parser(command, segment, value)
    if segment in VIRTUAL_MEMORY_segmentS:
        return virtual_memory_segment_parser(command, segment, value, name)
