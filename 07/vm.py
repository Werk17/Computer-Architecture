import os
import re
import sys

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


def getPushD():
    D = "@SP, AM=M+1, A=A-1, M=D,"
    return D


def getPopD():
    D = "@SP, AM=M-1, D=M,"
    return D


def pointerSeg(push, seg, index):
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

    instr = "@%s, D=M, @%d, D=D+A," % (SEGLABEL[seg], int(index))
    if push == "push":
        return instr + ("A=D, D=M," + getPushD())
    elif push == "pop":
        return instr + "@R15, M=D," + getPopD() + "@R15, A=M, M=D,"
    else:
        print("Invalid Pointer Segment.")


def constantSeg(push, seg, index):
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
    global filename

    if seg == "constant" and push == "push":
        return "@" + str(index) + "\nD=A\n" + getPushD()
    elif seg == "static":
        if push == "push":
            return "@" + str(filename) + "." + str(index) + "\nD=M\n" + getPushD()
        elif push == "pop":
            return getPopD() + "@" + str(filename) + "." + str(index) + "\nM=D\n"


def fixedSeg(push, seg, index):
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
            return "@%d, D=M," % (3 + int(index)) + getPushD()
        elif seg == "temp":
            return "@%d, D=M," % (5 + int(index)) + getPushD()
    elif push == "pop":
        if seg == "pointer":
            return getPopD() + "@%d, M=D," % (3 + int(index))
        if seg == "temp":
            return getPopD() + "@%d, M=D," % (5 + int(index))

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


def line2Command(l):
    # This function just strips commands that follow comments.
    return l[: l.find("//")].strip()


def uniqueLabel():
    # Returns a unique label.
    # Access global variable defined at the top of file, increment and return a unique label: UL_LABEL_NUMBER where label number is an integer.
    global LABEL_NUMBER
    LABEL_NUMBER += 1
    return "UL_" + str(LABEL_NUMBER)


def parsFile(f):
    outString = ""
    for line in f:
        command = line2Command(line)  # strip any comments
        # Process the line if characters still exist after removing comments
        if command:
            # Split and strip the line into separated tokens stored in list args[].
            args = [x.strip() for x in command.split()]
            # Process a binary operation (add, sub, and, or)
            if args[0] in ARITH_BINARY.keys():
                # Prepare to use the ARITH_BINARY dict by placing y in d-register and THEN processing the correct operation (remember ARITH_BINARY assumption of popD).
                outString += getPopD()
                outString += ARITH_BINARY[args[0]]
            # Process a unary operation (neg, not)
            # note: ARITH_UNARY dict processes stack values in-place.
            elif args[0] in ARITH_UNARY.keys():
                outString += ARITH_UNARY[args[0]]
            # Process comparison operation (lt, gt, eq)
            elif args[0] in ARITH_TEST.keys():
                # HACK ALERT - this shoul be a function, but I got lazy.
                outString += getPopD()
                # Use sub method to determine d-register value.
                outString += ARITH_BINARY["sub"]
                outString += getPopD()
                # Return unique label via function so that multiple comparisons can occur in a single program by giving each unique labels.
                l1 = uniqueLabel()
                l2 = uniqueLabel()
                # Create the asm code that carries out the comparison operation using unique labels generated above and a dictionary translation from ARITH_TEST.
                js = "@%s, D;%s, @%s, D=0;JMP, (%s),D=-1,(%s)," % (
                    l1,
                    ARITH_TEST[args[0]],
                    l2,
                    l1,
                    l2,
                )
                outString += js
                outString += getPushD()
            # Any valid vm code that makes it to this elif statement will be a call to push/pop using specified segments of memory.
            elif args[1] in SEGMENTS.keys():
                # ALERT - this is a nice way of calling functions in a dictionary.
                # Study this line closely.
                # Actual function is stored as value for specified key rather than a function call. This allows clients to pass arguments to the value of a dict.
                outString += SEGMENTS[args[1]
                                      ](args[0], args[1], args[2])
            # Account for invalid vm code and stop the program upon encountering. Any line that reaches this else statement is NOT valid vm code.
            else:
                print("Unknown command!")
                print(args)
                # non-zero argument in sys.exit() indicates abnormal exit (error)
                sys.exit(-1)
    # Use another unique label to ensure program termination using an infinite loop as prompted.
    l = uniqueLabel()
    outString += "(%s)" % (l) + ",@%s,0;JMP" % l  # Final endless loop

    # replace commas with newlines before returning
    return outString.replace(" ", "").replace(",", "\n")


