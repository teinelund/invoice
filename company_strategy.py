#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Company Strategy module
#

from os.path import join
from os import linesep
import sys
import codecs

class CompanyInfo:

	def __init__(self):
		self.id = None
		self.name = None
		self.ocr = None
		self.giro = None
		self.comment = None
		return


class LineParseError(StandardError):
	pass


class CompanyStrategy:

	def __init__(self):
		self.company_list = []
		self.dot_invoice_folder_path = None
		return


	#
	# company.txt
	#   Contains all parties that sends invoice to me.
	#
	#   id - unique integer number, starting from 1 and increasing by row. Mandatory. Set automaticaly by the command 'add'. Not by user input.
	#   company name - Company name. Mandatory
	#   ocr - OCR number. Optional
	#   giro - Bankgiro or Plusgiro. Mandatory
	#   comment - Optional
	#
	def get_header_in_file(self):
		return u"id, company name, ocr, giro, comment"


	def do_strategy(self, action, dot_invoice_folder_path):
		self.dot_invoice_folder_path = dot_invoice_folder_path
		self.read_file()
		if action == "list" or action == "l":
			self.list_companies()
		elif action == "add" or action == "a":
			self.add_company()
		elif action == "change" or action == "c":
			print "Not yet implemented"
			pass
		elif action == "delete" or action == "d":
			print "It is not possible to delete a company information."
			pass
		return

	def list_companies(self):
		self.sort_by_company_name()
		column_widths = self.calculate_column_widths()
		title = "{:<5}   {:<" + str(column_widths[0]) + "}   {:<" + str(column_widths[1]) + "}   {:<" + str(column_widths[2]) + "}   {:<" + str(column_widths[3]) + "}"
		print title.format("Index", "Company name", "OCR", "Giro", "Comment")
		index = 1
		row = u"{:>4}    {:<" + str(column_widths[0]) + u"}   {:<" + str(column_widths[1]) + u"}   {:<" + str(column_widths[2]) + u"}   {:<" + str(column_widths[3]) + u"}"
		for company_info in self.company_list:
			print row.format(index, company_info.name[0:30], company_info.ocr[0:30], company_info.giro[0:30], company_info.comment[0:30])
			index = index + 1
		return


	def add_company(self):
		next_id = 1
		if len(self.company_list) > 0:
			next_id = self.company_list[-1].id + 1	# TODO: Search the whole list and find the highest. Add one to that.
		print "Add company invoice information"
		print "-------------------------------"
		print "You will be asked questions about: Company name, OCR number, GIRO number and a comment."
		print "Company name and GIRO are mandatory. OCR number and comment are optional."
		answer = raw_input("Do you want to list current stored company information? [y/n/q = quit] ")
		if answer == "y" or answer == "Y":
			self.list_companies()
			print ""
		elif answer == "q" or answer == "Q":
			sys.exit(0)
		answer = raw_input("Company name (Mandatory)? Example: 'Telenor' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		name = unicode(answer.decode('utf-8'))
		answer = raw_input("OCR number (Optional)? Example: '00454322554' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		ocr = unicode(answer.decode('utf-8'))
		answer = raw_input("Giro number (Mandatory)? Example: '5564-2344' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		giro = unicode(answer.decode('utf-8'))
		answer = raw_input("Comment (Optional)? Example: 'Bredbandsfaktura' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		comment = unicode(answer.decode('utf-8'))
		answer = raw_input("Do you want to save this company information? [y/n/] ")
		if answer == "n" or answer == "N":
			sys.exit(0)
		self.sort_by_company_id()
		company_info = CompanyInfo()
		company_info.id = next_id
		company_info.name = name
		company_info.ocr = ocr
		company_info.giro = giro
		company_info.comment = comment
		self.company_list.append(company_info)
		self.save_company_list_to_file()
		return

	#
	# The company.txt file contains
	# Header: Company name, ocr, giro, comment
	#
	# company name contains string. May not be empty
	# ocr contains stirng. May be empty
	# giro contains string. May not be empty
	# comment contains string. May be empty
	#
	def read_file(self):
		copmany_file_path = join(self.dot_invoice_folder_path, "company.txt")
		file = codecs.open(copmany_file_path, encoding='utf-8', mode='r')
		index = 0
		for line in file:
			# NOTE! 'line' is of type unicode !
			if (len(line.strip())) == 0:
				continue
			if index > 0:
				company_info = self.get_company_info(index, line)
				self.company_list.append(company_info)
			index = index + 1
		file.close()
		return index


	def save_company_list_to_file(self):
		copmany_file_path = join(self.dot_invoice_folder_path, "company.txt")
		f = codecs.open(copmany_file_path, encoding='utf-8', mode='w')
		f.write(self.get_header_in_file() + linesep)
		for company_info in self.company_list:
			u_id = unicode(str(company_info.id))
			f.write(u_id + u", " + company_info.name + u", " + company_info.ocr + u", " + company_info.giro + u", " + company_info.comment + linesep)
		f.close()
		return



	def get_company_info(self, index, line):
		words = line.split(",")
		if len(words) != 5:
			raise LineParseError("Error at line: " + str(index) + ", in company.txt file. Line must have 5 columns. Line has: " + str(len(words)) + ", columns.")
		company_info = CompanyInfo()
		company_info.id = int(words[0].strip())
		company_info.name = words[1].strip()
		company_info.ocr = words[2].strip()
		company_info.giro = words[3].strip()
		company_info.comment = words[4].strip()
		return company_info


	def calculate_column_widths(self):
		column_widths = [12, 3, 4, 7]
		for company_info in self.company_list:
			if len(company_info.name) > column_widths[0]:
				column_widths[0] = len(company_info.name)
			if len(company_info.ocr) > column_widths[1]:
				column_widths[1] = len(company_info.ocr)
			if len(company_info.giro) > column_widths[2]:
				column_widths[2] = len(company_info.giro)
			if len(company_info.comment) > column_widths[3]:
				column_widths[3] = len(company_info.comment)
		index = 0
		for length in column_widths:
			if length > 30:
				column_widths[index] = 30
			index = index + 1
		return column_widths


	def sort_by_company_name(self):
		self.company_list = sorted(self.company_list, key=lambda company_info: company_info.name)
		return


	def sort_by_company_id(self):
		self.company_list = sorted(self.company_list, key=lambda company_info: company_info.id)
		return


	def get_company_info_given_id_ref(self, id):
		for company_info in self.company_list:
			if company_info.id == id:
				return company_info
		return 0

