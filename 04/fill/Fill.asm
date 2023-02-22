// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@color
M=0 // Declare color, initialized to white '0'

(LOOP)

    @SCREEN //Assign screen range
    D=A
    @pixels
    M=D

    @KBD // Assign keyboard address
    D=M
    @BLACKEN
    D;JGT // If greater than zero, make black (loop)

    @color  //assign to white if not already
    M=0 
    @COLORIZE
    0;JMP // color screen, unconditional jump

    (BLACKEN) // assign color to black
        @color
        M=-1 // 2's compliment for contant 1's

    (COLORIZE)
        @color
        D=M 
        @pixels
        A=M // pointer to start of pixel range, address to another address
        M=D // Colorize these pixels

        @pixels
        M=M+1 // Increment pixels by one until 
        D=M //    

        @24576  // Here, we decrement from the end of the screen to the 
        D=D-A   // beginning of the screen range until difference is less than 0
        @COLORIZE
        D;JLT

    @LOOP
    0;JMP
