import re
from functools import reduce


def standardize_column_name(column_name, table_name):

    if column_name.lower() in ['date', '']:
        return '"DATE"'

    new_column_name = column_name.replace(' ', '_')
    new_column_name = re.sub('[^0-9a-zA-Z_]+', '', new_column_name)

    first_digit_finder = re.search('\d', new_column_name)
    if new_column_name[0:2] in ['M1', 'M2']:
        new_column_name = new_column_name[2:]

    elif first_digit_finder is not None:
        new_column_name = new_column_name[first_digit_finder.start():]
    else:
        print("Couldn't format {}, continuing...".format(column_name))
        return None

    if new_column_name[0] in ['0', '1']:
        new_column_name = '20' + new_column_name
    else:
        new_column_name = '19' + new_column_name
            
    first_non_digit_finder = re.search('\D', new_column_name)
    if first_non_digit_finder is not None:
        year = new_column_name[:first_non_digit_finder.start()]
        suffix =  new_column_name[first_non_digit_finder.start():]
        prefix = suffix[0].lower()

        if prefix == 'm':
            if len(suffix) == 3:
                suffix = suffix[1:] + '01'
            elif len(suffix) == 2:
                suffix = '0' + suffix[1:] + '01'
            else:
                print("Couldn't format {}, continuing...".format(column_name))
                return None

        elif prefix == 'q':
            if suffix[1:] == '1':
                suffix = '0101'
            elif suffix[1:] == '2':
                suffix = '0401'
            elif suffix[1:] == '3':
                suffix = '0701'
            elif suffix[1:] == '4':
                suffix = '1001'
            else:
                print("Couldn't format {}, continuing...".format(column_name))
                return None

        else:
            print("Couldn't format {}, continuing...".format(column_name))
            return None

        return prefix + year + suffix

    return column_name


def standardize_value(value):

    if value is None or value == '#N/A':
        return 'NULL'

    if ':' in value:
        year = value[:4]

        if 'q' in value.lower():
            if value[-1] == '1':
                date_n_month = '0101'
            elif value[-1] == '2':
                date_n_month = '0401'
            elif value[-1] == '3':
                date_n_month = '0701'
            elif value[-1] == '4':
                date_n_month = '1001'
            else:
                print('Could not parse value: {}'.format(value))
                return 'NULL'

        else:
            date_n_month = value[-2:] + '01'

        value = "'" + year + date_n_month + "'::DATE"

    elif re.search('[a-zA-Z]', value):
        value = "'" + value + "'"
    
    return value


def monthly_or_quarterly(row):
    for key, value in row.items():
        stripped_key = re.sub('[^a-z]+', '', key.lower())
        if len(stripped_key) > 0:
            if stripped_key[-1] == 'm':
                return 'monthly'
            if stripped_key[-1] == 'q':
                return 'quarterly'

    return 'unknown'


def string_list(actual_list):
    return reduce(
        lambda string_list, value: string_list + str(value) + ", ",
        actual_list,
        ''
    )[0:-2]

