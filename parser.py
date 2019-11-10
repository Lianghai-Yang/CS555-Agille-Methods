import prettytable as pt
from Utils import Utils

KEYWORDS = {
    '0': ('INDI', 'FAM', 'HEAD', 'TRLR', 'NOTE',),
    '1': ('NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV',),
    '2': ('DATE')
}

utils = Utils()
individuals = {}
families = {}


def main():
    path = input('input file path: ')
    with open(path) as f:
        lines = []
        while True:
            line = str.strip(f.readline())
            if not line:
                break
            parsed_line = parseLine(line)
            isNewItem = True if line[0] == '0' else False
            if isNewItem:
                save(lines)
                lines = [ parsed_line, ]
            else:
                lines.append(parsed_line)
    getRelationship()
    # printIndi()
    # printFamilies()


def parseLine(line):
    parsed_line = line.split(' ', 2)
    # swap = False
    # valid = 'N'

    if len(parsed_line) == 3 and parsed_line[2] in ('INDI', "FAM"):
        tmp = parsed_line[2]
        parsed_line[2] = parsed_line[1]
        parsed_line[1] = tmp
        # swap = True

    # if parsed_line[0] in KEYWORDS.keys() and parsed_line[1] in KEYWORDS[parsed_line[0]]:
    #     valid = 'Y'

    # if parsed_line[1] in ('INDI', 'FAM') and swap is False:
    #     valid = 'N'

    return parsed_line


# Parsed line has structure like [[level, tag, arguments], [level, tag, arguments] ...]
def save(parsedLines):
    obj = {}
    obj_type = None
    date_type = None
    for line in parsedLines:
        if line[0] == '0' and (line[1] == 'INDI' or line[1] == 'FAM'):
            obj_type = line[1]
            obj['ID'] = line[2]
        elif line[0] == '1':
            if line[1] in KEYWORDS['1'] and len(line) == 3:
                # Array fields
                if line[1] in ['CHIL']:
                    if line[1] in obj:
                        obj[line[1]].append(line[2])
                    else:
                        obj[line[1]] = [ line[2], ]
                else:
                    obj[line[1]] = line[2]

            #  Date fields
            if line[1] in ['DEAT', 'BIRT', 'MARR', 'DIV']:
                obj[line[1]] = None
                date_type = line[1]

        elif line[0] == '2':
            if line[1] == 'DATE':
                obj[date_type] = line[2]
    # divorce_before_death(obj)
    if obj_type == 'INDI':
        if 'DEAT' not in obj:
            obj['DEAT'] = 'N/A'
        individuals[obj['ID']] = obj

    elif obj_type == 'FAM':
        MISSING_FIELDS = ['DIV', 'CHIL', 'MARR']
        for field in MISSING_FIELDS:
            if field not in obj:
                if field == 'CHIL':
                    obj[field] = []
                else:
                    obj[field] = 'N/A'
        families[obj['ID']] = obj


def getRelationship():
    for id in families:
        family = families[id]
        fields = ['CHIL', 'HUSB', 'WIFE']
        # if 'CHIL' not in family:
        #     family['CHIL'] = []
        for field in fields:
            if field in family:
                ids = []
                if field is 'CHIL':
                    ids = family['CHIL']
                else:
                    ids.append(family[field])
                if isinstance(ids, list) is False:
                    continue
                for iid in ids:
                    if field in individuals[iid]:
                        individuals[iid][field].append(id)
                    else:
                        individuals[iid][field] = [ id, ]


def printIndi():
    tab = pt.PrettyTable()
    tab.field_names = ['ID', 'NAME', 'GENDER', 'BIRTH DATE', 'DEATH DAET', 'SPOUSE', 'CHILD']
    indi_keys = list(individuals.keys())
    indi_keys.sort(reverse=False)
    for id in indi_keys:
        indi = individuals[id]
        spouse = 'N/A'
        child = 'N/A'
        if 'WIFE' in indi:
            spouse = indi['WIFE']
        elif 'HUSB' in indi:
            spouse = indi['HUSB']
        if 'CHIL' in indi:
            child = indi['CHIL']
        tab.add_row([id, indi['NAME'], indi['SEX'], indi['BIRT'], indi['DEAT'], spouse, child])
    print(tab)


