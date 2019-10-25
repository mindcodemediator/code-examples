#   Program Name: Recursion in MIPS                       #
#   Programmer: Val Prater				                       #
#   Date: 10/31/2018                                           #
################################################################ 
# Functional Description:
# Takes an integer between 1 and 12 and recurses by entered number
# minus one until it reaches zero
################################################################
	.data
Hello:		.asciiz		"Please enter a number between 0 and 12: "
Space:		.asciiz		"  "
WrgNum:		.asciiz		"Input out of range\n"
BaseTxt:	.asciiz		"Returning 1\n"
RecText:	.asciiz		"Recursing "
RetText:	.asciiz		"Returning "
NewLine:	.asciiz		"\n"
Bye:		.asciiz		"Goodbye!"
	.text


main:
		jal	Input					#get user input
		move $a0, $v0
		jal Recurse
		j Exit						#jump to end
Input:
		li		$v0, 4				#system call code for print string
		la		$a0, Hello			#load address of Hello prompt
		syscall						#print the prompt message
		li		$v0, 5				#system call code for Read Integer
		syscall						#reads value of N into $v0
		blt		$v0, $zero, WrongNum #if input less than zero, branch to wrong number prompt
		slti	$t0, $v0, 13		#check if input greater than 12
		beq		$t0, $zero WrongNum #if so, go to wrong number and get input again  
		#sw		$v0, 0($sp)			#add first value of n to the stack
		jr		$ra					#return to calling function
Recurse:
		#stack operations
		addiu	$sp, $sp, -12
		sw		$ra, 0($sp)			#keep $ra stored for this call
		sw		$a0, 4($sp)			#store n in next spot. keep last spot reserved for answer
		move	$a1, $a0			#store n in a1 to pass to space functions
		
		#Pre recursion printing
		jal		PrtSpcLp			#Print 2n spaces
		lw		$ra, 0($sp)
		li		$v0, 4				#system call code for print string
		la		$a0, RecText		#load address of recursion prompt 
		syscall						#print the prompt message		
		li		$v0, 1				#system call code for print int 
		lw		$a0, 4($sp)			#print what is in s0
		syscall
		li		$v0, 4				#system call code for print string
		la		$a0, NewLine			#load address of new line prompt 
		syscall	
		
		#check cases
		lw		$a0, 4($sp)			#put n back into a0
		beq		$a0, $zero, Base	#Base Case, will exit this function

				
		#recurse on n-1
		addi	$a0, $a0, -1	#a0 = n-1
		jal		Recurse			

		#equation
		lw		$t0, 4($sp)		#t0 = N
		addiu	$sp, $sp, -4	#get recursion result
		lw		$t1, 0($sp)		#t1 = Recurse(n-1)
		addiu	$sp, $sp, 4		#restore stack to current call
		mul		$t1, $t1, $t0	#multiply, because we checked input before recursion, this will not overflow so this is n * Recurse(n-1)
		addi	$t1, $t1, 1		#last step of equation is to add one
		sw		$t1, 8($sp)		#put answer in last stack spot
		

		
		#post recursion printing
		lw		$a1, 4($sp)
		jal	PrtSpcLp				#Print 2n spaces
		li		$v0, 4				#system call code for print string
		la		$a0, RetText		#load address of returning prompt 
		syscall						#print the prompt message
		li		$v0, 1				#system call code for print int 
		move	$a0, $t1			#print the answer
		syscall
		li		$v0, 4				#system call code for print string
		la		$a0, NewLine		#load address of recursion prompt 
		syscall

		#housekeeping
		lw		$ra, 0($sp)
		addiu	$sp, $sp, 12
		move	$a0, $t1			#put ans into a0
		jr		$ra
WrongNum:
		li		$v0, 4				#system call code for print string
		la		$a0, WrgNum			#load address of base prompt
		syscall						#print the prompt message
		j Input
Base:
		li		$v0, 4				#system call code for print string
		la		$a0, BaseTxt		#load address of wrong num prompt
		syscall						#print the prompt message
		ori		$t1, $zero, 1		#set $t1 to 1 
		sw		$t1, 8($sp)			#set base case to 1.
		addiu	$sp, $sp, 12		#reset stack
		jr		$ra					#return
PrtSpcLp:
		slti	$t2, $a1, 1			#set if less than one, don't print space
		beq		$t2, $zero, PrintDbl
		jr		$ra
PrintDbl:
		li		$v0, 4				#system call code for print string
		la		$a0, Space			#load address of recursion prompt 
		syscall
		addi	$a1, $a1, -1		#decrement n counter
		j PrtSpcLp					#go back to print space loop

Exit:
		li		$v0, 4 				#system call code for Print string
		la		$a0, Bye			#load address of msg into $a0
		syscall
		li		$v0, 10				#terminate program run  
		syscall						#return control to system