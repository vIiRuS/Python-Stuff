#!/usr/bin/env python

"""
A simple interpreter for the brainfuck programming language.

ToDo:
	- add support for more input ways (via pipe)
	- bugfixing

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
import os.path

class Pythonfuck():

	def runInteractive(self, code=None):
		while True:
			code = raw_input("> ")
			if code != "q":
				self.pointer = 0
				self.field = [0, ]
				self.runCode(code)
				print ""
			else:
				print "Quit signal emitted. Closing down."
				break

	def runCode(self, code):
		if self.debug == True:
			print "executed code: ", code
		self.i = 0
		while self.i < len(code):
			if self.debug:
				print "Pointer: ", self.pointer, "   Command: ", code[self.i], "    Position: ", self.i
				print "Datafield: ", self.field
			try:
				self.brainfuck[code[self.i]](code)
				self.i += 1
				if self.debug:
					print ""
			except KeyError:
				self.i += 1
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
		self.inputstr = ""

		parser = argparse.ArgumentParser(description='Input some valid Brainfuck code.')
		parser.add_argument('--bf', '-b', type=str, dest='bfcode',
					help='The Brainfuck code that should be interpreted')
		parser.add_argument('--interactive', '-i', dest='mode', action='store_const',
					const=self.runInteractive, default=self.runInteractive,
					help='Select interactive mode (default when nothing is supplied)')
		parser.add_argument('--debug', '-d', dest='debug', action='store_const',
					const=True, default=False,
					help='activate debug mode')
		parser.add_argument('--file', '-f', dest='filename',
					help='supply a file name')
		args = parser.parse_args()
		self.debug = args.debug
		if args.bfcode != None:
			self.runCode(args.bfcode)
		if args.filename != None:
			if os.path.isfile(args.filename):
				f = open(args.filename)
				self.runCode(f.read())
		else:
			self.runInteractive()

	def incrPointer(self, code):
		if len(self.field)-1 <= self.pointer:
			self.field.append(0)
		self.pointer += 1
	
	def decrPointer(self, code):
		self.pointer -= 1
	
	def incrValue(self, code):
		if self.field[self.pointer] == 255:
			self.field[self.pointer] = 0
		else:
			self.field[self.pointer] += 1
	
	def decrValue(self, code):
		if self.field[self.pointer] == 0:
			self.field[self.pointer] = 255
		else:
			self.field[self.pointer] -= 1
	
	def printChar(self, code):
		if self.debug:
			sys.stdout.write("'" + chr(self.field[self.pointer]) + "'\n")
		else:
			sys.stdout.write(chr(self.field[self.pointer]))

	def getChar(self, code):
		if self.inputstr == "":
			char = raw_input("Input: ")
			self.inputstr += char
		if self.inputstr == "":
			self.field[self.pointer] = 0
		else:
			self.field[self.pointer] = ord(self.inputstr[0])
			self.inputstr = self.inputstr[1:]
	
	def bWhile(self, code):
		loopcount = 0
		if self.field[self.pointer] == 0:
			if self.debug:
				print "ignore loop"
			while code[self.i] != "]" and loopcount == 0:
				self.i += 1
				if code[self.i] == "[":
					loopcount += 1
				elif code[self.i] == "]": 
					loopcount -= 1
				
	
	def bEndWhile(self, code):
		loopcount = 0
		if self.field[self.pointer] != 0:
			if self.debug:
				print "execute loop again"
			self.i  -= 1
			while code[self.i] != "]" and loopcount == 0:
				self.i -= 1
				if code[self.i] == "[":
					loopcount += 1
				elif code[self.i] == "]": 
					loopcount -= 1
				
			
				

if __name__ == '__main__':
	Pythonfuck()