def printFamilies():
    tab = pt.PrettyTable()
    tab.field_names = ['ID', 'HUSBAND ID', 'HUSBAND NAME', 'WIFE ID', 'WIFE NAME', 'CHILDREN', 'DIVORCE', 'MARRIAGE DATE']
    family_keys = list(families.keys())
    family_keys.sort(reverse=False)
    for id in family_keys:
        family = families[id]
        tab.add_row([
            id,
            family['HUSB'],
            individuals[family['HUSB']]['NAME'],
            family['WIFE'],
            individuals[family['WIFE']]['NAME'],
            family['CHIL'],
            family['DIV'],
            family['MARR']
        ])
    print(tab)


def listing():
    id_to_name = lambda ids: list(map(lambda x: individuals[x]['NAME'], ids))
    utils.print_res(msg='US36 - Recent Deaths:', res=id_to_name(utils.list_recent_deaths(individuals)))
    utils.print_res(msg='US30 - Living Married:', res=id_to_name(utils.list_living_married(individuals, families)))
    utils.print_res(msg='US31 - Living Single:', res=id_to_name(utils.list_living_single(individuals,families)))
    utils.print_res(msg='US35 - Recent Births:', res=id_to_name(utils.list_recent_birth(individuals)))
    utils.print_res(msg='US38 - Upcoming Births:', res=id_to_name(utils.list_upcoming_birthdays(individuals)))
    utils.print_res(msg='US29 - Deceased Individuals:', res=id_to_name(utils.list_deceased(individuals)))
    utils.print_res(msg='US34 - Large Age Differences:', res=id_to_name(utils.list_large_age_differences(individuals,families)))
    utils.print_res(msg='US39 - Upcoming anniversaries:', res=id_to_name(utils.list_upcoming_anniversaries(individuals, families))) 

