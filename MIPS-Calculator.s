################################################################
#   Program Name: My First MIPS program                        #
#   Programmer: Val Prater				                       #
#   Date: 10/27/2018                                           #
################################################################
# Functional Description:
# A calculator program. Inputs an integer, an operator, and 
# another integer and outputs the answer if all inputs are valid
################################################################
	.data
Hello:	.asciiz		"Welcome to my Calculator.\n"
###Prompts###
Int:	.asciiz		"Int: "
Op:		.asciiz		"Op: "
Ans:	.asciiz		"--------------\n"
###Helper strings###
Buff:	.asciiz		"   "
OpStr:	.asciiz		"ec+-*/%"
NewL:	.asciiz		"\n"
###Error Messages###
ZerErr: .asciiz		"Attempting to divide by zero. Please enter a new divisor\n"
OvErr:	.asciiz		"Overflow, state reset to zero\n"
OpErr:	.asciiz		"Invalid operator, please enter +, -, *, /, or %. Also c for clear & e for exit\n"
Bye:	.asciiz		"\nGood bye. Thanks for checking out my calculator."
		.globl	main
		.text
main:
		li		$v0, 4			#system call code for print string
		la		$a0, Hello		#load address of greeting message into $a0
		syscall					#print the prompt message
		jal GetInt				#prompt user for integer
		move	$s0, $v0		#move $v0 to $s0
Loop:
		li		$v0, 4			#system call code for print string  GET OPERATOR
		la		$a0, Op			#load address of operator prompt into $a0
		syscall					#print the prompt message
		li		$v0, 8			#system call code for Read String
		la		$a0, Buff		#load address of buffer string into a0 argument
		li		$a1, 3			#load size of string into a1 argument
		syscall					#get String
		la		$t0, Buff		#load buffer which should now contain inputted string
		lb		$t1, 0($t0)		#get first byte which should be operator
		### operator comparisons ###
		la		$t2, OpStr		#load in string of operators
		lb		$t3, 0($t2)		#load 'e' into t3 comparator
		beq		$t1, $t3, End   #branch to end
		lb		$t3, 1($t2)		#load 'c' into t3 comparator	
		beq		$t1, $t3, Clear #clear state
		lb		$t3, 2($t2)		#load + into t3
		beq		$t1, $t3, Add	#branch to add
		lb		$t3, 3($t2)		#load - into t3
		beq		$t1, $t3, Sub	#branch to sub
		lb		$t3, 4($t2)		#load * into t3
		beq		$t1, $t3, Mult	#branch to Mult
		lb		$t3, 5($t2)		#load / into t3
		beq		$t1, $t3, Div	#branch to div
		lb		$t3, 6($t2)		#load % into t3
		beq		$t1, $t3, Mod 	#branch to mod
		li		$v0, 4			#IF it gets this far, an invalid operator was entered, display error and re-prompt
		la		$a0, OpErr		#load address of message into $a0
		syscall					#print the prompt message
		j Loop					#return to top of Loop to get operator again
GetInt:
		li		$v0, 4			#system call code for print string  GET FIRST INT
		la		$a0, Int		#load address of Int prompt
		syscall					#print the prompt message
		li		$v0, 5			#system call code for Read Integer
		syscall					#reads value of N into $v0
		jr $ra					#return to calling function

Add:
		jal GetInt				#get second integer which is now stored in $v0
		add $s0, $s0, $v0		#perform addition
		jal Print				#print answer
		j Loop					#return to get operator
Sub:
		jal GetInt				#get second integer which is now stored in $v0
		sub $s0, $s0, $v0		#perform subtraction
		jal Print				#print answer
		j Loop					#return to get operator
Mult:
		jal GetInt				#get second integer which is now stored in $v0
		mult $s0, $v0			#perform multiplication
		mflo $s0				#set lower 32 bits to s0
		mfhi $t0				#set upper to temp to check for overflow
		bne $t0, $zero, Over	#branch to overflow message if anything is contained in upper 32 bits
		jal Print				#print answer
		j Loop					#return to get operator
Div:
		jal GetInt				#get second integer which is now stored in $v0
		beq $v0, $zero, DivZ	#if attempt to divide by zero
		div $s0, $v0			#perform division
		mflo $s0				#set state to quotient
		jal Print				#print answer
		j Loop					#return to get operator
DivZ:
		li		$v0, 4			#system call code for print string
		la		$a0, ZerErr		#load address of Zero Error msg
		syscall					#print the message
		j Div					#jump back to top of divide
Mod:	
		jal GetInt				#get second integer which is now stored in $v0
		beq $v0, $zero, ModZ	#if attempt to divide by zero
		div $s0, $v0			#perform division
		mfhi $s0				#return remainder
		jal Print				#print answer
		j Loop					#return to get operator
ModZ:
		li		$v0, 4			#system call code for print string
		la		$a0, ZerErr		#load address of Zero Error msg 
		syscall					#print the message
		j Mod					#jump back to top of mod
Over:
		li		$v0, 4			#system call code for print string
		la		$a0, OvErr		#load address of message into $a0
		syscall					#print the message
		j Clear
Print:
		li		$v0, 4			#system call code for print string
		la		$a0, Ans		#load address Answer msg
		syscall					#print the prompt message
		li		$v0, 1			#system call code for print int 
		move	$a0, $s0		#print what is in s0
		syscall
		li		$v0, 4			#system call code for print string
		la		$a0, NewL		#load address of New Line msg
		syscall					#print the prompt message
		jr $ra					#return to calling function
Clear:
		li		$s0, 0			#reset $s0
		jal Print				#print $s0
		j	Loop				#return to loop to get operator
End:
		li		$v0, 4			#system call code for Print string
		la		$a0, Bye		#load address of msg into $a0
		syscall					#print the string
		li		$v0, 10			#terminate program run  
		syscall					#return control to system
