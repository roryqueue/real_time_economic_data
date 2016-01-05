import psycopg2
from psycopg2.extras import DictCursor
import configs
import csv
import os
import re
from functools import reduce


# POSTGRES is a dict in the global scope of the gitignored configs.py file specifying db and auth
pg_connection = psycopg2.connect(**configs.POSTGRES)
pg_connection.autocommit = True
pg_cursor = pg_connection.cursor(cursor_factory=DictCursor)
from collections import OrderedDict


def string_list(actual_list):
    return reduce(
        lambda string_list, value: string_list + str(value) + ", ",
        actual_list,
        ''
    )[0:-2]


def standardize_column_name(column_name):

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

        if suffix[0] == 'M':
            prefix = 'm_'
            if len(suffix) == 3:
                suffix = suffix[1:] + '01'
            elif len(suffix) == 2:
                suffix = '0' + suffix[1:] + '01'
            else:
                print("Couldn't format {}, continuing...".format(column_name))
                return None

        elif suffix[0] == 'Q':
            prefix = 'q_'
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

        new_column_name = prefix + year + suffix

    return new_column_name


def table_from_csv(table_name=None, column_names=None):
    standardized_column_names = []
    for column_name in column_names:
        if column_name.lower() not in ['', 'date']:
            standardized_column_names.append(standardize_column_name(column_name))

    if len(standardized_column_names) < 1:
        return

    try:
        # probably a bad way to format, but it's a known data source 
        pg_cursor.execute(
            """ DROP TABLE IF EXISTS {table_name};
                CREATE TABLE {table_name} (
                    "DATE" date not null,
                    {data_columns}
                );
            """.format(
                table_name=table_name,
                data_columns=reduce(
                    lambda column_list, column: column_list + column,
                    [
                        '{} float,\n'.format(column_name)
                        for column_name in standardized_column_names
                    ]
                )[0:-2]
            )
        )

    except Exception as e:
        print(table_name + ' Error: ' + str(e))


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


def populate_row(table_name=None, row=None):
    cleaned_row = OrderedDict()

    for key, value in row.items():
        cleaned_row[standardize_column_name(key)] = standardize_value(value)

    if cleaned_row.get(None):
        cleaned_row.pop(None)

    if len(cleaned_row) > 0:
        try:
            # probably a bad way to format, but it's a known data source 
            pg_cursor.execute(
                """ INSERT INTO {table_name} ({columns})
                    VALUES ({vals});
                """.format(
                    table_name=table_name,
                    columns=string_list(cleaned_row.keys()),
                    vals=string_list(cleaned_row.values())
                )
            )

        except Exception as e:
            print(table_name + ' Error: ' + str(e))


def load_to_postgres(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_contents = csv.DictReader(csv_file)
        file_name = csv_file_path.split('/')[-1].replace('.csv', '')

        for index, row in enumerate(csv_contents):
            if index == 0:
                table_from_csv(
                    table_name=file_name,
                    column_names=row.keys()
                )

            populate_row(
                table_name=file_name,
                row=row
            )



def main():
    for csv_file in os.listdir('csv_data'):
        load_to_postgres('csv_data/' + csv_file)


if __name__ == '__main__':
    main()
