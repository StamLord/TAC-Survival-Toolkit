# Fix a string to fit the format: 6-0000000000
def parse_case_number(case_number):
    case_number = case_number.rstrip('\n')
    # If not enough numbers, fill with zeroes
    while len(case_number) < 10:
        case_number = '0' + case_number

    # If we are missing right side, add [6-]
    if len(case_number) == 10:
        case_number = '6-' + case_number

    # If lengh is correct we add [-] or [6]
    if len(case_number) == 11:
        if '-' in case_number:
            case_number = '6' + case_number
        else:
            case_number = case_number[0] + '-' + case_number[1:]
    return case_number