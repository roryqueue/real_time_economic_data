import psycopg2
from psycopg2.extras import DictCursor
import configs
import csv
import os
import re
from pprint import pprint

# POSTGRES is a dict in the global scope of the gitignored configs.py file specifying db and auth
pg_connection = psycopg2.connect(**configs.POSTGRES)
pg_connection.autocommit = True
pg_cursor = pg_connection.cursor(cursor_factory=DictCursor)


def table_from_csv(file_name, column_names):
    try:
        # I know formatting this is a bad habit but psycopg2 won't allow me to pass
        # in a table name proper regular way
        pg_cursor.execute(
            """ CREATE TABLE {table_name} (
                    "DATE" date not null,
                    {data_columns}
                );
            """.format(
                table_name=file_name,
                data_columns=reduce(
                    lambda column_list, column: column_list + column,
                    [
                        '{} float,\n'.format(
                            re.sub(
                                '[^0-9a-zA-Z_]+',
                                '',
                                column_name.replace(' ', '_')
                            )
                        )
                        for column_name in column_names\
                        if column_name not in ['DATE', '']
                    ]
                )[0:-2]
            )
        )
    except Exception as e:
        print file_name, ' Error: ', e


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
