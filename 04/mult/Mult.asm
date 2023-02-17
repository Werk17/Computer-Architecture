// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Jump into the first STEP if R0 > 0.

@R2	//GO TO FINAL ANSWER BOX
M=0	//ZERO ANS BOX

@R0
D=M
@END
D;JEQ	//IF ONE PRODUCT IS ZERO

@R1
D=M
@END
D;JEQ	//IF ONE PRODUCT IS ZERO

@R0	
D=M	
@R3	
M=D	


(LOOP)
@R1	//GET 2ND NUM
D=M	//D HAS 2ND NUM

@R2	//GO TO FINAL ANSWER BOX
M=D+M	//RAM[2] NOW HAS 2ND NUMBER + ITS PREVIOUS VALUE

@R3	//GET 1ST NUM
M=M-1	//1ST NUM-1

D=M	
@LOOP	//WHERE TO JUMP TO
D;JGT	//JUMP		   


(END)
@END
0;JMP	//FOREVER LOOP