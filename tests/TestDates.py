import sys
sys.path.append('..')
import unittest
from Utils import Utils

class TestDates(unittest.TestCase):
    def test_divorce_before_death(self):
        utils = Utils()
        self.assertTrue(utils.divorce_before_death(divorce_time='24 JUL 2018', death_time='25 JUL 2018'))
        self.assertRaises(ValueError, utils.divorce_before_death, divorce_time='25 JUL 2018', death_time='24 JUL 2018')
        

if __name__ == '__main__':
    unittest.main()