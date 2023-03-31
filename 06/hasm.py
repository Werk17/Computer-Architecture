import sys

next_RAM = 16
symbols = {
    "R0":  "0",
    "R1":  "1",
    "R2":  "2",
    "R3":  "3",
    "R4":  "4",
    "R5":  "5",
    "R6":  "6",
    "R7":  "7",
    "R8":  "8",
    "R9":  "9",
    "R10":  "10",
    "R11":  "11",
    "R12":  "12",
    "R13":  "13",
    "R14":  "14",
    "R15":  "15",
    "SCREEN": "16384",
    "KBD":  "24576",
    "SP": "0",
    "LCL":  "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4"
}

Comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

Dest = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

Jump = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

command_type = {
    '@':'A_COMMAND',
    '(':'L_COMMAND',
    'D':'C_COMMAND',
    'A':'C_COMMAND',
    'M':'C_COMMAND',
    '0':'C_COMMAND',
    '1':'C_COMMAND',
    '-1':'C_COMMAND',
    "!":"C_COMMAND",
    "-":"C_COMMAND"
    }


class Hasm(object):
    lines = []
    def __init__(self, filename):
        with open(filename, "r") as f:
            Hasm.pass1(f.readlines())
            Hasm.pass2(f.readlines())

    def pass1(self, line) -> str:
        # Hasm.strip_whitespace(lines)
        pass

    def pass2(self, lines) -> str:

        
        # mnemonic = line.split()
        binary = '{0:016b}'.format(val)
        pass

    # def strip_whitespace(lines):
    #     instructions = []
    #     for line in lines:
    #         stripped_line = line.strip() 
    #         if stripped_line:
    #             if not stripped_line.startswith("//"):
    #                 if "//" in stripped_line:
    #                     instructions.append(stripped_line.split("//")[0].strip())
    #                 else:
    #                     instructions.append(stripped_line)
    #     return instructions

    def dest2bin(mnemonic):
        # returns the binary code for the destination part of a C-instruction
        return Dest[mnemonic]

    def comp2bin(mnemonic):
        # returns the binary code for the comp part of a C-instruction
        return Comp[mnemonic]

    def jump2bin(mnemonic):
        # returns the binary code for the jump part of a C-instruction
        return Jump.get(mnemonic)

    def commandType(command):
        # returns "A_COMMAND", "C_COMMAND", or "L_COMMAND"
        # depending on the contents of the 'command' string
        if command.startswith('@'):
            return "A_COMMAND"
        elif command.startswith('('):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    

    def getSymbol(command):
        # given an A_COMMAND or L_COMMAND type, returns the symbol as a string,
        # eg (XXX) returns 'XXX'
        # @sum returns 'sum'
        if command.startswith("@"): # A_COMMAND
            return command[1:]
        elif command.startswith("(") and command.endswith(")"):
            return command[1:-1]
        else:
            return 'Invalid command type'
    
    
    def getDest(command):
        # return the dest mnemonic in the C-instruction 'commmand'
        ep = command.find("=")
        if ep == -1:
            return "null"
        return command[0:ep]

    def getComp(command):
        # return the comp mnemonic in the C-instruction 'commmand'
        if commandType(command) == "C_COMMAND":
            cmd = command
            if "=" in cmd:
                cmd = cmd.partition("=")[2]
            return cmd.partition(";")[0]
        return "" #This is an error condition

    def getJump(command):
        # return the jump mnemonic in the C-instruction 'commmand'
        if ';' in command:
            return command.split(';')[1]
        else:
            return 'null'

    


if __name__ == "__main__":
    assembler = Hasm(sys.argv[1])
    