try:

	import sys, os
	sys.path.append(os.path.abspath(os.path.join('..', '..')))

	import unittest
	import numpy as np
	from numpy.testing import assert_almost_equal, assert_equal, assert_string_equal
	from numpy.testing import assert_allclose, assert_raises, assert_raises_regex

	from app import text_process, remove_system_generated_msgs, process_text, word_count
except Exception as e:
	print('Some modules are missing {}'.format(e))
	

class FlaskTestCase(unittest.TestCase):
	"""docstring for FlaskTestCase
		A class for unit-testing some of the function/method in the 
		app.py file

		Args:
			unittest.TestCase this allows the new class to inherit
			from the unittest module
	"""

	def test_text_process(self):
		actual = text_process('Abubakar.OlAyemi')
		expected = 'abubakarolayemi'
		self.assertEqual(actual, expected, f'Should be equal {expected}')

	def test_remove_system_generated_msgs(self):
		actual = remove_system_generated_msgs(['i like to love you', '=234 781929201 was removed', 'kenny was added', 
			'mehn today nah craze', 'ibrahim joined using this group something', 'soliu left', 'python streamlit >>>',
			 'message was deleted by me', 'hope it works out fine'])
		expected = ['i like to love you', 'mehn today nah craze', 'python streamlit >>>', 'hope it works out fine']
		assert_equal(actual, expected, 'should be of same length and must be equal')

	def test_process_text(self):
		actual = process_text('../../../WhatsApp Chat with Abdul-Azeez.txt')
		actual = actual.columns.tolist()
		expected = ['Date', 'Time', 'Sender', 'Content', 'chat_length', 'word_count', 'day_name', 'month_name', 'year']
		self.assertEqual(actual, expected, 'should be equal')


	def test_word_count(self):
		actual = word_count('i love eating bread and beans yumm')
		expected = 7
		assert actual == expected

if __name__ == '__main__':
	unittest.main()