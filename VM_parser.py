import re
import regex_patterns
import memory_parser
import arithmetic_parser
import function_parser
import branching_parser

ARITHMETIC_LINE_TYPE = 1
FUNCTION_LINE_TYPE = 2
MEMORY_LINE_TYPE = 3
BRANCHING_LINE_TYPE = 4
CALL_SYS = 'call Sys.init 0'


def init():
    return [
        "\t@256",
        "\tD=A",
        "\t@SP",
        "\tM=D"
    ] + function_parser.call_cmd(CALL_SYS)


def type_detector(line):
    parts = line.split()
    if parts[0] in arithmetic_parser.POSSIBLE_COMMANDS:
        return ARITHMETIC_LINE_TYPE
    if parts[0] in memory_parser.POSSIBLE_COMMANDS:
        return MEMORY_LINE_TYPE
    if parts[0] in function_parser.POSSIBLE_COMMANDS:
        return FUNCTION_LINE_TYPE
    if parts[0] in branching_parser.POSSIBLE_COMMANDS:
        return BRANCHING_LINE_TYPE
    return -1


def line_stripper(line):
    match = re.match(regex_patterns.REDUNDANT_PARTS, line)
    if match is not None:
        return match.group('command').strip()
    raise ValueError("Parsing error! line : #########################", line, "did not parse ########################")


def parse_line(line, name):
    if line is not None:
        line_type = type_detector(line)
        if line_type == MEMORY_LINE_TYPE:
            return memory_parser.parse(line, name)
        if line_type == ARITHMETIC_LINE_TYPE:
            return arithmetic_parser.parse(line)
        if line_type == FUNCTION_LINE_TYPE:
            return function_parser.parse(line)
        if line_type == BRANCHING_LINE_TYPE:
            return branching_parser.parse(line)
    return None


def comment_ws_remover(lines):
    result = []
    for line in lines:
        match = re.match(regex_patterns.COMMENT_REGEX, line)
        if match:
            continue
        result.append(line)
    return result


def translate(lines, name):
    clean_lines = comment_ws_remover(lines)
    result = []
    for line in clean_lines:
        stripped = line_stripper(line)
        if stripped != '':
            result.append("//" + line)
            result += parse_line(stripped, name)
    return result