def valueCheck():
    # Check Families
    print('\n--------Checking Families------------')
    for fid in families:
        fami = families[fid]
        husb = individuals[fami['HUSB']]
        wife = individuals[fami['WIFE']]
        kids = fami['CHIL']

        # dates_before_current_date
        fami_dates_fields = ['MARR', 'DIV']
        for field in fami_dates_fields:
            try:
                utils.dates_bofore_current_date(fami[field])
            except ValueError as e:
                printError(e, fid, msg=('Date Type: ' + field))
        
        # Correct gender for role
        try:
            utils.correct_gender_for_role(husband_gender= husb['SEX'], wife_gender = wife['SEX'])
        except ValueError as e:
            printError(e,fid,husb['ID'],wife['ID'])

        # divorce_before_death
        try:
            utils.divorce_before_death(divorce_time=fami['DIV'], death_time=husb['DEAT'])
        except ValueError as e:
            printError(e, fid, husb['ID'])

        # divorce_before_death
        try:
            utils.divorce_before_death(divorce_time=fami['DIV'], death_time=wife['DEAT'])
        except ValueError as e:
            printError(e, fid, wife['ID'])

        # birth_before_marriage
        try:
            utils.birth_before_marriage(
                birth_date=husb['BIRT'],
                marriage_date=fami['MARR'],
            )
        except ValueError as e:
            printError(e, fid=fid, iid=husb['ID'])

        # birth_before_marriage
        try:
            utils.birth_before_marriage(
                birth_date=wife['BIRT'],
                marriage_date=fami['MARR'],
            )
        except ValueError as e:
            printError(e, fid=fid, iid=wife['ID'])

        # marriage_before_death
        try:
            utils.marriage_before_death(marriage_date=fami['MARR'], death_date=husb['DEAT'])
        except ValueError as e:
            printError(e, fid, husb['ID'])

        # marriage_before_death
        try:
            utils.marriage_before_death(marriage_date=fami['MARR'], death_date=wife['DEAT'])
        except ValueError as e:
            printError(e, fid, wife['ID'])

        # marriage_before_divorce
        try:
            utils.marriage_before_divorce(marriage_date=fami['MARR'], divorce_date=fami['DIV'])
        except ValueError as e:
            printError(e, fid=fid)

        # marriage_after_14
        try:
            utils.marriage_after_14(husband_birth_date=husb['BIRT'], wife_birth_date=wife['BIRT'], marriage_date=fami['MARR'])
        except ValueError as e:
            printError(e, fid=fid, msg='Husband Birthdate {}, Wife Birthdate {}, Marriage date {}'.format(husb['BIRT'], wife['BIRT'], fami['MARR']))

        # Check Child's Values
        for kid in kids:
            chil = individuals[kid]

            # parents_not_too_old
            try:
                utils.parents_not_too_old(father_birth_date=husb['BIRT'], mother_birth_date=wife['BIRT'], child_birth_date=chil['BIRT'])
            except ValueError as e:
                printError(e, fid=fid, iid=kid)

            # birth_before_marriage_of_parents
            try:
                utils.birth_before_marriage_of_parents(
                    child_birth_date=chil['BIRT'],
                    marriage_date=fami['MARR'],
                    divorce_date=fami['DIV']
                )
            except ValueError as e:
                printError(e, fid=fid, iid=kid)

            # birth_before_death_of_parents
            try:
                utils.birth_before_death_of_parents(
                    father_death_date=husb['DEAT'],
                    mother_death_date=wife['DEAT'],
                    child_birth_date=chil['BIRT']
                )
            except ValueError as e:
                printError(e, fid=fid, iid=kid)

        # Check number of siblings
        try:
            utils.fewer_than_15_siblings(child_list=fami['CHIL'])
        except ValueError as e:
            printError(e, fid=fid)

    # Check Individuals
    print('\n--------Checking Individuals---------')
    for individual in individuals:
        indi = individuals[individual]

        indi_dates_fields = ['BIRT', 'DEAT']
        for field in indi_dates_fields:
            try:
                utils.dates_bofore_current_date(indi[field])
            except ValueError as e:
                printError(e, iid=individual, msg=('Date Type: ' + field))

        # less_than_150
        try:
            utils.less_than_150(birth_time=indi['BIRT'], death_time=indi['DEAT'])
        except ValueError as e:
            printError(e, fid=None, iid=individual)

        # birth_before_death
        try:
            utils.birth_before_death(birth_date=indi['BIRT'], death_date=indi['DEAT'])
        except ValueError as e:
            printError(e, iid=individual)
        
        # no_bigamy
        indi_role_fields = ['HUSB', 'WIFE']
        for role in indi_role_fields:
            if role in indi:
                marriage_divorce_list = list()
                for fami_id in indi[role]:
                    marriage_divorce_list.append({ 'MARR': families[fami_id]['MARR'], 'DIV': families[fami_id]['DIV'] })
                try:
                    utils.no_bigamy(marriage_divorce_list=marriage_divorce_list)
                except ValueError as e:
                    printError(e, iid=individual)            


def printError(e, fid=None, iid=None, msg=None):
    family_info, individual_info, message = '', '', ''
    if fid is not None:
        family_info = ' \t- Family: {fid}\n'.format(fid=fid)
    if iid is not None:
        individual_info = ' \t- Individual: {iid}\n'.format(iid=iid)
    if msg is not None:
        message = ' \t- {msg}\n'.format(msg = msg)
    print('Error \n{e}{FAMILY}{INDIVIDUAL}{MESSAGE}'.format(
        FAMILY=family_info,
        INDIVIDUAL=individual_info,
        e=str(e),
        MESSAGE=message
    ))


main()

if __name__ == "__main__":
    printIndi()
    printFamilies()
    listing()
    valueCheck()