#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Invoice Strategy module
#
from os.path import join
from os import linesep
from company_strategy import CompanyStrategy
from company_strategy import LineParseError
from periodic_invoice_strategy import PeriodicInvoiceStrategy
import sys
import codecs
from datetime import date

class InvoiceInfo:

	def __init__(self):
		self.id = None
		self.name_ref = None
		self.periodic_invoice_ref = None
		self.pay_date = None
		self.amount = None
		self.ocr = None
		self.giro = None
		self.comment = None
		return

class InvoiceStrategy:

	def __init__(self):
		self.invoice_list = []
		self.company_strategy = CompanyStrategy()
		self.periodic_invoice_strategy = PeriodicInvoiceStrategy()
		self.dot_invoice_folder_path = None
		self.months = [u"januari", u"feruari", u"mars", u"april", u"maj", u"juni", u"juli", u"augusti", u"september", u"oktober", u"november", u"december"]
		self.frequencies = [u"varje månad", u"var annan månad", u"kvartal", u"var 4:e månad", u"halvår", u"varje år"]
		return


	def get_header_in_file(self):
		return u"company name ref, periodic invoice ref, pay date, amount, ocr, giro, comment"


	def do_strategy(self, action, dot_invoice_folder_path):
		self.dot_invoice_folder_path = dot_invoice_folder_path
		self.read_file()
		# Read all companies.
		self.company_strategy.dot_invoice_folder_path = dot_invoice_folder_path
		self.company_strategy.read_file()
		# Read all periodic invoices.
		self.periodic_invoice_strategy.dot_invoice_folder_path = dot_invoice_folder_path
		self.periodic_invoice_strategy.read_file()
		self.periodic_invoice_strategy.company_strategy.dot_invoice_folder_path = dot_invoice_folder_path
		self.periodic_invoice_strategy.company_strategy.read_file()

		if action == "list" or action == "l":
			self.list_invoices()
		elif action == "add" or action == "a":
			self.add_invoice()
		elif action == "change" or action == "c":
			print "Not yet implemented"
			pass
		elif action == "delete" or action == "d":
			print "It is not possible to delete a company information."
			pass
		return


	def list_invoices(self):
		column_widths = self.calculate_column_widths()
		title = "  {:<" + str(column_widths[0]) + "}   {:<" + str(column_widths[1]) + "}   {:<" + str(column_widths[2]) + "}   {:<" + str(column_widths[3]) + "}   {:<" + str(column_widths[4]) + "}   {:<" + str(column_widths[5]) + "}"
		print title.format("Company name", "Pay date", "Amount", "OCR", "Giro", "Comment")
		row = u"  {:<" + str(column_widths[0]) + u"}   {:<" + str(column_widths[1]) + u"}   {:<" + str(column_widths[2]) + u"}   {:<" + str(column_widths[3]) + u"}   {:<" + str(column_widths[4]) + u"}   {:<" + str(column_widths[5]) + u"}"
		for invoice_info in self.invoice_list:
			company_name = ""
			if (invoice_info.name_ref >= 0):
				company_name = self.company_strategy.get_company_info_given_id_ref(invoice_info.name_ref).name
			else:
				company_name = self.periodic_invoice_strategy.get_company_info_given_id_ref(invoice_info.periodic_invoice_ref).name
			print row.format(company_name[0:30], invoice_info.pay_date[0:30], invoice_info.amount[0:30], invoice_info.ocr[0:30], invoice_info.giro[0:30], invoice_info.comment[0:30])
		return


	def add_invoice(self):
		next_id = 1
		if len(self.invoice_list) > 0:
			next_id = self.invoice_list[-1].id + 1	# TODO: Search the whole list and find the highest. Add one to that.
		print "Add invoice information"
		print "-----------------------"
		print "You will be asked questions about: Company name, pay date, amount, OCR number, GIRO number and a comment."
		answer = raw_input("Is this invoice a periodic invoice or an ordinary invoice? [p/o/q = quit] ")
		name_ref = -1
		periodic_invoice_ref = -1
		ocr = ""
		giro = ""
		pay_date = date.today().isoformat()
		if answer == "q" or answer == "Q":
			sys.exit(0)
		elif answer == "p" or answer == "P":
			print "These are the pariodic invoices:"
			self.periodic_invoice_strategy.list_periodic_invoices()

			answer = raw_input("Index for pariodic invoice? Example: '5' [q = quit] ")
			if answer == "q" or answer == "Q":
				sys.exit(0)
			index = int(answer)
			periodic_invoice_info = self.periodic_invoice_strategy.periodic_invoice_list[index - 1]
			periodic_invoice_ref = periodic_invoice_info.id
			print "'" + self.company_strategy.get_company_info_given_id_ref(periodic_invoice_info.name_ref).name + "' was selected."
			ocr = self.company_strategy.get_company_info_given_id_ref(periodic_invoice_info.name_ref).ocr
			giro = self.company_strategy.get_company_info_given_id_ref(periodic_invoice_info.name_ref).giro
		else:
			# answer is equal 'o' or 'O'
			print "These are the companies stored:"
			self.company_strategy.list_companies()

			answer = raw_input("Index for companies? Example: '2' [q = quit] ")
			if answer == "q" or answer == "Q":
				sys.exit(0)
			index = int(answer)
			company_info = self.company_strategy.company_list[index - 1]
			name_ref = company_info.id
			print "'" + self.company_strategy.get_company_info_given_id_ref(name_ref).name + "' was selected."
		answer = raw_input("Do you want to use todays date? [y/n/q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		if answer == "n" or answer == "N":
			answer = raw_input("Enter a date in format YYYY-mm-dd. Example: '2019-06-25' (25:th of June 2019). No check is made that the date is valid. [q = quit] ")
			if answer == "q" or answer == "Q":
				sys.exit(0)
			pay_date = unicode(answer.decode('utf-8'))
		answer = raw_input("Enter amount in SEK? Example: '349' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		amount = unicode(answer.decode('utf-8'))
		if len(ocr) > 0:
			answer = raw_input("OCR number (Mandatory)? Example: '0045321223' [q = quit]. Default is " + ocr + ". Just pressing enter selects default ")
			if answer == "q" or answer == "Q":
				sys.exit(0)
			if len(answer) > 0:
				ocr = unicode(answer.decode('utf-8'))
		else:
			answer = raw_input("OCR number (Mandatory)? Example: '0045321223' [q = quit] ")
			if answer == "q" or answer == "Q":
				sys.exit(0)
			ocr = unicode(answer.decode('utf-8'))
		if len(giro) > 0:
			answer = raw_input("Giro number (Mandatory)? Example: '5564-2344' [q = quit]. Default is " + giro + ". Just pressing enter selects default ")
			if answer == "q" or answer == "Q":
				sys.exit(0)
			if len(answer) > 0:
				giro = unicode(answer.decode('utf-8'))
		else:
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
		invoice_info = InvoiceInfo()
		invoice_info.id = next_id
		invoice_info.name_ref = name_ref
		invoice_info.periodic_invoice_ref = periodic_invoice_ref
		invoice_info.pay_date = pay_date
		invoice_info.amount = amount
		invoice_info.ocr = ocr
		invoice_info.giro = giro
		invoice_info.comment = comment
		self.invoice_list.append(invoice_info)
		self.save_invoice_list_to_file()
		return

	#
	# invoice.txt
	#   Contains all payed invoices, but the automatic invoices.
	#
	#   id. An integer. May not be empty.
	#   company name ref - Referece number to company. Integer. Optional.
	#   periodic invoice ref - Reference to periodic_invoice. Integer. Optional.
	#   pay date - the date when the invoice is payed. Mandatory
	#   amount - the amount in SEK. If periodic invoice contains amount, this value is optional. If present, it overrides periodic invoice amount. If perioduc invoice is not present, this is mandatory.
	#   ocr - OCR number. If company contains ocr number, this is optional. If present, it overrides compant ocr. If company does not have ocr, then a value in this ocr is mandatory.
	#   comment - Optional
	#
	#   Note: When listing invoices, use the giro from company. Same for ocr. If ocr is empty, use ocr from company.
	#         One of Compant name ref and Periodic Invoice Ref is mandatory. Not both.
	#         When listing invoices, add automatic invoices to the list.
	#
	def read_file(self):
		invoice_file_path = join(self.dot_invoice_folder_path, "invoice.txt")
		file = codecs.open(invoice_file_path, encoding='utf-8', mode='r')
		index = 0
		for line in file:
			if (len(line.strip())) == 0:
				continue
			if index > 0:
				invoice_info = self.get_invoice_info(index, line)
				self.invoice_list.append(invoice_info)
			index = index + 1
		file.close()
		return index

	def save_invoice_list_to_file(self):
		invoice_file_path = join(self.dot_invoice_folder_path, "invoice.txt")
		f = codecs.open(invoice_file_path, encoding='utf-8', mode='w')
		f.write(self.get_header_in_file() + linesep)
		for invoice_info in self.invoice_list:
			f.write(str(invoice_info.id) + u", " + str(invoice_info.name_ref) + u", " + str(invoice_info.periodic_invoice_ref) + u", " + invoice_info.pay_date + u", " + invoice_info.amount + u", " + invoice_info.ocr + u", " + invoice_info.giro + u", " + invoice_info.comment + linesep)
		f.close()
		return


	def get_invoice_info(self, index, line):
		words = line.split(",")
		if len(words) != 8:
			raise LineParseError("Error at line: " + str(index) + ", in invoice.txt file. Line must have 8 columns. Line has: " + str(len(words)) + ", columns.")
		invoice_info = InvoiceInfo()
		invoice_info.id = int(words[0].strip())
		invoice_info.name_ref = int(words[1].strip())
		invoice_info.periodic_invoice_ref = int(words[2].strip())
		invoice_info.pay_date = words[3].strip()
		invoice_info.amount = words[4].strip()
		invoice_info.ocr = words[5].strip()
		invoice_info.giro = words[6].strip()
		invoice_info.comment = words[7].strip()
		return invoice_info


	# company name ref, periodic invoice ref, pay date, amount, ocr, comment
	def calculate_column_widths(self):
		column_widths = [12, 8, 6, 3, 4, 7]
		for invoice_info in self.invoice_list:
			if invoice_info.name_ref >= 0:
				if len(self.company_strategy.get_company_info_given_id_ref(invoice_info.name_ref).name) > column_widths[0]:
					column_widths[0] = len(self.company_strategy.get_company_info_given_id_ref(invoice_info.name_ref).name)
			if invoice_info.periodic_invoice_ref >= 0:
				if len(self.periodic_invoice_strategy.get_company_info_given_id_ref(invoice_info.periodic_invoice_ref).name) > column_widths[0]:
					column_widths[0] = len(self.periodic_invoice_strategy.get_company_info_given_id_ref(invoice_info.periodic_invoice_ref).name)
			if len(invoice_info.pay_date) > column_widths[1]:
				column_widths[1] = len(invoice_info.pay_date)
			if len(invoice_info.amount) > column_widths[2]:
				column_widths[2] = len(invoice_info.amount)
			if len(invoice_info.ocr) > column_widths[3]:
				column_widths[3] = len(invoice_info.ocr)
			if len(invoice_info.giro) > column_widths[4]:
				column_widths[4] = len(invoice_info.giro)
			if len(invoice_info.comment) > column_widths[5]:
				column_widths[5] = len(invoice_info.comment)
		index = 0
		for length in column_widths:
			if length > 30:
				column_widths[index] = 30
			index = index + 1
		return column_widths



