
KEYWORDS = {
            '0': ('INDI', 'FAM', 'HEAD', 'TRLR', 'NOTE',),
            '1': ('NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV',),
            '2': ('DATE')
        }

def main():
    path = input('input file path: ')
    with open(path) as f:
        while True:
            line = str.strip(f.readline())
            if not line:
                break
            parseLine(line)


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

    print('--> {}'.format(line))
    print('<-- {level}|{tag}|{valid}|{arguments}'.format(
        level=parsed_line[0],
        tag=parsed_line[1],
        valid=valid,
        arguments='' if len(parsed_line) < 3 else parsed_line[2]))

main()



