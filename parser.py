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
    swap = False
    valid = 'N'

    if len(parsed_line) == 3 and parsed_line[2] in ('INDI', "FAM"):
        tmp = parsed_line[2]
        parsed_line[2] = parsed_line[1]
        parsed_line[1] = tmp
        swap = True

    if parsed_line[0] in KEYWORDS.keys() and parsed_line[1] in KEYWORDS[parsed_line[0]]:
        valid = 'Y'

    if parsed_line[1] in ('INDI', 'FAM') and swap is False:
        valid = 'N'

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
    utils.print_res(msg='Recent Deaths:', res=utils.list_recent_deaths(individuals))
    utils.print_res(msg='Living Married:', res=utils.list_living_married(individuals, families))
    
def valueCheck():
        for fid in families:
            fami = families[fid]
            husb = individuals[fami['HUSB']]
            wife = individuals[fami['WIFE']]
            kids = fami['CHIL']
            try:
                utils.divorce_before_death(divorce_time=fami['DIV'], death_time=husb['DEAT'])
            except ValueError as e:
                print('Error: FAMILIES: {fid}: INDIVIDUALS: {iid}'.format(fid=fid, iid=husb['ID']) + str(e))
                
            try:
                utils.divorce_before_death(divorce_time=fami['DIV'], death_time=wife['DEAT'])
            except ValueError as e:
                print('Error: FAMILIES: {fid}: INDIVIDUALS: {iid}'.format(fid=fid, iid=wife['ID']) + str(e))

main()

if __name__ == "__main__":
    printIndi()
    printFamilies()
    listing()
    valueCheck()