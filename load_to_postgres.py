import psycopg2
from psycopg2.extras import DictCursor
import configs
import csv
import os
import re
from pprint import pprint
from functools import reduce

# POSTGRES is a dict in the global scope of the gitignored configs.py file specifying db and auth
pg_connection = psycopg2.connect(**configs.POSTGRES)
pg_connection.autocommit = True
pg_cursor = pg_connection.cursor(cursor_factory=DictCursor)


def table_from_csv(file_name, column_names):
    standardized_column_names = []
    for column_name in column_names:
        if column_name in ['DATE', '']:
            continue

        new_column_name = column_name.replace(' ', '_')
        new_column_name = re.sub('[^0-9a-zA-Z_]+', '', new_column_name)

        first_digit_finder = re.search('\d', new_column_name)
        if new_column_name[0:2] in ['M1', 'M2']:
            new_column_name = new_column_name[2:]

        elif first_digit_finder is not None:
            new_column_name = new_column_name[first_digit_finder.start():]
        else:
            print("Couldn't format {}, continuing...".format(column_name))
            continue

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
                    continue

            else:
                print("Couldn't format {}, continuing...".format(column_name))
                continue

            new_column_name = prefix + year + suffix

        standardized_column_names.append(new_column_name)

    # print column_names
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
                table_name=file_name,
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
        print(file_name + ' Error: ' + str(e))


def load_to_postgres(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_contents = csv.DictReader(csv_file)
        for index, row in enumerate(csv_contents):
            row = dict(row)
            if index == 0:
                table_from_csv(
                    csv_file_path.split('/')[-1].replace('.csv', ''),
                    row.keys()
                )


def main():
    for csv_file in os.listdir('csv_data'):
        load_to_postgres('csv_data/' + csv_file)


if __name__ == '__main__':
    main()
