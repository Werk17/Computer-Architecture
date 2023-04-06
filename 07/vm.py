import os
import re
import sys


class VM:

    ARITH_BINARY = {
        'add': 'M=D+M',
        'sub': 'M=M-D',
        'and': 'M=M&D',
        'or': 'M=M|D'
    }

    ARITH_UNARY = {

        'neg': '@SP\
            A=M-1\
            M=-M',

        'not': '@SP\
            A=M-1\
            M=!M'
    }

    ARITH_TEST = {
        'eg': 'JEQ',
        'gt': 'JGT',
        'lt': 'JLT'
    }

    SEGLABEL = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
        'pointer': 3,
        'temp': 5,
        'static': 16,
    }

    LABEL_NUMBER = 0

    def __init__(self, filename):
        self.filename = filename
        self.parsFile(filename)

    def getPushD(self):
        D = '''\
        @SP
        AM=M+1
        A=A-1
        M=D'''

    def getPopD(self):
        D = '''\
            @SP
            AM=M-1
            D=M'''

    def pointerSeg(self, push, seg, index):
        # The following puts the segment's pointer + index in the D
        # register, then achives its aim of either pushing RAM[seg+index]
        # to the stack or poping the stack to RAM[seg+index]. This will
        # work for ARG, LCL, THIS, and THAT segements
        #
        # INPUTS:
        # push - a string that defines 'push' or 'pop' the operation occuring
        # seg - a string that specifies the segment being worked with,
        # here it is LCL, ARG, THIS, or THAT
        # index - an integer that species the offset from the segment's base address
        # OUTPUTS:
        # a string of hack machine language instructions that performs push/pop seg index

        instr = "@%s, D=M, @%d, D=D+A," % (self.SEGLABEL[seg], int(index))
        if push == "push":
            return instr + ("A=D, D=M," + self.getPushD())
        elif push == "pop":
            return instr + "@R15, M=D," + self.getPopD() + "@R15, A=M, M=D,"
        else:
            print("Invalid Pointer Segment.")

    def constantSeg(self, push, seg, index, filename):
        # This function returns a sequence of machine language
        # instructions that places a constant value onto the
        # top of the stack. Note pop is undefined for this
        # function if seg is 'constant'. However, this function
        # also addresses seg = 'static', for which pop is defined.
        # NOTE: For seg = 'static' the filename is needed. This can be a global
        # or you can change the parameters to the function.

        # INPUTS:
        # push - a string that defines 'push' or 'pop' the operation occuring
        # seg - a string that specifies the segment being worked with, here 'constant' or 'static'
        # index - an integer that species the offset in general, but here is the literal value
        # OUTPUTS:
        # a string of hack machine language instructions that perform push/pop seg index
        # if push = 'push', seg = 'constant', and index = an integer
        # or if push = 'push' or 'pop', seg = 'static' and index = and integer

        if seg == "constant" and push == "push":
            return "@" + str(index) + "\nD=A\n" + self.getPushD()
        elif seg == "static":
            if push == "push":
                return "@" + str(filename) + "." + str(index) + "\nD=M\n" + self.getPushD()
            elif push == "pop":
                return self.getPopD() + "@" + str(filename) + "." + str(index) + "\nM=D\n"

    def fixedSeg(self, push, seg, index):
        # The following puts the segment's value + index in the D
        # register and then either pops from the stack to that address
        # or pushes from that address to the stack. Note that for fixed segments
        # the base address is 'fixed' as follows and is NOT a pointer:
        # pointer = 3
        # temp    = 5
        # INPUTS:
        # push - a string that defines 'push' or 'pop' the operation occuring
        # seg - a string that specifies the segment being worked with,
        # here 'pointer' or 'temp'
        # index - an integer that species the offset from the segment's base address
        # OUTPUTS:
        # a string of hack machine language instructions that performs push/pop seg index'

        if push == "push":
            if seg == "pointer":
                return "@%d, D=M," % (3 + int(index)) + self.getPushD()
            elif seg == "temp":
                return "@%d, D=M," % (5 + int(index)) + self.getPushD()
        elif push == "pop":
            if seg == "pointer":
                return self.getPopD() + "@%d, M=D," % (3 + int(index))
            if seg == "temp":
                return self.getPopD() + "@%d, M=D," % (5 + int(index))

        else:
            print("Not a fixed segment")

    SEGMENTS = {
        "constant": constantSeg,
        "static": constantSeg,
        "pointer": fixedSeg,
        "temp": fixedSeg,
        "local": pointerSeg,
        "argument": pointerSeg,
        "this": pointerSeg,
        "that": pointerSeg,

    }

    def uniqueLabel(self):
        # Returns a unique label.
        # Access global variable defined at the top of file, increment and return a unique label: UL_LABEL_NUMBER where label number is an integer.
        global LABEL_NUMBER
        LABEL_NUMBER += 1
        return "UL_" + str(LABEL_NUMBER)

    def arithTest(self, type):
        global c
        c += 1
        if type == "eq":
            return "D;JEQ"
        elif type == "lt":
            return "D;JLT"
        elif type == "gt":
            return "D;JGT"
        else:
            return "{} is in not a valid type".format(type)

        # return(getPopD() + ARITH_BINARY["sub"] + "\n@T" + str(c) + \n)

    # def parsFile(self, f):  # f = filehandle
    #     file = open(f, 'r')
    #     for line in file:
    #         tokens = line.split()
    #         # break line into tokens
    #         # push static 2
    #         # token[0] = 'push', [1] = 'static', [2] = '2'
    #         op = tokens[0]
    #         seg = tokens[1]
    #         index = tokens[2]

    #         # if token[0] in dictionary: ONE OF DICTS
    #         # do things
    #         if op in self.ARITH_BINARY.keys():
    #             pass
    #         pass
    #     # Terminate with infinite loop
    #     pass

    def parsFile(self, f):
        outString = ""
        for line in f:
            command = self.line2Command(line)  # strip any comments
            # Process the line if characters still exist after removing comments
            if command:
                # Split and strip the line into separated tokens stored in list args[].
                args = [x.strip() for x in command.split()]
                # Process a binary operation (add, sub, and, or)
                if args[0] in self.ARITH_BINARY.keys():
                    # Prepare to use the ARITH_BINARY dict by placing y in d-register and THEN processing the correct operation (remember ARITH_BINARY assumption of popD).
                    outString += self.getPopD()
                    outString += self.ARITH_BINARY[args[0]]
                # Process a unary operation (neg, not)
                # note: ARITH_UNARY dict processes stack values in-place.
                elif args[0] in self.ARITH_UNARY.keys():
                    outString += self.ARITH_UNARY[args[0]]
                # Process comparison operation (lt, gt, eq)
                elif args[0] in self.ARITH_TEST.keys():
                    # HACK ALERT - this shoul be a function, but I got lazy.
                    outString += self.getPopD()
                    # Use sub method to determine d-register value.
                    outString += self.ARITH_BINARY["sub"]
                    outString += self.getPopD()
                    # Return unique label via function so that multiple comparisons can occur in a single program by giving each unique labels.
                    l1 = self.uniqueLabel()
                    l2 = self.uniqueLabel()
                    # Create the asm code that carries out the comparison operation using unique labels generated above and a dictionary translation from ARITH_TEST.
                    js = "@%s, D;%s, @%s, D=0;JMP, (%s),D=-1,(%s)," % (
                        l1,
                        self.ARITH_TEST[args[0]],
                        l2,
                        l1,
                        l2,
                    )
                    outString += js
                    outString += self.getPushD()
                # Any valid vm code that makes it to this elif statement will be a call to push/pop using specified segments of memory.
                elif args[1] in self.SEGMENTS.keys():
                    # ALERT - this is a nice way of calling functions in a dictionary.
                    # Study this line closely.
                    # Actual function is stored as value for specified key rather than a function call. This allows clients to pass arguments to the value of a dict.
                    outString += self.SEGMENTS[args[1]
                                               ](args[0], args[1], args[2])
                # Account for invalid vm code and stop the program upon encountering. Any line that reaches this else statement is NOT valid vm code.
                else:
                    print("Unknown command!")
                    print(args)
                    # non-zero argument in sys.exit() indicates abnormal exit (error)
                    sys.exit(-1)
        # Use another unique label to ensure program termination using an infinite loop as prompted.
        l = self.uniqueLabel()
        outString += "(%s)" % (l) + ",@%s,0;JMP" % l  # Final endless loop

        # replace commas with newlines before returning
        return outString.replace(" ", "").replace(",", "\n")
    
    def getGoto(label):
        return "@{} 0;JMP".format(label)
    
    def getLabel(label):
        return "(" + label + ")"
    
    def ifGoto(self, label):
        self.getPopD() 
        pass


if __name__ == "__main__":
    filename = sys.argv[1].strip()
    hvm = VM(filename)
    # hvm.parsFile(filename)
