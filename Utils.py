from datetime import datetime

class Utils:
    def divorce_before_death(self, divorce_time, death_time):
        _format = '%d %b %Y'
        death_time = datetime.strptime(death_time, _format)
        divorce_time = datetime.strptime(divorce_time, _format)
        if death_time.timestamp() - divorce_time.timestamp() < 0:
            raise ValueError('Death Date before Divorce Date')
        return True
