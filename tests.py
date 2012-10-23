import unittest
from view_helper import *

class Test_try_parse(unittest.TestCase):

	def test_valid_int(self):
		result = try_parse('5', int)
		self.assertEqual(result, 5)

	def test_invalid_with_provided_default(self):
		result = try_parse('b', int, 5)
		self.assertEqual(result, 5)

	def test_invalid_with_no_default(self):
		result = try_parse('b', int)
		self.assertEqual(result, None)


class Test_int_try_parse(unittest.TestCase):

	def test_int_try_parse_valid(self):
		result = int_try_parse('5')
		self.assertEqual(result, 5)

	def test_int_try_parse_invalid_with_provided_default(self):
		result = int_try_parse('b', 5)
		self.assertEqual(result, 5)

	def test_int_try_parse_invalid_with_no_default(self):
		result = int_try_parse('b')
		self.assertEqual(result, 0)


class Test_parse_query_string(unittest.TestCase):

	def test_with_valid_query_string(self):
		query_string = { 'page' : 2}
		func = lambda value, default : value
		result = parse_query_string(query_string, 'page', func)	
		self.assertEqual(result, 2)

	def test_with_nonexistent_key_and_no_provided_default(self):
		query_string = {}	
		func = None
		result = parse_query_string(query_string, 'page', func)
		self.assertEqual(result, None)

	def test_with_nonexistent_key_with_provided_default(self):
		query_string = {}	
		func = None
		result = parse_query_string(query_string, 'page', func, 5)
		self.assertEqual(result, 5)


class Test_create_pagination(unittest.TestCase):

	def test_for_one_page_only(self):
		total_count = 4
		number_to_skip = 0
		page_size = 4
		page_number = 1
		result = create_pagination(total_count, number_to_skip, page_size, page_number)
		self.assertEqual(result['previous'], False)
		self.assertEqual(result['next'], False)

	def test_for_two_pages_from_page_one(self):
		total_count = 5
		number_to_skip = 0
		page_size = 4
		page_number = 1
		result = create_pagination(total_count, number_to_skip, page_size, page_number)
		self.assertEqual(result['previous'], False)
		self.assertEqual(result['next'], True)

	def test_for_two_pages_from_page_two(self):
		total_count = 5
		number_to_skip = 4
		page_size = 4
		page_number = 2
		result = create_pagination(total_count, number_to_skip, page_size, page_number)
		self.assertEqual(result['previous'], True)
		self.assertEqual(result['next'], False)

	def test_for_three_pages_from_page_two(self):
		total_count = 9
		number_to_skip = 4
		page_size = 4
		page_number = 2
		result = create_pagination(total_count, number_to_skip, page_size, page_number)
		self.assertEqual(result['previous'], True)
		self.assertEqual(result['next'], True)

if __name__ == '__main__':
	unittest.main()