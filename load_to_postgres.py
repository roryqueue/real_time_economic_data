import psycopg2
from psycopg2.extras import DictCursor
import csv
import os
from functools import reduce
import configs
import clean_data

# POSTGRES is a dict in the global scope of the gitignored configs.py file specifying db and auth
pg_connection = psycopg2.connect(**configs.POSTGRES)
pg_connection.autocommit = True
pg_cursor = pg_connection.cursor(cursor_factory=DictCursor)
from collections import OrderedDict


def table_from_csv(table_name=None, column_names=None):
    standardized_column_names = []
    for column_name in column_names:
        if column_name.lower() not in ['', 'date']:
            standardized_column_names.append(clean_data.standardize_column_name(column_name, table_name))

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


def populate_row(table_name=None, row=None):
    cleaned_row = OrderedDict()

    for key, value in row.items():
        cleaned_row[clean_data.standardize_column_name(key, table_name)] = clean_data.standardize_value(value)

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
                    columns=clean_data.string_list(cleaned_row.keys()),
                    vals=clean_data.string_list(cleaned_row.values())
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
                table_name = file_name + '_' + clean_data.monthly_or_quarterly(row)

                table_from_csv(
                    table_name=table_name,
                    column_names=row.keys()
                )

            populate_row(
                table_name=table_name,
                row=row
            )
        print('Loaded file ', file_name)


def main():
    for csv_file in os.listdir('csv_data'):
        if 'first_second_third' not in csv_file:
            load_to_postgres('csv_data/' + csv_file)


if __name__ == '__main__':
    main()
