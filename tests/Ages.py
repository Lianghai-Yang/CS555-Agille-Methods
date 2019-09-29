import sys
sys.path.append('..')
import unittest
from Utils import Utils

class Ages(unittest.TestCase):
    def test_parents_not_too_old(self):
        utils = Utils()
        self.assertTrue(utils.parents_not_too_old(
            father_birth_date='24 JUL 1984',
            mother_birth_date='25 JUL 1985',
            child_birth_date='24 JUN 2019',
        ))
        self.assertRaises(ValueError, utils.parents_not_too_old, 
            father_birth_date='25 JUL 1948',
            mother_birth_date='24 JUL 1938', # greater than 60 years older than her child
            child_birth_date='24 JUL 2018',
        )

    def test_marriage_after_14(self):
        utils = Utils()
        self.assertTrue(utils.marriage_after_14(
            husband_birth_date='24 JUL 1984',
            wife_birth_date='25 JUL 1985',
            marriage_date='24 JUN 2000',
        ))
        self.assertRaises(ValueError, utils.marriage_after_14(
            husband_birth_date='25 JUL 2012',
            wife_birth_date='24 JUL 2013', 
            marriage_date='24 JUL 2020',
        ))

if __name__ == '__main__':
    unittest.main()