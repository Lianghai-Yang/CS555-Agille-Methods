from datetime import datetime

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