#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Invoice module
#

import argparse
import sys
from os.path import expanduser
from os.path import exists
from os.path import join
from os import mkdir
from invoice_strategy import InvoiceStrategy
from company_strategy import CompanyStrategy
from periodic_invoice_strategy import PeriodicInvoiceStrategy
from automatic_invoice_strategy import AutomaticInvoiceStrategy
from invoice_strategy import InvoiceStrategy
from os import linesep
import codecs

class Invoice:

	def __init__(self):
		self.args = None
		self.strategy = None
		self.dot_invoice_folder_path = None
		return


	def parse_args(self, sys_argv):
		length = len(sys_argv)
		args = sys_argv[1:length]	# Remove the first parameter in sys.argv, because that is the program name.
		self._parser = argparse.ArgumentParser(description="Stores payed invoices.", epilog="Henrik Teinelund (C) 2019.")
		self._parser.add_argument("--action", "-a", dest="action", choices=["add", "a", "list", "l", "change", "c", "delete", "d"], help="An action can be one of: add, list, change or delete.")
		self._parser.add_argument("--item", "-i", dest="item", choices=["invoice", "i", "company", "c", "periodic-invoice", "p", "automatic-invoice", "a"], help="An item can be one of: invoice, periodic-invoice, company or automatic-invoice.")
		self.args = self._parser.parse_args(args)
		return


	def validate_args(self):
		if self.args.item is None:
			return "NO_ITEM"
		if self.args.action is None:
			return "NO_ACTION"
		return ""

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
	# company.txt
	#   Contains all parties that sends invoice to me.
	#
	#   id - unique integer number, starting from 1 and increasing by row. Mandatory. Set automaticaly by the command 'add'. Not by user input.
	#   company name - Company name. Mandatory
	#   ocr - OCR number. Optional
	#   giro - Bankgiro or Plusgiro. Mandatory
	#   comment - Optional
	#
	#
	# automatic_invoice.txt
	#   Contains all invoices that are payed automaticaly, by giro.
	#
	#   id - unique integer number, starting from 1 and increasing by row. Mandatory. Set automaticaly by the command 'add'. Not by user input.
	#   company name ref - Company name reference. Mandatory
	#   amount - the amount in SEK. Mandatory
	#   start date - the start date when this invoice will be valid. If omitted, periodic invoice is valid until end date. Optional
	#   end date - the end date when this invoice will be invalid. If omitted, periodic invoice is valid from start date until forever. Optional
	#   pay day - the day in the month when this invoice should be payed. Mandatory
	#   frequency - montly, every second month, quartly, every 4:th month, half year, yearly. Mandatory
	#   start month - which month period starts each year. Integer. January starts at 1. Mandatory
	#   comment - Optional
	#
	# periodic_invoice.txt
	#   Contains all invoices that occurs in periodic frequency.
	#
	#   id - unique integer number, starting from 1 and increasing by row. Mandatory. Set automaticaly by the command 'add'. Not by user input.
	#   company name ref - Company name reference. Mandatory
	#   amount - the amount in SEK. Mandatory
	#   start date - the start date when this invoice will be valid. Optional
	#   end date - the end date when this invoice will be invalid. Optional
	#   frequency - montly, every second month, quartly, every 4:th month, half year, yearly. Mandatory
	#   start month - which month period starts each year. Integer. January starts at 1. Mandatory
	#   comment - Optional
	#
	def initialize_default_folders_and_files(self, home_path):
		return_message = []
		if not exists(home_path):
			return_message.append("HOME_PATH_DOES_NOT_EXIST")
			return return_message
		return_message.append("HOME_PATH_DOES_EXIST")
		self.dot_invoice_folder_path = join(home_path, ".invoice")
		if not exists(self.dot_invoice_folder_path):
			mkdir(self.dot_invoice_folder_path)
			return_message.append("DOT_INVOICE_FOLDER_CREATED")
		invoice_file_path = join(self.dot_invoice_folder_path, "invoice.txt")
		if not exists(invoice_file_path):
			strategy = InvoiceStrategy()
			f = codecs.open(invoice_file_path, encoding='utf-8', mode='w')
			f.write(strategy.get_header_in_file() + linesep)
			f.close()
			return_message.append("INVOICE_FILE_CREATED")
		copmany_file_path = join(self.dot_invoice_folder_path, "company.txt")
		if not exists(copmany_file_path):
			strategy = CompanyStrategy()
			f = codecs.open(copmany_file_path, encoding='utf-8', mode='w')
			f.write(strategy.get_header_in_file() + linesep)
			f.close()
			return_message.append("COMPANY_FILE_CREATED")
		automatic_invoice_file_path = join(self.dot_invoice_folder_path, "automatic_invoice.txt")
		if not exists(automatic_invoice_file_path):
			strategy = AutomaticInvoiceStrategy()
			f = codecs.open(automatic_invoice_file_path, encoding='utf-8', mode='w')
			f.write(strategy.get_header_in_file() + linesep)		# Mind that 'pay day' is on a day in the month. Not date!
			f.close()
			return_message.append("AUTOMATIC_INVOICE_FILE_CREATED")
		periodic_invoice_file_path = join(self.dot_invoice_folder_path, "periodic_invoice.txt")
		if not exists(periodic_invoice_file_path):
			strategy = PeriodicInvoiceStrategy()
			f = codecs.open(periodic_invoice_file_path, encoding='utf-8', mode='w')
			f.write(strategy.get_header_in_file() + linesep)
			f.close()
			return_message.append("PERIODIC_INVOICE_FILE_CREATED")
		return return_message


	def select_strategy(self):
		if self.args.item == "company" or self.args.item == "c":
			self.strategy = CompanyStrategy()
		elif self.args.item == "invoice" or self.args.item == "i":
			self.strategy = InvoiceStrategy()
		elif self.args.item == "periodic-invoice" or self.args.item == "p":
			self.strategy = PeriodicInvoiceStrategy()
		elif self.args.item == "automatic-invoice" or self.args.item == "a":
			self.strategy = AutomaticInvoiceStrategy()
		return



#
# The main method
#
if __name__ == "__main__":

	invoice = Invoice()
	invoice.parse_args(sys.argv)
	result = invoice.validate_args()
	if result == "NO_ITEM" or result == "NO_ACTION":
		print "--item and --action are mandatory. Use --help to display the help page."
	home = expanduser("~")
	message = invoice.initialize_default_folders_and_files(home)
	try:
		if message.index("HOME_PATH_DOES_NOT_EXIST") >= 0:
			print "User HOME folder does not exist for user."
			sys.exit(1)
	except ValueError:
			pass
	invoice.select_strategy()
	invoice.strategy.do_strategy(invoice.args.action, invoice.dot_invoice_folder_path)


	