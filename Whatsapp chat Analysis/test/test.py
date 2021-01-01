try:

	import sys, os
	sys.path.append(os.path.abspath(os.path.join('..')))

	import unittest
	import numpy as np
	from numpy.testing import assert_almost_equal, assert_equal, assert_string_equal
	from numpy.testing import assert_allclose, assert_raises, assert_raises_regex
	from app import app
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

	pass