def getGoto(label):
    return "@{}\n 0;JMP\n".format(label)


def getLabel(label):
    return "(" + label + ")"


def getIf_goto(label):
    return getPopD() + "@{}, D;JNE,".format(label)


def _getPushMem(src):
    # INPUT: src - a text string that is a symbol corresponding to a RAM address containing an address
    # OUTPUT: a text string that will result in the address in src being pushed
    # to the top of the stack.

    return "@{}\n D=M \n{}" % (src, getPushD())


def _getPushLabel(src):
    # INPUT: src - a text string that is some label, eg '(MAIN_LOOP)' which
    # corresponds to a ROM address in the symbol table.
    # OUTPUT: a text string that will result in the ROM address
    # to the top of the stack.
    return "@{}\n D=A\n {}\n" % (src, getPushD())


def _getPopMem(dest):
    # INPUT: src - a text string that is a symbol that corresponding to a RAM address containing an address
    # OUTPUT: a text string that pops the stack and places that value into the dest segment pointer
    return getPopD() + "@{}\n M=D\n" % (dest)


def _getMoveMem(src, dest):
    # INPUT: src - a text string that is a symbol corresponding to a RAM address containing an address
    # INPUT: dest- a text string that is a symbol corresponding to a RAM address containing an address
    # OUPUT: a text string that copies the address in src to dest
    return "@{}\n D=M\n @{}\n M=D\n" % (src, dest)


def getCall(funcName, nArgs):
    content = ""
    returnAddress = uniqueLabel(funcName)
    content += _getPushLabel(returnAddress)

    content += _getPushLabel(returnAddress)
    content += _getPushMem("LCL")
    content += _getPushMem("ARG")
    content += _getPushMem("THIS")
    content += _getPushMem("THAT")
    content += _getMoveMem("SP", "LCL")
    # save caller segment pointers, LCL, ARG, THIS, THAT
    # getPushMem()
    # _getMoveMem
    setArg = f"{nArgs + 5}, D=A, @SP, D=M-D, @ARG, M=D,"
    content += setArg
    content += getGoto(funcName)
    content += getLabel(returnAddress)
    return content


def getFunction(funcName, nLocals):
    # Ouput entry point '(funcName)'
    getLabel(funcName)
    # make n local variables equal to zero
    code = "D=0, "
    for i in int(nLocals):
        code += f"{getPushD()}"
    return code


def getReturn():
    # get address at the frames end, local at R15
    content = ""
    content += "@LCL, D=M, @5, A=D-A, D-M"
    content += "@R15, M=D,"
    content += getPopD() + "@ARG, A=M, M=D"
    content += "@ARG, D=M, @R14, M=D+1,"
    content += _getMoveMem("LCL", "SP")

    # popMem for this, that, arg, lcl
    content += _getPopMem("THAT")
    content += _getPopMem("THIS")
    content += _getPopMem("ARG")
    content += _getPopMem("LCL")

    _getMoveMem("@R14", "SP")

    return content


def getInit(sysinit=True):
    """
    Write the VM initialization code:
        Set the SP to 256.
        Initialize system pointers to -1.
        Call Sys.Init()
        Halt loop
    Passing sysinit = False oly sets the SP.  This allows the simpler
    VM test scripts to run correctly.
    """
    os = ""
    os += '@256,D=A,@SP,M=D,'
    if sysinit:
        # initialize ARG, LCL, THIS, THAT
        os += 'A=A+1,M=-1,A=A+1,M=-1,A=A+1,M=-1,A=A+1,M=-1,'
        os += getCall('Sys.init', 0)  # release control to init
        halt = uniqueLabel()
        os += '@%s, (%s), 0;JMP,' % (halt, halt)
    return os


if __name__ == "__main__":
    filename = sys.argv[1].strip()
    # ASM_File = filename.replace(".vm", ".asm")

    f = open(filename)
    print(parsFile(f))
    f.close()
