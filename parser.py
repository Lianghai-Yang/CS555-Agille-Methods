import prettytable as pt

KEYWORDS = {
    '0': ('INDI', 'FAM', 'HEAD', 'TRLR', 'NOTE',),
    '1': ('NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV',),
    '2': ('DATE')
}

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
    printIndi()
    printFamilies()


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

    # print('--> {}'.format(line))
    # print('<-- {level}|{tag}|{valid}|{arguments}'.format(
    #     level=parsed_line[0],
    #     tag=parsed_line[1],
    #     valid=valid,
    #     arguments='' if len(parsed_line) < 3 else parsed_line[2]))
    return parsed_line


# Parsed line has structure like [[level, tag, arguments], [level, tag, arguments] ...]
def save(parsedLines):
    obj = { 'DEAT': 'N/A' }
    obj_type = None
    date_type = None
    for line in parsedLines:
        if line[0] == '0' and (line[1] == 'INDI' or line[1] == 'FAM'):
            obj_type = line[1]
            obj['ID'] = line[2]
        elif line[0] == '1':
            if line[1] in KEYWORDS['1'] and len(line) == 3:
                obj[line[1]] = line[2]
            if line[1] in ['DEAT', 'BIRT', 'MARR', 'DIV']:
                obj[line[1]] = None
                date_type = line[1]
        elif line[0] == '2':
            if line[1] == 'DATE':
                obj[date_type] = line[2]

    if obj_type == 'INDI':
        individuals[obj['ID']] = obj
    elif obj_type == 'FAM':
        families[obj['ID']] = obj

def getRelationship():
    for id in families:
        family = families[id]
        fields = ['CHIL', 'HUSB', 'WIFE']
        for field in fields:
            if field in family:
                if field in individuals[family[field]]:
                    individuals[family[field]][field].append(id)
                else:
                    individuals[family[field]][field] = [ id, ]

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
    tab.field_names = ['ID', 'HUSBAND ID', 'HUSBAND NAME', 'WIFE ID', 'WIFE NAME', 'Chilren']
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
            family['CHIL']
        ])
    print(tab)
main()



