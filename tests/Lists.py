import sys
sys.path.append('..')
import unittest
from Utils import Utils

class Lists(unittest.TestCase):
    
    def list_recent_deaths(self):
        utils = Utils()
        self.assertTrue(utils.list_recent_deaths(
            person= {'ID':'@I1', 'DEAT':'24 JUL 1984'}
        ))
        self.assertRaises(ValueError, utils.list_recent_deaths, 
            death_date='22 JUL 2013',
            
        )


if __name__ == '__main__':
    unittest.main()