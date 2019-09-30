import sys
sys.path.append('..')
import unittest
from Utils import Utils

class TestDates(unittest.TestCase):
    utils = Utils()
    
    def test_divorce_before_death(self):
        utils = self.utils
        self.assertTrue(utils.divorce_before_death(divorce_time='24 JUL 2018', death_time='25 JUL 2018'))
        self.assertRaises(ValueError, utils.divorce_before_death, divorce_time='25 JUL 2018', death_time='24 JUL 2018')
        
    def test_birth_before_marriage_of_parents(self):
        utils = self.utils
        self.assertTrue(utils.birth_before_marriage_of_parents(
            child_birth_date='24 JUL 1994',
            marriage_date='24 JUL 1990',
            divorce_date='24 JUL 2010'
        ))

        self.assertTrue(utils.birth_before_marriage_of_parents(
            child_birth_date='24 JUL 1994',
            marriage_date='24 JUL 1990',
            divorce_date='24 JUL 2010'
        ))

        self.assertRaises(ValueError, utils.birth_before_marriage_of_parents,
            child_birth_date='24 JUL 1994',
            marriage_date='24 JUL 1990',
            divorce_date='24 JUL 1993',
        )


if __name__ == '__main__':
    unittest.main()