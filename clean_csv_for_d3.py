import csv
import os
import re
from pprint import pprint
import clean_data

def create_clean_csv(csv_file_path):

    old_file_name = csv_file_path.split('/')[-1][:-4]
    with open(csv_file_path, 'r') as csv_file:

        csv_contents = csv.DictReader(csv_file)
        for index, row in enumerate(csv_contents):

            new_file_name = old_file_name + '_' + clean_data.monthly_or_quarterly(row) + '.csv'

            with open('d3_csv/' + new_file_name, 'w') as new_csv_file:
                columns = list(row.keys())
                for index, column in enumerate(columns):
                    if column == '':
                        columns[index] = 'date'

                csv_writer = csv.DictWriter(new_csv_file, fieldnames=columns)
                if index == 0:
                    print(new_file_name)
                    csv_writer.writeheader()

                if row.get('') is not None:
                    row['date'] = row['']
                    row.pop('')

                for key, value in row.items():
                    row[key] = ''
                    for char in value:
                        if char.isdigit() or char in ['.', ',']:
                            row[key] += char
                csv_writer.writerow(row)



        csv_file.close()


def main():
    for csv_file in os.listdir('csv_data'):
        if 'first_second_third' not in csv_file:
            create_clean_csv('csv_data/' + csv_file)


if __name__ == '__main__':
    main()
