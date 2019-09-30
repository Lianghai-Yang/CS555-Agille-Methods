import sys
sys.path.append('..')
import unittest
from Utils import Utils, _format
from datetime import datetime, timedelta

class TestLists(unittest.TestCase):
    
    def test_list_recent_deaths(self):
        utils = Utils()
        before_days = (datetime.today() - timedelta(days=20)).strftime(_format)
        self.assertListEqual(utils.list_recent_deaths(
            people = {
                '@I1@': {'ID': '@I1@', 'NAME': 'Tim /James/', 'SEX': 'M', 'BIRT': before_days, 'FAMC': '@F2@', 'DEAT': '24 SEP 2019', 'HUSB': ['@F1@'], 'CHIL': ['@F2@']},
                '@I2@': {'ID': '@I2@', 'NAME': 'Anna /Bella/', 'SEX': 'F', 'BIRT': '23 JUL 1971', 'FAMC': '@F4@', 'DEAT': '31 MAR 2019', 'WIFE': ['@F1@', '@F3@'], 'CHIL': ['@F4@']},
                '@I3@': {'ID': '@I2@', 'NAME': 'Anna /Bella/', 'SEX': 'F', 'BIRT': '23 JUL 1971', 'FAMC': '@F4@', 'DEAT': 'N/A', 'WIFE': ['@F1@', '@F3@'], 'CHIL': ['@F4@']},
            }),
            ['@I1@']
        )


if __name__ == '__main__':
    unittest.main()