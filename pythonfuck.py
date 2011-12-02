#!/usr/bin/env python

"""
A script to check the diff betweet the followers of two users


-----------------------------------------------------------------------------
"THE NERD-WARE LICENSE" (Revision 1):
<viirus@pherth.net> wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me/us a beer, mate or some food in return
Phillip Thelen
-----------------------------------------------------------------------------
"""

import sys
import argparse

class Pythonfuck():

	def runInteractive(self, code=None):
		while True:
			code = raw_input("> ")
			if code != "q":
				self.pointer = 0
				self.field = [0, ]
				self.runCode(code)
			else:
				print "Quit signal emitted. Closing down."
				break

	def runCode(self, code):
		for self.i, char in enumerate(code):
			if self.debug:
				print "Pointer: ", self.pointer, "   Command: ", char, "    Position: ", self.i
				print "Datafield: ", self.field
			try:
				self.brainfuck[char](code)
				if self.debug:
					print ""
			except KeyError:
				continue
		
	def __init__(self):

		self.brainfuck = {
			">" : self.incrPointer,
			"<" : self.decrPointer,
			"+" : self.incrValue,
			"-" : self.decrValue,
			"." : self.printChar,
			"," : self.getChar,
			"[" : self.bWhile,
			"]" : self.bEndWhile
		}

		self.pointer = 0
		self.field = [0, ]

		parser = argparse.ArgumentParser(description='Input some valid Brainfuck code.')
		parser.add_argument('code', metavar='B', type=str,
					help='The Brainfuck code that should be interpreted')
		parser.add_argument('-i', dest='mode', action='store_const',
					const=self.runInteractive, default=self.runCode,
					help='Switch to interactive mode (instead of interpreting the given brainfuck code and then exiting)')
		parser.add_argument('-d', dest='debug', action='store_const',
					const=True, default=False,
					help='activate debug mode')
		args = parser.parse_args()
		self.debug = args.debug
		args.mode(args.code)

	def incrPointer(self, code):
		if len(self.field)-1 <= self.pointer:
			self.field.append(0)
		self.pointer += 1
	
	def decrPointer(self, code):
		if self.pointer > 0:
			self.pointer -= 1
		else:
			print "ERROR: You can't have a negative pointer"
	
	def incrValue(self, code):
		self.field[self.pointer] += 1
	
	def decrValue(self, code):
		self.field[self.pointer] -= 1
	
	def printChar(self, code):
		if self.debug:
			sys.stdout.write("'" + chr(self.field[self.pointer]) + "'\n")
		else:
			sys.stdout.write(chr(self.field[self.pointer]))

	def getChar(self, code):
		char = raw_input("Input: ")
		if char == "":
			self.field[self.pointer] = 0
		else:
			self.field[self.pointer] = ord(char)
	
	def bWhile(self, code):
		loopcount = 0
		loopcounter = 0
		if self.field[self.pointer] == 0:
			if self.debug:
				print "ignore loop"
			while code[self.i + loopcounter] != "]" and loopcount == 0:
				loopcounter += 1
				if code[self.i] == "[":
					loopcount += 1
				elif code[self.i] == "]": 
					loopcount -= 1
				
	
	def bEndWhile(self, code):
		loopcount = 0
		loopcounter = 0
		loopcode = "]"
		if self.field[self.pointer] != 0:
			if self.debug:
				print "execute loop again"
			while True:
				loopcounter += 1
				loopcode += code[self.i-loopcounter]
				if code[self.i-loopcounter] == "[" and loopcount == 0:
					break

				if code[self.i-loopcounter] == "]":
					loopcount += 1
				elif code[self.i-loopcounter] == "[": 
					loopcount -= 1
				
				if self.debug:
					print "###", self.i-loopcounter, code[self.i-loopcounter], loopcount
			self.runCode(loopcode[::-1])
				

if __name__ == '__main__':
	Pythonfuck()