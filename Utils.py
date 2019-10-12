from datetime import datetime, timedelta

_format = '%d %b %Y'

class Utils:
    def print_res(self, msg, res):
        print(msg)
        print(res)
        print('-------------------------------------')
    
    def divorce_before_death(self, divorce_time, death_time):
        if divorce_time == 'N/A' or death_time == 'N/A':
            return True

        death_time = datetime.strptime(death_time, _format)
        divorce_time = datetime.strptime(divorce_time, _format)

        if death_time.timestamp() - divorce_time.timestamp() < 0:
            raise ValueError('US06: Death Date is not before Divorce Date')

        return True

    def parents_not_too_old(self, father_birth_date, mother_birth_date, child_birth_date):
        fbd = datetime.strptime(father_birth_date, _format)
        mbd = datetime.strptime(mother_birth_date, _format)
        cbd = datetime.strptime(child_birth_date, _format)

        # check father's birth date and child's
        if (cbd - fbd).days > 80 * 365: 
            raise ValueError("US12: Father's birth date greater than 80 years older than his child.")

        # check mother's birth date and child's
        if (cbd - mbd).days > 60 * 365:
            raise ValueError("US12: Mother's birth date greater than 60 years older than her child.")

        return True

    def marriage_after_14(self, families, people):
        family_keys =  list(families.keys())
        for id in family_keys:
            family = families[id]
            husband_id = family['HUSB']
            wife_id = family['WIFE']
            wbd = datetime.strptime(people[wife_id]['BIRT'], _format)
            hbd = datetime.strptime(people[husband_id]['BIRT'], _format)
            if family['MARR'] == 'N/A':
                return True
            
            md = datetime.strptime(family['MARR'], _format)

            if (md - hbd).days < 14 * 365: 
                raise ValueError("Error: FAMILIES: {fid}: INDIVIDUALS: {iid}: US10: Husband should be greater than 14 when he got married.".format(fid=id, iid=husband_id))
            if (md - wbd).days < 14 * 365:
                raise ValueError("Error: FAMILIES: {fid}: INDIVIDUALS: {iid}: US10: Wife should be greater than 14 when she got married.".format(fid=id, iid=wife_id))

        return True

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

    def birth_before_marriage_of_parents(self, child_birth_date, marriage_date, divorce_date='N/A'):
        if marriage_date == 'N/A':
            raise ValueError('US08: Child birth date should be after marriage of parents')
        
        cbd = datetime.strptime(child_birth_date, _format)
        md  = datetime.strptime(marriage_date, _format)

        if cbd < md:
            raise ValueError('US08: Child birth date should be after marriage of parents')

        if divorce_date != 'N/A':
            dd  = datetime.strptime(divorce_date, _format)
            if cbd - dd > timedelta(days=30*9):
                raise ValueError('US08: Child birth should not be more than 9 months after parents\' divorce')

        return True

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
    
    def less_than_150(self, birth_time, death_time):
        if birth_time == 'N/A':
            raise ValueError('US07: Birth date should not be N/A')
        birth_time = datetime.strptime(birth_time, _format)
        if death_time == 'N/A':
            today_time = datetime.today()
            if (today_time - birth_time).days > 150 * 365:
                raise ValueError('US07: Active living time should be less than 150 years')
        else:
            death_time = datetime.strptime(death_time, _format)
            if(death_time - birth_time).days > 150 * 365:
                raise ValueError('US07: Living time should be less than 150 years')
        
        return True






        
