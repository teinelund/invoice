#!/usr/bin/env python

#
# Test Invoice module
#

import unittest
from invoice import Invoice
import tempfile
import shutil
from os.path import dirname
import tempfile
import shutil
from os.path import join
from os.path import exists
from os import mkdir
from invoice_strategy import InvoiceStrategy
from company_strategy import CompanyStrategy

class ArgsMock:
		
		def __init__(self):
			self.item = None
			self.action = None
			return

class TestInvoice(unittest.TestCase):

	#
	# invoice.parse_args(args)
	#

	INVOICE_PY = "invoice.py"

	def test_parse_args_where_action_is_add_and_item_is_invoice(self):
		# initialize
		action = "add"
		item = "invoice"
		invoice = Invoice()
		args = [self.INVOICE_PY, "--action", action, "--item", item]
		# test
		invoice.parse_args(args)
		# verify
		self.assertEqual(invoice.args.action, action)
		self.assertEqual(invoice.args.item, item)
		return

	def test_parse_args_where_action_is_list_and_item_is_company(self):
		# initialize
		action = "list"
		item = "company"
		invoice = Invoice()
		args = [self.INVOICE_PY, "--action", action, "--item", item]
		# test
		invoice.parse_args(args)
		# verify
		self.assertEqual(invoice.args.action, action)
		self.assertEqual(invoice.args.item, item)
		return

	def test_parse_args_where_action_is_change_and_item_is_periodic_invoice(self):
		# initialize
		action = "change"
		item = "periodic-invoice"
		invoice = Invoice()
		args = [self.INVOICE_PY, "--action", action, "--item", item]
		# test
		invoice.parse_args(args)
		# verify
		self.assertEqual(invoice.args.action, action)
		self.assertEqual(invoice.args.item, item)
		return

	def test_parse_args_where_action_is_delete_and_item_is_automatic_invoice(self):
		# initialize
		action = "delete"
		item = "automatic-invoice"
		invoice = Invoice()
		args = [self.INVOICE_PY, "--action", action, "--item", item]
		# test
		invoice.parse_args(args)
		# verify
		self.assertEqual(invoice.args.action, action)
		self.assertEqual(invoice.args.item, item)
		return


	#
	# invoice.validate_args()
	#


	def test_validate_args_where_item_and_action_are_none(self):
		# initialize
		expected_result = "NO_ITEM"
		invoice = Invoice()
		invoice.args = ArgsMock()
		# test
		result = invoice.validate_args()
		# verify
		self.assertEqual(result, expected_result)
		return

	def test_validate_args_where_action_is_none(self):
		# initialize
		expected_result = "NO_ACTION"
		invoice = Invoice()
		invoice.args = ArgsMock()
		invoice.args.item = "company"
		# test
		result = invoice.validate_args()
		# verify
		self.assertEqual(result, expected_result)
		return

	def test_validate_args_where_item_and_action_are_set_to_valid_values(self):
		# initialize
		expected_result = ""
		invoice = Invoice()
		invoice.args = ArgsMock()
		invoice.args.item = "company"
		invoice.args.action = "add"
		# test
		result = invoice.validate_args()
		# verify
		self.assertEqual(result, expected_result)
		return


	#
	# invoice.initialize_default_folders_and_files(home_path)
	#


	def test_initialize_default_folders_and_files_where_home_path_does_not_exist(self):
		# initialize
		dir = dirname("/THIS/PATH/DOES/NOT/EXIST")
		invoice = Invoice()
		# test
		result = invoice.initialize_default_folders_and_files(dir)
		# verify
		self.assertTrue(result.index("HOME_PATH_DOES_NOT_EXIST") >= 0)
		return


	def test_initialize_default_folders_and_files_where_home_path_exist_but_not_folder_dot_invoice(self):
		# initialize
		dir = tempfile.mkdtemp()
		invoice = Invoice()
		# test
		result = invoice.initialize_default_folders_and_files(dir)
		# verify
		self.assertEqual(len(result), 6)
		try:
			self.assertTrue(result.index("HOME_PATH_DOES_NOT_EXIST") >= 0)
			self.fail("ValueError expected.")
		except ValueError:
			pass
		self.assertTrue(result.index("HOME_PATH_DOES_EXIST") >= 0)
		dot_invoice_folder_path = join(dir, ".invoice")
		self.assertEqual(exists(dot_invoice_folder_path), True)
		self.assertTrue(result.index("DOT_INVOICE_FOLDER_CREATED") >= 0)
		invoice_file_path = join(dot_invoice_folder_path, "invoice.txt")
		self.assertEqual(exists(invoice_file_path), True)
		self.assertTrue(result.index("INVOICE_FILE_CREATED") >= 0)
		company_file_path = join(dot_invoice_folder_path, "company.txt")
		self.assertEqual(exists(company_file_path), True)
		self.assertTrue(result.index("COMPANY_FILE_CREATED") >= 0)
		automatic_invoice_file_path = join(dot_invoice_folder_path, "automatic_invoice.txt")
		self.assertEqual(exists(automatic_invoice_file_path), True)
		self.assertTrue(result.index("AUTOMATIC_INVOICE_FILE_CREATED") >= 0)
		periodic_invoice_file_path = join(dot_invoice_folder_path, "periodic_invoice.txt")
		self.assertEqual(exists(periodic_invoice_file_path), True)
		self.assertTrue(result.index("PERIODIC_INVOICE_FILE_CREATED") >= 0)
		# cleanup
		shutil.rmtree(dir)
		return

	def test_initialize_default_folders_and_files_where_dot_invoice_folder_and_all_files_exist(self):
		# initialize
		dir = tempfile.mkdtemp()
		self.create_default_files_and_folders(dir)
		invoice = Invoice()
		# test
		result = invoice.initialize_default_folders_and_files(dir)
		# verify
		self.assertEqual(len(result), 1)
		try:
			self.assertTrue(result.index("HOME_PATH_DOES_NOT_EXIST") >= 0)
			self.fail("ValueError expected.")
		except ValueError:
			pass
		self.assertTrue(result.index("HOME_PATH_DOES_EXIST") >= 0)
		dot_invoice_folder_path = join(dir, ".invoice")
		self.assertEqual(exists(dot_invoice_folder_path), True)
		invoice_file_path = join(dot_invoice_folder_path, "invoice.txt")
		self.assertEqual(exists(invoice_file_path), True)
		# cleanup
		shutil.rmtree(dir)
		return

	def create_default_files_and_folders(self, dir):
		dot_invoice_folder_path = join(dir, ".invoice")
		mkdir(dot_invoice_folder_path)
		invoice_file_path = join(dot_invoice_folder_path, "invoice.txt")
		f = open(invoice_file_path,"w")
		f.write("Company name, pay date, amount, ocr, giro, comment")
		f.close()
		company_file_path = join(dot_invoice_folder_path, "company.txt")
		f = open(company_file_path,"w")
		f.write("Company name, ocr, giro, comment")
		f.close()
		automatic_invoice_file_path = join(dot_invoice_folder_path, "automatic_invoice.txt")
		f = open(automatic_invoice_file_path,"w")
		f.write("Company name, amount, start date, end date, pay day, frequency, comment")
		f.close()
		periodic_invoice_file_path = join(dot_invoice_folder_path, "periodic_invoice.txt")
		f = open(periodic_invoice_file_path,"w")
		f.write("Company name, amount, start date, end date, frequency, comment")
		f.close()
		return


	#
	# invoice.select_strategy()
	#

	def test_select_strategy_where_args_item_is_company(self):
		# initialize
		expected_result = ""
		invoice = Invoice()
		invoice.args = ArgsMock()
		invoice.args.item = "company"
		# test
		invoice.select_strategy()
		# verify
		self.assertTrue(isinstance(invoice.strategy, CompanyStrategy))
		return

	def test_select_strategy_where_args_item_is_invoice(self):
		# initialize
		expected_result = ""
		invoice = Invoice()
		invoice.args = ArgsMock()
		invoice.args.item = "invoice"
		# test
		invoice.select_strategy()
		# verify
		self.assertTrue(isinstance(invoice.strategy, InvoiceStrategy))
		return

	def test_select_strategy_where_args_item_is_c(self):
		# initialize
		expected_result = ""
		invoice = Invoice()
		invoice.args = ArgsMock()
		invoice.args.item = "c"
		# test
		invoice.select_strategy()
		# verify
		self.assertTrue(isinstance(invoice.strategy, CompanyStrategy))
		return

	def test_select_strategy_where_args_item_is_i(self):
		# initialize
		expected_result = ""
		invoice = Invoice()
		invoice.args = ArgsMock()
		invoice.args.item = "i"
		# test
		invoice.select_strategy()
		# verify
		self.assertTrue(isinstance(invoice.strategy, InvoiceStrategy))
		return



if __name__ == '__main__':
    unittest.main()
