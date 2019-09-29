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

    def test_marriage_after_14(self,families,people):
        utils = Utils()
        self.assertTrue(utils.marriage_after_14(
            families = {'ID': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I1@', 'CHIL': ['@I3@', '@I5@'], 'DIV': 'N/A'},
            people = {'@I1@': {'ID': '@I1@', 'NAME': 'Tim /James/', 'SEX': 'M', 'BIRT': '12 APR 1970', 'FAMC': '@F2@', 'DEAT': '24 SEP 2018', 'HUSB': ['@F1@'], 'CHIL': ['@F2@']},
                      '@I2@': {'ID': '@I2@', 'NAME': 'Anna /Bella/', 'SEX': 'F', 'BIRT': '23 JUL 1971', 'FAMC': '@F4@', 'DEAT': '20 SEP 2017', 'WIFE': ['@F1@', '@F3@'], 'CHIL': ['@F4@']}})
        )
        self.assertRaises(ValueError, utils.marriage_after_14(
            families = {'ID': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I1@', 'CHIL': ['@I3@', '@I5@'], 'DIV': 'N/A'},
            people = {'@I1@': {'ID': '@I1@', 'NAME': 'Tim /James/', 'SEX': 'M', 'BIRT': '12 APR 1970', 'FAMC': '@F2@', 'DEAT': '24 SEP 2018', 'HUSB': ['@F1@'], 'CHIL': ['@F2@']},
                      '@I2@': {'ID': '@I2@', 'NAME': 'Anna /Bella/', 'SEX': 'F', 'BIRT': '23 JUL 1971', 'FAMC': '@F4@', 'DEAT': '20 SEP 2017', 'WIFE': ['@F1@', '@F3@'], 'CHIL': ['@F4@']}})
        )

if __name__ == '__main__':
    unittest.main()