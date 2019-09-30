import sys
sys.path.append('..')
import unittest
from Utils import Utils, _format
from datetime import datetime, timedelta

class TestLists(unittest.TestCase):
    utils = Utils()
    
    def test_list_recent_deaths(self):
        utils = self.utils
        before_days = (datetime.today() - timedelta(days=20)).strftime(_format)
        self.assertListEqual(utils.list_recent_deaths(
            people = {
                '@I1@': {'ID': '@I1@', 'NAME': 'Tim /James/', 'SEX': 'M', 'BIRT': before_days, 'FAMC': '@F2@', 'DEAT': '24 SEP 2019', 'HUSB': ['@F1@'], 'CHIL': ['@F2@']},
                '@I2@': {'ID': '@I2@', 'NAME': 'Anna /Bella/', 'SEX': 'F', 'BIRT': '23 JUL 1971', 'FAMC': '@F4@', 'DEAT': '31 MAR 2019', 'WIFE': ['@F1@', '@F3@'], 'CHIL': ['@F4@']},
                '@I3@': {'ID': '@I2@', 'NAME': 'Anna /Bella/', 'SEX': 'F', 'BIRT': '23 JUL 1971', 'FAMC': '@F4@', 'DEAT': 'N/A', 'WIFE': ['@F1@', '@F3@'], 'CHIL': ['@F4@']},
            }),
            sorted(['@I1@'])
        )

    def test_list_living_married(self):
        utils = self.utils
        self.assertListEqual(
            utils.list_living_married(
                people = {
                    "@I1@": {"ID": "@I1@","NAME": "Emme /Taylor/","SEX": "F","BIRT": "20 MAR 1949","DEAT": "N/A","WIFE": ["@F1@"]},
                    "@I2@": {"ID": "@I2@","NAME": "John /Smith/","SEX": "M","BIRT": "8 APR 1946","DEAT": "N/A","HUSB": ["@F1@"]},
                    "@I3@": {"ID": "@I3@","NAME": "Emily /Smith/","SEX": "F","BIRT": "5 DEC 1970","FAMC": "@F1@","DEAT": "N/A","CHIL": ["@F1@"],"WIFE": ["@F3@"]},
                    "@I8@": {"ID": "@I8@","NAME": "Trum /Johnson/","SEX": "M","BIRT": "7 NOV 1969","DEAT": "12 MAY 2000","HUSB": ["@F3@"]},
                    "@I9@": {"ID": "@I9@","NAME": "Jacob /Johnson/","SEX": "M","BIRT": "9 APR 1989","FAMC": "@F3@","DEAT": "N/A","CHIL": ["@F3@"]},
                },
                families = {
                    "@F1@": {"ID": "@F1@","HUSB": "@I2@","WIFE": "@I1@","CHIL": ["@I3@","@I5@"],"DIV": "N/A","MARR": "12 MAY 1968"},
                    "@F3@": {"ID": "@F3@","HUSB": "@I8@","WIFE": "@I3@","CHIL": ["@I9@"],"DIV": "N/A","MARR": "23 JAN 1989"},
                }
            ),
            sorted(['@I1@', '@I2@', '@I3@'])
        )
        

if __name__ == '__main__':
    unittest.main()