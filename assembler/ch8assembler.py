#!/usr/bin/env python

#################################################################
#                                                               #
#   Name: ch8a                                                  #
#                                                               #
#   Description: very basic Chip8 assembler                     #
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

class CH8A:

	input_file = ""
	data = list()
	print_bytes = False
	verbose = False # TODO
	end_of_code = False
	clean_format = False

	def __init__(self):
		self.parse_args()
		self.assemble()

	def parse_args(self):
		parser = argparse.ArgumentParser(description='Assemble Chip8 programs.')
		parser.add_argument("input_file", help="The input file to be assembled.")
		parser.add_argument("output_file", help="The output file to write to.")
		parser.add_argument("-p", "--print_bytes", help="print bytes.", action='store_true')
		parser.add_argument("-c", "--clean_format", help="clean format.", action='store_true')

		args = parser.parse_args()
		
		self.input_file = args.input_file
		self.output_file = args.output_file
		self.print_bytes = args.print_bytes
		self.clean_format = args.clean_format


	def assemble(self):
		self.feed_data()
		chipcode = b""

		for instruction in self.data.split('\n'):
			if "GOTO" in instruction:
				code = "0" + instruction.split("0x")[1]
				chipcode += code.decode("hex")
			elif "CLS" in instruction:
				chipcode += "00E0".decode("hex")
			elif "RET" in instruction:
				chipcode += "00EE".decode("hex")
			elif "JP L" in instruction:
				code = "1" + instruction.split("L")[1]
				chipcode += code.decode("hex")
			elif "CALL" in instruction:
				code = "2" + instruction.split("#")[1]
				chipcode += code.decode("hex")
			elif "SE v" in instruction:
				if "#" in instruction:
					kk = instruction.split("#")[1]
					x = instruction.split("v")[1].split(",")[0]
					code = "3" + x + kk
					chipcode += code.decode("hex")
				else:
					_,x,y = instruction.split("v")
					x = x[0]
					code = "5" + x + y + "0"
					chipcode += code.decode("hex")
			elif "SNE v" in instruction:
				if "#" in instruction:
					kk = instruction.split("#")[1]
					x = instruction.split("v")[1].split(",")[0]
					code = "4" + x + kk
					chipcode += code.decode("hex")
				else:
					_,x,y = instruction.split("v")
					x = x[0]
					code = "9" + x + y + "0"
					chipcode += code.decode("hex")
			elif "LD v" in instruction:
				if "#" in instruction:
					kk = instruction.split("#")[1]
					x = instruction.split("v")[1].split(",")[0]
					code = "6" + x + kk
					chipcode += code.decode("hex")
				#TODO else
			elif "ADD v" in instruction:
				if "#" in instruction:
					kk = instruction.split("#")[1]
					x = instruction.split("v")[1].split(",")[0]
					code = "7" + x + kk
					chipcode += code.decode("hex")
				else:
					_,x,y = instruction.split("v")
					x = x[0]
					code = "8" + x + y + "4"
					chipcode += code.decode("hex")
			#TODO rest
			elif "DRW" in instruction:
				#Dxyn
				x,y,n = instruction.split(",")
				x = x.split("v")[1]
				y = y.split("v")[1]
				n = n.split("#")[1]
				code = "D" + x + y + n
				chipcode += code.decode("hex")
			#TODO rest
			elif "LD I" in instruction:
				code = "A" + instruction.split("#")[1]
				chipcode += code.decode("hex")
			#TODO rest
			elif "db" in instruction:
				high,low = instruction.split(",")
				high = high.split("#")[1]
				low = low.split("#")[1]
				code = high + low
				chipcode += code.decode("hex")
			else:
				print instruction
		self.write_data(chipcode)

	def write_data(self, chipcode):
		with open(self.output_file, 'wb') as f:
		    f.write(chipcode)

	def feed_data(self):
		with open(self.input_file, 'r') as file:
		    self.data=file.read()
		temp = ""
		for instruction in self.data.split('\n'):
			# remove comments
			if len(instruction) > 0 and instruction[0] == ";":
				continue
			# remove addresses
			if len(instruction) > 1:
				temp += instruction.split('\t')[1] + "\n"
		# remove trailing newline and assign to data
		self.data = temp[:-1]

	def raw_encode(self, byte):
		return "".join("{:02X}".format(ord(c)) for c in byte)

if __name__ == "__main__":
	ch8a = CH8A()