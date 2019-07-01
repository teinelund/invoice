#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Automatic Invoice Strategy module
#

from os.path import join
from os import linesep
from company_strategy import CompanyStrategy
import sys
import codecs

class AutomaticInvoiceInfo:

	def __init__(self):
		self.id = None
		self.name_ref = None
		self.amount = None
		self.start_date = None
		self.end_date = None
		self.pay_day = None
		self.frequency_index = None
		self.start_month_index = None
		self.comment = None
		return


class AutomaticInvoiceStrategy:

	def __init__(self):
		self.automatic_invoice_list = []
		self.company_strategy = CompanyStrategy()
		self.dot_invoice_folder_path = None
		self.months = [u"januari", u"feruari", u"mars", u"april", u"maj", u"juni", u"juli", u"augusti", u"september", u"oktober", u"november", u"december"]
		self.frequencies = [u"varje månad", u"var annan månad", u"kvartal", u"var 4:e månad", u"halvår", u"varje år"]
		return


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
	def get_header_in_file(self):
		return u"id, company name ref, amount, start date, end date, pay day, frequency, start month, comment"


	def do_strategy(self, action, dot_invoice_folder_path):
		self.dot_invoice_folder_path = dot_invoice_folder_path
		self.read_file()
		# Read all companies and put them in self.company_list.
		self.company_strategy.dot_invoice_folder_path = dot_invoice_folder_path
		self.company_strategy.read_file()

		if action == "list" or action == "l":
			self.list_automatic_invoices()
		elif action == "add" or action == "a":
			self.add_automatic_invoice()
		elif action == "change" or action == "c":
			print "Not yet implemented"
			pass
		elif action == "delete" or action == "d":
			print "It is not possible to delete a company information."
			pass
		return


	def list_automatic_invoices(self):
		column_widths = self.calculate_column_widths()
		title = "{:<5}   {:<" + str(column_widths[0]) + "}   {:<" + str(column_widths[1]) + "}   {:<" + str(column_widths[2]) + "}   {:<" + str(column_widths[3]) + "}   {:<" + str(column_widths[4]) + "}   {:<" + str(column_widths[5]) + "}   {:<" + str(column_widths[6]) + "}   {:<" + str(column_widths[6]) + "}"
		print title.format("Index", "Company name", "Amount", "Start date", "End date", "Pay day", "Frequency", "Start month", "Comment")
		index = 1
		row = u"{:>4}    {:<" + str(column_widths[0]) + u"}   {:<" + str(column_widths[1]) + u"}   {:<" + str(column_widths[2]) + u"}   {:<" + str(column_widths[3]) + u"}   {:<" + str(column_widths[4]) + u"}   {:<" + str(column_widths[5]) + u"}   {:<" + str(column_widths[6]) + u"}   {:<" + str(column_widths[7]) + u"}"
		for automatic_invoice_info in self.automatic_invoice_list:
			print row.format(index, self.company_strategy.get_company_info_given_id_ref(automatic_invoice_info.name_ref).name[0:30], automatic_invoice_info.amount[0:30], automatic_invoice_info.start_date[0:30], automatic_invoice_info.end_date[0:30], automatic_invoice_info.pay_day[0:30], self.frequencies[automatic_invoice_info.frequency_index][0:30], self.months[automatic_invoice_info.start_month_index][0:30], automatic_invoice_info.comment[0:30])
			index = index + 1
		return


	def add_automatic_invoice(self):
		next_id = 1
		if len(self.automatic_invoice_list) > 0:
			next_id = self.automatic_invoice_list[-1].id + 1
		print "Add automatic invoice information"
		print "--------------------------------"
		print "You will be asked questions about: Company name, amount, start date, end date, pay day, frequency, start month and comment."
		print "Company name, pay day, frequency and start month are mandatory. The others are optional."
		answer = raw_input("Do you want to list current stored peridoic invoice information? [y/n/q = quit] ")
		if answer == "y" or answer == "Y":
			self.list_automatic_invoices()
			print ""
		elif answer == "q" or answer == "Q":
			sys.exit(0)
		print "Stored companies:"
		self.company_strategy.list_companies()
		answer = raw_input("Index for company name ? Example: '5' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		index = int(answer)
		company_info = self.company_strategy.company_list[index - 1]
		company_name_ref = company_info.id
		print "'" + company_info.name + "' was selected."
		answer = raw_input("Amount in SEK (Optional)? Example: '359' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		amount = unicode(answer.decode('utf-8'))
		answer = raw_input("Start date (Optional)? Example: '2017-06-01' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		start_date = unicode(answer.decode('utf-8'))
		answer = raw_input("End date (Optional)? Example: '2019-12-31' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		end_date = unicode(answer.decode('utf-8'))

		answer = raw_input("Pay day (Mandatory)? The day which the invoice will be payed. Example: '28' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		pay_day = unicode(answer.decode('utf-8'))

		print "Index Frequency"
		index = 1
		for frequency in self.frequencies:
			print "  " + str(index) + "   " + frequency
			index = index + 1
		answer = raw_input("Frequency index: (Mandatory)? Example: '3' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		frequency_index = int(answer) - 1
		print "'" + self.frequencies[frequency_index] + "' was selected."
		print "Index Months"
		index = 1
		for month in self.months:
			print "  " + str(index) + "   " + month
			index = index + 1
		answer = raw_input("Start month index (Mandatory)? Example: '5' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		start_month_index = int(answer) - 1
		print "'" + self.months[start_month_index] + "' was selected."
		answer = raw_input("Comment (Optinal)? Example: 'Important' [q = quit] ")
		if answer == "q" or answer == "Q":
			sys.exit(0)
		comment = unicode(answer.decode('utf-8'))
		answer = raw_input("Do you want to save this company information? [y/n/] ")
		if answer == "n" or answer == "N":
			sys.exit(0)
		automatic_invoice_info = AutomaticInvoiceInfo()
		automatic_invoice_info.id = next_id
		automatic_invoice_info.name_ref = company_name_ref
		automatic_invoice_info.amount = amount
		automatic_invoice_info.start_date = start_date
		automatic_invoice_info.end_date = end_date
		automatic_invoice_info.pay_day = pay_day
		automatic_invoice_info.frequency_index = frequency_index
		automatic_invoice_info.start_month_index = start_month_index
		automatic_invoice_info.comment = comment
		self.automatic_invoice_list.append(automatic_invoice_info)
		self.save_automatic_invoice_list_to_file()
		return


	#
	# The automatic_invoice_strategy.txt file contains
	# Header: id, company name ref, amount, start date, end date, pay day, frequency, start month, comment
	#
	# id. An integer. May not be empty.
	# company name ref contains an integer. May not be empty
	# amount contains stirng. May be empty
	# start date contains string. May not be empty
	# end date contains string. May not be empty
	# frquency contains an integer. May not be empty.
	# start month contains an integer. May not be empty.
	# comment contains string. May be empty
	#
	def read_file(self):
		automatic_invoice_file_path = join(self.dot_invoice_folder_path, "automatic_invoice.txt")
		file = codecs.open(automatic_invoice_file_path, encoding='utf-8', mode='r')
		index = 0
		for line in file:
			if (len(line.strip())) == 0:
				continue
			if index > 0:
				automatic_invoice_info = self.get_automatic_invoice_info(index, line)
				self.automatic_invoice_list.append(automatic_invoice_info)
			index = index + 1
		file.close()
		return index


	def save_automatic_invoice_list_to_file(self):
		automatic_invoice_file_path = join(self.dot_invoice_folder_path, "automatic_invoice.txt")
		f = codecs.open(automatic_invoice_file_path, encoding='utf-8', mode='w')
		f.write(self.get_header_in_file() + linesep)
		for automatic_invoice_info in self.automatic_invoice_list:
			f.write(str(automatic_invoice_info.id) + u", " + str(automatic_invoice_info.name_ref) + u", " + automatic_invoice_info.amount + u", " + automatic_invoice_info.start_date + u", " + automatic_invoice_info.end_date + u", " + automatic_invoice_info.pay_day + u", " + str(automatic_invoice_info.frequency_index) + u", " + str(automatic_invoice_info.start_month_index) + u", " + automatic_invoice_info.comment + linesep)
		f.close()
		return


	def get_automatic_invoice_info(self, index, line):
		words = line.split(",")
		if len(words) != 9:
			raise LineParseError("Error at line: " + str(index) + ", in automatic_invoice.txt file. Line must have 9 columns. Line has: " + str(len(words)) + ", columns.")
		automatic_invoice_info = AutomaticInvoiceInfo()
		automatic_invoice_info.id = int(words[0].strip())
		automatic_invoice_info.name_ref = int(words[1].strip())
		automatic_invoice_info.amount = words[2].strip()
		automatic_invoice_info.start_date = words[3].strip()
		automatic_invoice_info.end_date = words[4].strip()
		automatic_invoice_info.pay_day = words[5].strip()
		automatic_invoice_info.frequency_index = int(words[6].strip())
		automatic_invoice_info.start_month_index = int(words[7].strip())
		automatic_invoice_info.comment = words[8].strip()
		return automatic_invoice_info


	# company name, amount, start date, end date, frequency, start month, comment
	def calculate_column_widths(self):
		column_widths = [12, 6, 10, 8, 7, 9, 11, 7]
		for automatic_invoice_info in self.automatic_invoice_list:
			if len(self.company_strategy.get_company_info_given_id_ref(automatic_invoice_info.name_ref).name) > column_widths[0]:
				column_widths[0] = len(self.company_strategy.get_company_info_given_id_ref(automatic_invoice_info.name_ref).name)
			if len(automatic_invoice_info.start_date) > column_widths[1]:
				column_widths[1] = len(automatic_invoice_info.start_date)
			if len(automatic_invoice_info.start_date) > column_widths[2]:
				column_widths[2] = len(automatic_invoice_info.start_date)
			if len(automatic_invoice_info.end_date) > column_widths[3]:
				column_widths[3] = len(automatic_invoice_info.end_date)
			if len(automatic_invoice_info.pay_day) > column_widths[4]:
				column_widths[4] = len(automatic_invoice_info.pay_day)
			if len(self.frequencies[automatic_invoice_info.frequency_index]) > column_widths[5]:
				column_widths[5] = len(self.frequencies[automatic_invoice_info.frequency_index])
			if len(self.months[automatic_invoice_info.start_month_index]) > column_widths[6]:
				column_widths[6] = len(self.months[automatic_invoice_info.start_month_index])
			if len(automatic_invoice_info.comment) > column_widths[7]:
				column_widths[7] = len(automatic_invoice_info.comment)
		index = 0
		for length in column_widths:
			if length > 30:
				column_widths[index] = 30
			index = index + 1
		return column_widths


