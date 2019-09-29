import sys
sys.path.append('..')
import unittest
from Utils import Utils

class Lists(unittest.TestCase):
    
    def test_list_recent_deaths(self):
        utils = Utils()
        
        self.assertTrue(utils.list_recent_deaths
              (people= {'@I1@': {'ID': '@I1@', 'NAME': 'Tim /James/', 'SEX': 'M', 'BIRT': '12 APR 1970', 'FAMC': '@F2@', 'DEAT': '24 SEP 2019', 'HUSB': ['@F1@'], 'CHIL': ['@F2@']},
                        '@I2@': {'ID': '@I2@', 'NAME': 'Anna /Bella/', 'SEX': 'F', 'BIRT': '23 JUL 1971', 'FAMC': '@F4@', 'DEAT': 'N/A', 'WIFE': ['@F1@', '@F3@'], 'CHIL': ['@F4@']}})   
            
        )
        
        #self.assertRaises(ValueError, utils.list_recent_deaths
         #     (people= {'@I1@': {'ID': '@I1@', 'NAME': 'Tim /James/', 'SEX': 'M', 'BIRT': '12 APR 1970', 'FAMC': '@F2@', 'DEAT': '24 SEP 2018', 'HUSB': ['@F1@'], 'CHIL': ['@F2@']},
          #              '@I2@': {'ID': '@I2@', 'NAME': 'Anna /Bella/', 'SEX': 'F', 'BIRT': '23 JUL 1971', 'FAMC': '@F4@', 'DEAT': '20 SEP 2017', 'WIFE': ['@F1@', '@F3@'], 'CHIL': ['@F4@']}})   
            
        #)

if __name__ == '__main__':
    unittest.main()