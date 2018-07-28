#!/usr/bin/env python

#################################################################
#                                                               #
#   Name: ch8da                                                 #
#                                                               #
#   Description: Chip8 disassembler                           #
#   Author: Mahdi Enan                                          #
#   Contact: mahdi.cie@gmail.com                                #
#   Reference: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM #                                #
#                                                               #
#   License: GNU General Public License (GPL) v2                #
#   http://www.gnu.org/licenses/old-licenses/gpl-2.0.html       #
#                                                               #
#   Copyright (C) 2018 Mahdi Enan                               #
#                                                               #
#################################################################
import sys
import argparse

class CH8DA:

	input_file = ""
	data = list()
	print_bytes = False
	verbose = False # TODO
	end_of_code = False
	clean_format = False

	def __init__(self):
		self.parse_args()
		print ";file:\t{}\n".format(self.input_file)
		self.disassemble()

	def parse_args(self):
		parser = argparse.ArgumentParser(description='Disassemble Chip8 programs.')
		parser.add_argument("input_file", help="The input file to be disassembled.")
		parser.add_argument("-p", "--print_bytes", help="print bytes.", action='store_true')
		parser.add_argument("-c", "--clean_format", help="clean format.", action='store_true')
		args = parser.parse_args()
		
		self.input_file = args.input_file
		self.print_bytes = args.print_bytes
		self.clean_format = args.clean_format

	def disassemble(self):
		self.feed_data()
		address_counter = 0x200
		
		for code in self.data:
			hexcode = int(code, 16)

			if not self.clean_format:
				sys.stdout.write("L{:03X}:\t".format(address_counter))

			if not self.end_of_code: # loop until endless jump
				if hexcode & 0xFFFF == 0x00E0:
					self.disassemble_0x00E0(hexcode)
				elif hexcode & 0xFFFF == 0x00EE:
					self.disassemble_0x00EE(hexcode)
				#elif hexcode & 0xF000 == 0x0000:
				#	print "DEBG"
				#	pass #self.disassemble_0x0XXX(hexcode)
				elif hexcode & 0xF000 == 0x1000:
					self.disassemble_0x1XXX(hexcode, address_counter)
				elif hexcode & 0xF000 == 0x2000:
					self.disassemble_0x2XXX(hexcode)
				elif hexcode & 0xF000 == 0x3000:
					self.disassemble_0x3XXX(hexcode)
				elif hexcode & 0xF000 == 0x4000:
					self.disassemble_0x4XXX(hexcode)
				elif hexcode & 0xF000 == 0x5000:
					self.disassemble_0x5XXX(hexcode)
				elif hexcode & 0xF000 == 0x6000:
					self.disassemble_0x6XXX(hexcode)
				elif hexcode & 0xF000 == 0x7000:
					self.disassemble_0x7XXX(hexcode)
				elif hexcode & 0xF00F == 0x8000:
					self.disassemble_0x8XX0(hexcode)
				elif hexcode & 0xF00F == 0x8001:
					self.disassemble_0x8XX1(hexcode)
				elif hexcode & 0xF00F == 0x8002:
					self.disassemble_0x8XX2(hexcode)
				elif hexcode & 0xF00F == 0x8003:
					self.disassemble_0x8XX3(hexcode)
				elif hexcode & 0xF00F == 0x8004:
					self.disassemble_0x8XX4(hexcode)
				elif hexcode & 0xF00F == 0x8005:
					self.disassemble_0x8XX5(hexcode)
				elif hexcode & 0xF00F == 0x8006:
					self.disassemble_0x8XX6(hexcode)
				elif hexcode & 0xF00F == 0x8007:
					self.disassemble_0x8XX7(hexcode)
				elif hexcode & 0xF00F == 0x800E:
					self.disassemble_0x8XXE(hexcode)
				elif hexcode & 0xF00F == 0x9000:
					self.disassemble_0x9XX0(hexcode)
				elif hexcode & 0xF000 == 0xA000:
					self.disassemble_0xAXXX(hexcode)
				elif hexcode & 0xF000 == 0xB000:
					self.disassemble_0xBXXX(hexcode)
				elif hexcode & 0xF000 == 0xC000:
					self.disassemble_0xCXXX(hexcode)
				elif hexcode & 0xF000 == 0xD000:
					self.disassemble_0xDXXX(hexcode)
				elif hexcode & 0xF0FF == 0xE09E:
					self.disassemble_0xEX9E(hexcode)
				elif hexcode & 0xE0A1 == 0xE0A1:
					self.disassemble_0xEXA1(hexcode)
				elif hexcode & 0xF0FF == 0xF007:
					self.disassemble_0xFX07(hexcode)
				elif hexcode & 0xF0FF == 0xF00A:
					self.disassemble_0xFX0A(hexcode)
				elif hexcode & 0xF0FF == 0xF015:
					self.disassemble_0xFX15(hexcode)
				elif hexcode & 0xF0FF == 0xF018:
					self.disassemble_0xFX18(hexcode)
				elif hexcode & 0xF0FF == 0xF01E:
					self.disassemble_0xFX1E(hexcode)
				elif hexcode & 0xF0FF == 0xF029:
					self.disassemble_0xFX29(hexcode)
				elif hexcode & 0xF0FF == 0xF033:
					self.disassemble_0xFX33(hexcode)
				elif hexcode & 0xF0FF == 0xF055:
					self.disassemble_0xFX55(hexcode)
				elif hexcode & 0xF0FF == 0xF065:
					self.disassemble_0xFX65(hexcode)
				else:
					#print "'" + str(hex(hexcode)) + "' is not implemented!"
					high = "{:04X}".format(hexcode)[:2]
					low = "{:04X}".format(hexcode)[2:]
					print "db #" + high + ", #" + low
			else: # end of code (start of data segment)
				high = "{:04X}".format(hexcode)[:2]
				low = "{:04X}".format(hexcode)[2:]
				print "db #" + high + ", #" + low
			address_counter += 2

	# SYS addr (0snnn)
	def disassemble_0x0XXX(self, hexcode): # wrong!
		print "GOTO 0x{:03X}".format(hexcode & 0x0FFF)

	# CLR
	def disassemble_0x00E0(self, hexcode): # untested
		print "CLS"

	# RET
	def disassemble_0x00EE(self, hexcode): # untested
		print "RET"


	# JP addr (1nnn)
	def disassemble_0x1XXX(self, hexcode, location): # ok
		destination = "{:03X}".format(hexcode & 0x0FFF)
		print "JP L" + destination
		if destination == hex(location)[2:]:
			self.end_of_code = True

	# CALL addr (2nnn)
	def disassemble_0x2XXX(self, hexcode): # recheck!
		print "CALL " + "#{:03X}".format(hexcode & 0x0FFF)

	# SE Vx, byte (3xkk)
	def disassemble_0x3XXX(self, hexcode): # ok
		print "SE " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "#" + "{:02X}".format(hexcode & 0x00FF)

	# SNE Vx, byte (4xkk)
	def disassemble_0x4XXX(self, hexcode): # recheck!
		print "SNE " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "#" + "{:02X}".format(hexcode & 0x00FF)

	# SE Vx, Vy (5xy0)
	def disassemble_0x5XXX(self, hexcode): # probably wrong!
		print "SE " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# LD Vx, byte (6xkk)
	def disassemble_0x6XXX(self, hexcode): # ok
		print "LD " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "#" + "{:02X}".format(hexcode & 0x00FF)

	# ADD Vx, byte (7xkk)
	def disassemble_0x7XXX(self, hexcode): # recheck!
		print "ADD " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "#" + "{:02X}".format(hexcode & 0x00FF)

	# LD Vx, Vy (8xy0)
	def disassemble_0x8XX0(self, hexcode): # ok
		print "LD " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# OR Vx, Vy (8xy1)
	def disassemble_0x8XX1(self, hexcode): # wrong!
		print "OR " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2]

	# AND Vx, Vy (8xy2)
	def disassemble_0x8XX2(self, hexcode): # wtf
		print "AND " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# XOR Vx, Vy (8xy3)
	def disassemble_0x8XX3(self, hexcode): # wrong!
		print "XOR " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# ADD Vx, Vy (8xy4)
	def disassemble_0x8XX4(self, hexcode): # ok
		print "ADD " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# SUB Vx, Vy (8xy5)
	def disassemble_0x8XX5(self, hexcode): # ok
		print "SUB " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# SHR Vx {, Vy} (8xy6)
	def disassemble_0x8XX6(self, hexcode): # untested
		print "SHR " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "#" + "{:02X}".format(hexcode & 0x00FF)

	# SUBN Vx, Vy (8xy7)
	def disassemble_0x8XX7(self, hexcode): # untested
		print "SUBN " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# SHL Vx {, Vy} (8xyE)
	def disassemble_0x8XXE(self, hexcode): # untested
		print "SHL " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# SNE Vx, Vy (9xy0)
	def disassemble_0x9XX0(self, hexcode): # untested
		print "SNE " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[:2][:1]

	# LD I, addr (Annn)
	def disassemble_0xAXXX(self, hexcode): # untested
		print "LD I, " + "#{:03X}".format(hexcode & 0x0FFF)

	# JP V0, addr (Bnnn)
	def disassemble_0xBXXX(self, hexcode): # untested
		print "JP v0, " + "#{:03X}".format(hexcode & 0x0FFF)

	# RND Vx, byte (Cxkk)
	def disassemble_0xCXXX(self, hexcode): # untested
		print "RND " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "#" + "{:02X}".format(hexcode & 0x00FF)

	# DRW Vx, Vy, nibble (Dxyn)
	def disassemble_0xDXXX(self, hexcode): # untested
		print "DRW " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", "\
					+ "v" + "{:01X}".format(hexcode & 0x00F0)[0:1] + ", "\
					+ "#" + "{:01X}".format(hexcode & 0x000F)

	# SKP Vx (Ex9E)
	def disassemble_0xEX9E(self, hexcode): # untested
		print "SKP " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1]

	# SKNP Vx (ExA1)
	def disassemble_0xEXA1(self, hexcode): # untested
		print "SKNP " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1]

	# LD Vx, DT (Fx07)
	def disassemble_0xFX07(self, hexcode): # untested
		print "LD " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", DT"
	# LD Vx, K (Fx0A)
	def disassemble_0xFX0A(self, hexcode): # untested
		print "LD " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", K"

	# LD DT, Vx (Fx15)
	def disassemble_0xFX15(self, hexcode): # untested
		print "LD DT, " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1]

	# LD ST, Vx (Fx18)
	def disassemble_0xFX18(self, hexcode): # untested
		print "LD ST, " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1]

	# ADD I, Vx (Fx1E)
	def disassemble_0xFX1E(self, hexcode): # untested
		print "ADD I, " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1]

	# LD F, Vx (Fx29)
	def disassemble_0xFX29(self, hexcode): # untested
		print "LD F, " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1]

	# LD B, Vx (Fx33)
	def disassemble_0xFX33(self, hexcode): # untested
		print "LD B, " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1]

	# LD [I], Vx (Fx55)
	def disassemble_0xFX55(self, hexcode): # untested
		print "LD [I], " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1]

	# LD Vx, [I] (Fx65)
	def disassemble_0xFX65(self, hexcode): # untested
		print "LD " + "v" + "{:01X}".format(hexcode & 0x0F00)[:1] + ", [I]"

	def feed_data(self):

		f = open(self.input_file, "rb")
		while 1:
			byte = f.read(2)
			if not byte:
				break
			else:
				hex_encoded = self.raw_encode(byte)
				self.data.append(hex_encoded)
				if self.print_bytes:
					print hex_encoded
		f.close()
		if self.print_bytes:
			sys.exit(0)

	def raw_encode(self, byte):
		return "".join("{:02X}".format(ord(c)) for c in byte)

if __name__ == "__main__":
	ch8da = CH8DA()