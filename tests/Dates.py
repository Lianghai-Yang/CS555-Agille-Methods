import sys
sys.path.append('..')
import unittest
from Utils import Utils


class Dates(unittest.TestCase):
    def test_divorce_before_death(self):
        utils = Utils()
        self.assertTrue(utils.divorce_before_death('24 JUL 2018', '25 JUL 2018'))
        self.assertRaises(ValueError, utils.divorce_before_death, '25 JUL 2018', '24 JUL 2018')


if __name__ == '__main__':
    unittest.main()