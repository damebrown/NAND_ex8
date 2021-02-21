POSSIBLE_COMMANDS = ['label', 'goto', 'if-goto']


def parse(line):
    parts = line.split()
    if parts[0] == POSSIBLE_COMMANDS[0]:
        return [
            "(" + parts[1] + ")"
        ]
    if parts[0] == POSSIBLE_COMMANDS[1]:
        return [
            "\t@" + parts[1],
            "\t0;JMP"
        ]
    if parts[0] == POSSIBLE_COMMANDS[2]:
        return [
            "\t@SP",
            "\tAM=M-1",
            "\tD=M",
            "\t@NO.JMP." + parts[1],
            "\tD;JEQ",
            "\t@" + parts[1],
            "\t0;JMP",
            "(NO.JMP." + parts[1] + ")",
        ]
    return []
