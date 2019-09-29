from datetime import datetime,timedelta

_format = '%d %b %Y'

class Utils:
    def divorce_before_death(self, divorce_time, death_time):
        # to do valid the format of date
        death_time = datetime.strptime(death_time, _format)
        divorce_time = datetime.strptime(divorce_time, _format)
        if death_time.timestamp() - divorce_time.timestamp() < 0:
            raise ValueError('Death Date before Divorce Date')
        return True

    def parents_not_too_old(self, father_birth_date, mother_birth_date, child_birth_date):
        fbd = datetime.strptime(father_birth_date, _format)
        mbd = datetime.strptime(mother_birth_date, _format)
        cbd = datetime.strptime(child_birth_date, _format)

        # check father's birth date and child's
        if (cbd - fbd).days > 80 * 365: 
            raise ValueError("Father's birth date greater than 80 years older than his child.")

        # check mother's birth date and child's
        if (cbd - mbd).days > 60 * 365:
            raise ValueError("Mother's birth date greater than 60 years older than her child.")

        return True

    def marriage_after_14(self, husband_birth_date, wife_birth_date, marriage_date):
        hbd = datetime.strptime(husband_birth_date, _format)
        wbd = datetime.strptime(wife_birth_date, _format)
        md = datetime.strptime(marriage_date, _format)

        # check husband's birth date and wife's birth date
        if (md - hbd).days < 14 * 365: 
            raise ValueError("Husband should be 14 when he got married.")

        # check mother's birth date and child's
        if (md - wbd).days < 14 * 365:
            raise ValueError("Wife should be 14 when she got married.")

        return True

    def list_recent_deaths(self,people):
        
        recent_deaths = []
        indi_keys = list(people.keys())
       
        for id in indi_keys:
           indi = people[id]
           if indi['DEAT'] != 'N/A':
                
                today = datetime.today()
                deaths_time = datetime.strptime(indi['DEAT'],_format)
                delta = today - deaths_time    
                if delta <= timedelta(days=30):
                    recent_deaths.append(people[id])
       
        return recent_deaths
