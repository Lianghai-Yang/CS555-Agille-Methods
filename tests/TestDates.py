import sys
sys.path.append('..')
import unittest
from Utils import Utils, _format
from datetime import datetime, timedelta

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


    def test_less_than_150(self):
        utils = self.utils

        self.assertTrue(utils.less_than_150(
            birth_time='24 JUL 1994',
            death_time='24 JUL 2019'
        ))

        self.assertTrue(utils.less_than_150(
            birth_time='24 JUL 1994',
            death_time='N/A'
        ))

        self.assertRaises(ValueError, utils.less_than_150,
            birth_time='24 JUL 1719',
            death_time='N/A'
        )

        self.assertRaises(ValueError, utils.less_than_150,
            birth_time='24 JUL 1719',
            death_time='24 JUL 2019'
        )


    def test_birth_before_death_of_parents(self):
        utils = self.utils

        self.assertTrue(utils.birth_before_death_of_parents(
            father_death_date   = '04 JUL 2000',
            mother_death_date   = '12 AUG 2010',
            child_birth_date    = '24 MAR 1962'
        ))

        self.assertTrue(utils.birth_before_death_of_parents(
            father_death_date   = '04 JUL 2000',
            mother_death_date   = 'N/A',
            child_birth_date    = '24 MAR 1962'
        ))

        self.assertTrue(utils.birth_before_death_of_parents(
            father_death_date   = 'N/A',
            mother_death_date   = '12 AUG 2010',
            child_birth_date    = '24 MAR 1962'
        ))

        self.assertRaises(ValueError, utils.birth_before_death_of_parents,
            father_death_date   = '04 JUL 1900',
            mother_death_date   = '12 AUG 2010',
            child_birth_date    = '24 MAR 1962'
        )

        self.assertRaises(ValueError, utils.birth_before_death_of_parents,
            father_death_date   = '04 JUL 2000',
            mother_death_date   = '12 AUG 1940',
            child_birth_date    = '24 MAR 1962'
        )


    def test_birth_before_marriage(self):
        utils = self.utils

        self.assertTrue(utils.birth_before_marriage(
            birth_date      = '01 JAN 1984',
            marriage_date   = '01 JAN 2018',
        ))

        self.assertTrue(utils.birth_before_marriage(
            birth_date      = '01 JAN 1984',
            marriage_date   = 'N/A',
        ))

        self.assertRaises(ValueError, utils.birth_before_marriage,
            birth_date      = '01 JAN 1999',
            marriage_date   = '01 JAN 1982'
        )


    def test_marriage_before_divorce(self):
        utils = self.utils

        self.assertTrue(utils.marriage_before_divorce(
            marriage_date      = '01 JAN 1984',
            divorce_date   = '01 JAN 2018',
        ))

        self.assertTrue(utils.marriage_before_divorce(
            marriage_date      = '01 JAN 1984',
            divorce_date   = 'N/A',
        ))

        self.assertTrue(utils.marriage_before_divorce(
            marriage_date      = 'N/A',
            divorce_date   = 'N/A',
        ))

        self.assertRaises(ValueError, utils.marriage_before_divorce,
            marriage_date      = '01 JAN 1999',
            divorce_date   = '01 JAN 1982'
        )


    def test_marriage_before_death(self):
        utils = self.utils

        self.assertTrue(utils.marriage_before_death(
            marriage_date      = '01 JAN 1984',
            death_date   = '01 JAN 2018',
        ))

        self.assertTrue(utils.marriage_before_death(
            marriage_date      = '01 JAN 1984',
            death_date   = 'N/A',
        ))

        self.assertTrue(utils.marriage_before_death(
            marriage_date      = 'N/A',
            death_date   = 'N/A',
        ))

        self.assertRaises(ValueError, utils.marriage_before_death,
            marriage_date      = '01 JAN 1999',
            death_date   = '01 JAN 1982'
        )


    def test_dates_before_current_date(self):
        utils = self.utils

        passed_date = '17 JUL 1980'
        self.assertTrue(utils.dates_bofore_current_date(passed_date))

        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime(_format)
        self.assertRaises(ValueError, utils.dates_bofore_current_date, date=tomorrow_date)

if __name__ == '__main__':
    unittest.main()