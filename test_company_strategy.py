#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Test Company Strategy module
#

import unittest
from company_strategy import CompanyStrategy
from company_strategy import CompanyInfo
from company_strategy import LineParseError
import tempfile
import shutil
from os.path import join
from os import mkdir
from os import linesep


class TestCompanyStrategy(unittest.TestCase):

	#
	# strategy.get_company_info()
	#

	def test_get_company_info_where_all_columns_have_values(self):
		# initialize
		expected_id = "1"
		expected_name = "Uddevalla Energi"
		expected_ocr = "00543277320043"
		expected_giro = "5567-2356"
		expected_comment = "Sopavgift"
		line = expected_id + ", " + expected_name + ", " + expected_ocr + ", " + expected_giro + ", " + expected_comment
		strategy = CompanyStrategy()
		# test
		result = strategy.get_company_info(1, line)
		# verify
		self.assertEqual(result.id, int(expected_id))
		self.assertEqual(result.name, expected_name)
		self.assertEqual(result.ocr, expected_ocr)
		self.assertEqual(result.giro, expected_giro)
		self.assertEqual(result.comment, expected_comment)
		return


	def test_get_company_info_where_ocr_and_comment_contains_one_space_char(self):
		# initialize
		expected_id = "1"
		expected_name = "Uddevalla Energi"
		expected_ocr = ""
		expected_giro = "5567-2356"
		expected_comment = ""
		line = expected_id + ", " + expected_name + ", " + expected_ocr + ", " + expected_giro + ", " + expected_comment
		strategy = CompanyStrategy()
		# test
		result = strategy.get_company_info(1, line)
		# verify
		self.assertEqual(result.id, int(expected_id))
		self.assertEqual(result.name, expected_name)
		self.assertEqual(result.ocr, expected_ocr)
		self.assertEqual(result.giro, expected_giro)
		self.assertEqual(result.comment, expected_comment)
		return

	def test_get_company_info_where_ocr_and_comment_are_empty(self):
		# initialize
		expected_id = "1"
		expected_name = "Uddevalla Energi"
		expected_ocr = ""
		expected_giro = "5567-2356"
		expected_comment = ""
		line = expected_id + ", " + expected_name + "," + expected_ocr + ", " + expected_giro + "," + expected_comment
		strategy = CompanyStrategy()
		# test
		result = strategy.get_company_info(1, line)
		# verify
		self.assertEqual(result.id, int(expected_id))
		self.assertEqual(result.name, expected_name)
		self.assertEqual(result.ocr, expected_ocr)
		self.assertEqual(result.giro, expected_giro)
		self.assertEqual(result.comment, expected_comment)
		return

	def test_get_company_info_where_line_has_four_columns(self):
		# initialize
		expected_id = "1"
		expected_name = "Uddevalla Energi"
		expected_ocr = ""
		expected_giro = "5567-2356"
		line = expected_id + ", " + expected_name + "," + expected_ocr + ", " + expected_giro
		strategy = CompanyStrategy()
		# test
		try:
			result = strategy.get_company_info(1, line)
			# verify
			self.fail("Exception expected.")
		except LineParseError:
			pass
		return

	def test_get_company_info_where_line_has_six_columns(self):
		# initialize
		expected_id = "1"
		expected_name = "Uddevalla Energi"
		expected_ocr = ""
		expected_giro = "5567-2356"
		expected_comment = ""
		line = expected_id + ", " + expected_name + "," + expected_ocr + ", " + expected_giro + "," + expected_comment + ","
		strategy = CompanyStrategy()
		# test
		try:
			result = strategy.get_company_info(1, line)
			# verify
			self.fail("Exception expected.")
		except LineParseError:
			pass
		return


	#
	# strategy.read_file()
	#

	def test_read_file_where_file_contains_no_entries(self):
		# initialize
		dir = tempfile.mkdtemp()
		self.create_company_file_with_with_no_entries(dir)
		strategy = CompanyStrategy()
		strategy.dot_invoice_folder_path = dir
		# test
		rows = strategy.read_file()
		# verify
		self.assertEqual(len(strategy.company_list), 0)
		self.assertEqual(rows, 1)
		# cleanup
		shutil.rmtree(dir)
		return


	def create_company_file_with_with_no_entries(self, dir):
		company_file_path = join(dir, "company.txt")
		strategy = CompanyStrategy()
		f = open(company_file_path,"w")
		f.write(strategy.get_header_in_file() + linesep)
		f.close()


	def test_read_file_where_file_contains_two_entries(self):
		# initialize
		dir = tempfile.mkdtemp()
		self.create_company_file_with_two_entries(dir)
		strategy = CompanyStrategy()
		strategy.dot_invoice_folder_path = dir
		# test
		rows = strategy.read_file()
		# verify
		self.assertEqual(len(strategy.company_list), 2)
		self.assertEqual(rows, 3)
		self.assertEqual(strategy.company_list[0].id, 1)
		self.assertEqual(strategy.company_list[0].name, "Uddevalla Energi")
		self.assertEqual(strategy.company_list[0].ocr, "00543277320043")
		self.assertEqual(strategy.company_list[0].giro, "5567-2356")
		self.assertEqual(strategy.company_list[0].comment, "Sopavgift")
		self.assertEqual(strategy.company_list[1].id, 2)
		self.assertEqual(strategy.company_list[1].name, "Telenor")
		self.assertEqual(strategy.company_list[1].ocr, "")
		self.assertEqual(strategy.company_list[1].giro, "885674-3")
		self.assertEqual(strategy.company_list[1].comment, "")
		# cleanup
		shutil.rmtree(dir)
		return


	def create_company_file_with_two_entries(self, dir):
		company_file_path = join(dir, "company.txt")
		strategy = CompanyStrategy()
		f = open(company_file_path,"w")
		f.write(strategy.get_header_in_file() + linesep)
		f.write("1, Uddevalla Energi, 00543277320043, 5567-2356, Sopavgift" + linesep)
		f.write("2, Telenor,, 885674-3," + linesep)
		f.close()



	#
	# strategy.sort_by_company_name()
	#

	def test_sort_by_company_name(self):
		# initialize
		strategy = CompanyStrategy()
		strategy.company_list = self.create_company_list_1()
		# test
		strategy.sort_by_company_name()
		# verify
		self.assertEqual(len(strategy.company_list), 3)
		self.assertEqual(strategy.company_list[0].name, "Bredbbandsbolaget")
		self.assertEqual(strategy.company_list[1].name, "Telenor")
		self.assertEqual(strategy.company_list[2].name, "Uddevalla Energi")
		return


	def create_company_list_1(self):
		company_list = []
		company_info = CompanyInfo()
		company_info.id = 1
		company_info.name = "Telenor"
		company_list.append(company_info)
		company_info = CompanyInfo()
		company_info.id = 2
		company_info.name = "Uddevalla Energi"
		company_list.append(company_info)
		company_info = CompanyInfo()
		company_info.id = 3
		company_info.name = "Bredbbandsbolaget"
		company_list.append(company_info)
		return company_list


	#
	# strategy.sort_by_company_id()
	#

	def test_sort_by_company_id(self):
		# initialize
		strategy = CompanyStrategy()
		strategy.company_list = self.create_company_list_2()
		# test
		strategy.sort_by_company_id()
		# verify
		self.assertEqual(len(strategy.company_list), 3)
		self.assertEqual(strategy.company_list[0].name, "Telenor")
		self.assertEqual(strategy.company_list[1].name, "Uddevalla Energi")
		self.assertEqual(strategy.company_list[2].name, "Bredbbandsbolaget")
		return


	def create_company_list_2(self):
		company_list = []
		company_info = CompanyInfo()
		company_info.id = 3
		company_info.name = "Bredbbandsbolaget"
		company_list.append(company_info)
		company_info = CompanyInfo()
		company_info.id = 1
		company_info.name = "Telenor"
		company_list.append(company_info)
		company_info = CompanyInfo()
		company_info.id = 2
		company_info.name = "Uddevalla Energi"
		company_list.append(company_info)
		return company_list



	#
	# Test swedish characters in output
	#

	def test_swedish_characters_in_output_1(self):
		# initialize
		text = u"TEST"
		expected = u"TEST      "
		format_text = row = "{:<10}"
		# test
		result = format_text.format(text)
		# verify
		self.assertEqual(result, expected)
		return

	# Read: https://docs.python.org/2.7/howto/unicode.html
	# Read: https://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20
	def test_swedish_characters_in_output_2(self):
		# initialize
		text = u"TESTåä"
		expected = u"TESTåä    "
		format_text = row = "{:<10}"
		# test
		result = format_text.format(text)
		# verify
		self.assertEqual(result, expected)
		return



if __name__ == '__main__':
    unittest.main()
