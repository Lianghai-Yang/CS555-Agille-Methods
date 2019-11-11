from datetime import datetime, timedelta
import math

_format = '%d %b %Y'

class Utils:

    def dates_within(self, date1, date2, limit, units):
        '''
        @Refer : CS-555 Lecture 6, slides page 27.
        @Return: boolean. True if date1 and date2 are within limit units. False if they are not.
        @Params: date1, date2. In format '%d %b %Y', eg. "7 JUL 1980"
        '''
        _date1, _date2 = datetime.strptime(date1, _format), datetime.strptime(date2, _format)
        units_types = {'days': 1, 'months': 30.4, 'years': 365.25}
        return (abs((_date1 - _date2).days) / units_types[units]) <= limit


    def compare_dates(self, date1, date2):
        '''
        @Return: number. 1 if date1 is greater than date2; -1 if date1 is less than date2; 0 if they are equal.
        @Params: date1, date2. In format '%d %b %Y', eg. "7 JUL 1980"
        '''
        _date1, _date2 = datetime.strptime(date1, _format), datetime.strptime(date2, _format)
        diff = (_date1 - _date2).days
        return 0 if diff == 0 else abs(diff)/diff


    def print_res(self, msg, res):
        print(msg)
        print(res)
        print('-------------------------------------')


    # US06
    def divorce_before_death(self, divorce_time, death_time):
        if divorce_time == 'N/A' or death_time == 'N/A':
            return True

        death_time = datetime.strptime(death_time, _format)
        divorce_time = datetime.strptime(divorce_time, _format)

        if death_time.timestamp() - divorce_time.timestamp() < 0:
            raise ValueError('US06: Death Date is not before Divorce Date \n\t- Detail: divorce_time="{divorce_time}",="{death_time}"\n'.format(
                divorce_time=divorce_time,
                death_time=death_time
            ))

        return True


    # US12
    def parents_not_too_old(self, father_birth_date, mother_birth_date, child_birth_date):
        fbd = datetime.strptime(father_birth_date, _format)
        mbd = datetime.strptime(mother_birth_date, _format)
        cbd = datetime.strptime(child_birth_date, _format)

        # check father's birth date and child's
        if (cbd - fbd).days > 80 * 365:
            raise ValueError("US12: Father's birth date greater than 80 years older than his child. \n\t- Detail: father_birth_date=\"{father_birth_date}\", child_birth_date=\"{child_birth_date}\"\n".format(
                father_birth_date=father_birth_date,
                child_birth_date=child_birth_date,
            ))

        # check mother's birth date and child's
        if (cbd - mbd).days > 60 * 365:
            raise ValueError("US12: Mother's birth date greater than 60 years older than her child. \n\t- Detail: mother_birth_date=\"{mother_birth_date}\", child_birth_date=\"{child_birth_date}\"\n".format(
                mother_birth_date=father_birth_date,
                child_birth_date=child_birth_date,
            ))

        return True


    # US10
    def marriage_after_14(self, husband_birth_date, wife_birth_date, marriage_date):
        hbd = datetime.strptime(husband_birth_date, _format)
        wbd = datetime.strptime(wife_birth_date, _format)
        md = datetime.strptime(marriage_date, _format)

        if (md - hbd).days < 14 * 365:
            raise ValueError("US10: Husband should be greater than 14 when he got married. - INFO Husband birth date='{husband_birth_date}', marriage_date = '{marriage_date}'\n".format(
                husband_birth_date=husband_birth_date,
                marriage_date = marriage_date,
                ))
        if (md - wbd).days < 14 * 365:
            raise ValueError("US10: Wife should be greater than 14 when she got married. - INFO Wife birth date='{wife_birth_date}', marriage_date = '{marriage_date}'\n".format(
                wife_birth_date=wife_birth_date,
                marriage_date = marriage_date,
                ))

        return True


    # US36
    def list_recent_deaths(self, people):
        recent_deaths = []
        indi_keys = list(people.keys())

        for id in indi_keys:
           indi = people[id]
           if indi['DEAT'] != 'N/A':
                today = datetime.today()
                deaths_time = datetime.strptime(indi['DEAT'],_format)
                delta = today - deaths_time
                if delta <= timedelta(days=30):
                    recent_deaths.append(id)

        return sorted(recent_deaths)


    # US08
    def birth_before_marriage_of_parents(self, child_birth_date, marriage_date, divorce_date='N/A'):
        if marriage_date == 'N/A':
            raise ValueError('US08: Child birth date should be after marriage of parents \n\t- Detail: child_birth_date="{child_birth_date}", marriage_date="{marriage_date}"\n'.format(
                child_birth_date=child_birth_date,
                marriage_date=marriage_date
            ))

        cbd = datetime.strptime(child_birth_date, _format)
        md  = datetime.strptime(marriage_date, _format)

        if cbd < md:
            raise ValueError('US08: Child birth date should be after marriage of parents \n\t- Detail: child_birth_date="{child_birth_date}", marriage_date="{marriage_date}"\n'.format(
                child_birth_date=child_birth_date,
                marriage_date=marriage_date
            ))

        if divorce_date != 'N/A':
            dd  = datetime.strptime(divorce_date, _format)
            if cbd - dd > timedelta(days=30*9):
                raise ValueError('US08: Child birth should not be more than 9 months after parents\' divorce \n\t- Detail: child_birth_date="{child_birth_date}", divorce_date="{divorce_date}"\n'.format(
                    child_birth_date=child_birth_date,
                    divorce_date=divorce_date
                ))
        return True


    # US30
    def list_living_married(self, people, families):
        res = []

        for id in list(families.keys()):
            family  = families[id]
            husband = people[family['HUSB']]
            wife    = people[family['WIFE']]
            if husband['DEAT'] == 'N/A':
                res.append(husband['ID'])
            if wife['DEAT'] == 'N/A':
                res.append(wife['ID'])

        return sorted(res)


    # US31
    def list_living_single(self, people, families):
        living_single = []
        marriaged = set()
        for family in families:
            fami = families[family]
            if 'HUSB' in fami:
                marriaged.add(fami['HUSB'])
            if 'WIFE' in fami:
                marriaged.add(fami['WIFE'])

        for individual in people:
            indi = people[individual]
            if indi['ID'] != 'N/A' and indi['DEAT'] == 'N/A':
                if indi['ID'] not in marriaged:
                    living_single.append(indi['ID'])

        return sorted(living_single)


    # US07
    def less_than_150(self, birth_time, death_time):
        if birth_time == 'N/A':
            raise ValueError('US07: Birth date should not be N/A')
        birth_time = datetime.strptime(birth_time, _format)
        if death_time == 'N/A':
            today_time = datetime.today()
            if (today_time - birth_time).days > 150 * 365:
                raise ValueError('US07: Active living time should be less than 150 years \n\t- Detail: birth_time="{birth_time}"\n'.format(
                    birth_time=birth_time
                ))
        else:
            death_time = datetime.strptime(death_time, _format)
            if(death_time - birth_time).days > 150 * 365:
                raise ValueError('US07: Living time should be less than 150 years \n\t- Detail: birth_time="{birth_time}", death_time="{death_time}"\n'.format(
                    birth_time=birth_time,
                    death_time=death_time
                ))
        return True


    # US35
    def list_recent_birth(self, people):
        recent_birth = []
        indi_keys = list(people.keys())

        for id in indi_keys:
           indi = people[id]
           if indi['DEAT'] == 'N/A':
                today = datetime.today()
                birth_time = datetime.strptime(indi['BIRT'],_format)
                delta = today - birth_time
                if delta <= timedelta(days=30):
                    recent_birth.append(id)

        return sorted(recent_birth)


    # US38
    def list_upcoming_birthdays(self, people):
        upcoming_birthdays = []
        indi_keys = list(people.keys())

        for id in indi_keys:
           indi = people[id]
           if indi['DEAT'] == 'N/A':
                today = datetime.today()
                birthday_time = datetime.strptime(indi['BIRT'],_format)
                birthday_date = datetime(today.year,birthday_time.month, birthday_time.day)
                delta = birthday_date - today
                if birthday_date > today and delta < timedelta(days = 30):
                    upcoming_birthdays.append(id)

        return sorted(upcoming_birthdays)


    # US09
    def birth_before_death_of_parents(self, father_death_date, mother_death_date, child_birth_date):
        '''
        US09
        @Return: True if the birth date is before the death dates of parents
        '''
        if (
            father_death_date is not None
            and
            father_death_date != 'N/A'
            and
            self.compare_dates(father_death_date, child_birth_date) < 0
        ):
            raise ValueError('US09: Father\'s death date should be after birth date of child \n\t- Detail: child_birth_date="{child_birth_date}", father_death_date="{father_death_date}"\n'.format(
                child_birth_date=child_birth_date,
                father_death_date=father_death_date,
            ))

        if (
            mother_death_date is not None
            and
            mother_death_date != 'N/A'
            and
            self.compare_dates(mother_death_date, child_birth_date) < 0
        ):
            raise ValueError('US09: Mother\'s death date should be after birth date of child \n\t- Detail: mother_death_date="{mother_death_date}", child_birth_date="{child_birth_date}"\n'.format(
                mother_death_date=mother_death_date,
                child_birth_date=child_birth_date,
            ))

        return True


    # US02
    def birth_before_marriage(self, birth_date, marriage_date):
        '''
        US02
        @Return: True if the birth date is before the marriage date
        '''
        if marriage_date is not None and marriage_date != 'N/A' and self.compare_dates(birth_date, marriage_date) > 0:
            raise ValueError('US02: Birth date should be before marriage date \n\t- Detail: birth_date="{birth_date}", marriage_date="{marriage_date}"\n'.format(
                birth_date=birth_date,
                marriage_date=marriage_date,
            ))

        return True


    # US04
    def marriage_before_divorce(self, marriage_date, divorce_date):
        if marriage_date is not None and marriage_date != 'N/A' and divorce_date is not None and divorce_date != 'N/A' and self.compare_dates(marriage_date, divorce_date) > 0:
            raise ValueError('US04: Divorce date should be before marriage date \n\t- Detail: marriage_date="{marriage_date}", divorce_date="{divorce_date}"\n'.format(
                marriage_date=marriage_date,
                divorce_date=divorce_date,
            ))

        return True


    # US05
    def marriage_before_death(self, marriage_date, death_date):
        if marriage_date is not None and marriage_date != 'N/A' and death_date is not None and death_date != 'N/A' and self.compare_dates(marriage_date, death_date) > 0 :
            raise ValueError('US05: Marriage date should be before death date \n\t- Detail: marriage_date="{marriage_date}", death_date="{death_date}"\n'.format(
                marriage_date=marriage_date,
                death_date=death_date,
            ))

        return True


    # US29
    def list_deceased(self, people):
        deceased = []
        indi_keys = list(people.keys())

        for id in indi_keys:
           indi = people[id]
           if indi['DEAT'] != 'N/A':
                deceased.append(id)

        return sorted(deceased)


    # US34
    def list_large_age_differences(self, people, families):
        res = []

        for id in list(families.keys()):
            family  = families[id]
            husband = people[family['HUSB']]
            wife    = people[family['WIFE']]


            husband_birth = datetime.strptime(husband['BIRT'],_format)
            wife_birth = datetime.strptime(wife['BIRT'],_format)
            today_time = datetime.today()

            husband_age = today_time - wife_birth
            wife_age = today_time - husband_birth
            if ((husband_age - wife_age).days > (wife_age).days) or ((wife_age - husband_age).days > (husband_age).days):
                res.append(husband['ID'])
                res.append(wife['ID'])

        return sorted(res)


    # US01
    def dates_bofore_current_date(self, date):
        if date == 'N/A':
            return True

        current_date = datetime.now().strftime(_format)
        if self.compare_dates(current_date, date) > 0:
            return True
        raise ValueError('US01: Date should be before current date\n\t- Detail: date: {date}, current date: {current_date}\n'.format(date=date, current_date=current_date))


    # US03
    def birth_before_death(self, birth_date, death_date):
        if birth_date is None or birth_date == 'N/A':
            raise ValueError('US03: Birth date should not be N/A or None\n')

        if death_date == 'N/A':
            return True

        if self.compare_dates(death_date, birth_date) > 0:
            return True

        raise ValueError(
            'US03: Birth date should be before death date\n\t- Detail: birth date: {birth_date}, death_date: {death_date}\n'.format(
                birth_date=birth_date,
                death_date=death_date
            )
        )


    # US11
    def no_bigamy(self, marriage_divorce_list):
        serialized = map(
            lambda item: {
                "MARR": datetime.strptime(item['MARR'], _format).timestamp() if item['MARR'] != 'N/A' and item['MARR'] is not None else math.inf,
                "DIV": datetime.strptime(item['DIV'], _format).timestamp() if item['DIV'] != "N/A" and item['DIV'] is not None else math.inf
            },
            marriage_divorce_list
        )

        sorted_list = sorted(serialized, key=lambda x: x['MARR'])

        for i in range(len(sorted_list)):
            if i == len(sorted_list) - 1:
                break
            if sorted_list[i]['DIV'] > sorted_list[i + 1]['MARR']:
                raise ValueError('US11: no bigamy allowed. marriage date {marr_date} is before divorce date {div_date}'.format(
                    marr_date=datetime.fromtimestamp(sorted_list[i + 1]['MARR']).strftime(_format) if sorted_list[i]['MARR'] != math.inf else 'N/A',
                    div_date=datetime.fromtimestamp(sorted_list[i]['DIV']).strftime(_format) if sorted_list[i]['DIV'] != math.inf else 'N/A'
                ))

        return True
    

    # US15
    def fewer_than_15_siblings(self, child_list):
        if len(child_list) >= 15:
            raise ValueError('US15: Number of siblings should be less than 15. Now is {num}'.format(num=len(child_list)))
        return True

    
    # US13
    def siblings_spacing(self, date1, date2):
        diff = abs(datetime.strptime(date1, _format) - datetime.strptime(date2, _format))
        if diff <= timedelta(weeks=8*4) and diff >= timedelta(days=2):
            raise ValueError('US13: birth dates of siblings should be more than 8 months apart and less than 2 days apart')
        return True                


    # US21
    def correct_gender_for_role(self, husband_gender, wife_gender):
        
        if husband_gender != 'M':
                raise ValueError ('US21: Husband in family should be male')
        if wife_gender != 'F':
                raise ValueError ('US21: Wife in family should be female')
        return True      


    # US39
    def list_upcoming_anniversaries(self, people, families):
        res = []
        today = datetime.today()
        for id in list(families.keys()):
            family  = families[id]
            husband = people[family['HUSB']]
            wife    = people[family['WIFE']]
            if husband['DEAT'] == 'N/A' and wife['DEAT'] == 'N/A':
        
                
                marriage_time = datetime.strptime(family['MARR'],_format)
                marriage_date = datetime(today.year,marriage_time.month, marriage_time.day)
                delta = marriage_date - today
                if marriage_date > today and delta < timedelta(days = 30):
                   res.append(husband['ID'])
                   res.append(wife['ID'])

        return sorted(res)  


    # US16
    def male_last_name(self, males_list):
        for i in range(len(males_list)):
            if i == len(males_list) - 1:
                break
            if males_list[i].split()[1] != males_list[i + 1].split()[1]:
                raise ValueError('US16: {name1} and {name2} have different last name'.format(name1=males_list[i], name2=males_list[i + 1]))
        return True