import psycopg2
from psycopg2.extras import DictCursor, Json
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


def populate_row(table_name=None, row=None):
    metric_values = []
    metric_date = None
    for key, value in row.items():
        cleaned_key = clean_data.standardize_column_name(key, table_name)
        cleaned_value = clean_data.standardize_value(value)
        if str(cleaned_key) == '"DATE"':
            metric_date = cleaned_value
        elif cleaned_key is not None and cleaned_value is not None and cleaned_value != "NULL":
            metric_values.append({
                'release_date': cleaned_key,
                'value': cleaned_value
            })

    metric_values = sorted(metric_values, key=lambda release: release['release_date'])
    final_value = None
    value_finalization_index = None
    for index, value_dict in enumerate(reversed(metric_values)):
        release_value = value_dict['value']
        if final_value is None:
            final_value = release_value

        if release_value != final_value:
            break
        
        value_finalization_index = index

    
    if value_finalization_index is not None:
        metric_values = metric_values[:-(value_finalization_index)]

    if len(metric_values) > 0:
        try:
            # probably a bad way to format, but it's a known data source 
            pg_cursor.execute(
                """ INSERT INTO {table_name}
                        (metric_date, metric_values, initial_release_date, final_release_date)
                    VALUES
                        ({metric_date}, {metric_values}, {initial_release_date}, {final_release_date});
                """.format(
                    table_name=table_name,
                    metric_date=metric_date,
                    metric_values=Json(metric_values),
                    initial_release_date="'" + metric_values[0]['release_date'][1:] + "'::DATE",
                    final_release_date="'" + metric_values[-1]['release_date'][1:] + "'::DATE"
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

                try:
                    # probably a bad way to format, but it's a known data source 
                    pg_cursor.execute(
                        """ DROP TABLE IF EXISTS {table_name};
                            CREATE TABLE {table_name} (
                                metric_date date not null,
                                metric_values jsonb default '[]'::JSON,
                                initial_release_date date not null,
                                final_release_date date not null
                            );
                        """.format(table_name=table_name)
                    )

                except Exception as e:
                    print(table_name + ' Error: ' + str(e))

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
