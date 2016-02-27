import csv
import os
import re
from pprint import pprint
import clean_data

def create_clean_csv(csv_file_path):
    # try:
    old_file_name = csv_file_path.split('/')[-1][:-4]

    with open(csv_file_path, 'r') as csv_file:
        csv_contents = csv.DictReader(csv_file)
        print(csv_contents)
        header_row = csv_contents.keys()
        print('hr', header_row)
        new_file_name = old_file_name + '_'\
        + clean_data.monthly_or_quarterly(header_row) + '.csv'

        with open('d3_csv/' + new_file_name, 'w') as new_csv_file:
            columns = header_row.keys()
            for index, column in enumerate(columns):
                if column == '':
                    columns[index] = 'date'

            # csv_keys = [clean_data.standardize_column_name(key, new_file_name) for key in row.keys()]
            # print(csv_keys)
            print(columns)
            csv_writer = csv.DictWriter(new_csv_file, fieldnames=columns)
            csv_writer.writeheader()


        for index, row in enumerate(csv_contents):
            # pprint(row.values())
            if index == 0:
                continue
            # print(index)
            # pprint(row)
            # row_string = str(row.values())
            # cleaned_row_string = ''
            for key, value in row.items():
                row[key] = ''
                for char in value:
                    if char.isdigit() or char in ['.', ',']:
                        row[key] += char
            print(row)

            # print(cleaned_row_string)
            # print(re.findall('[^\d.]+', str(row.values())))
            csv_writer.writerow(row)

        csv_file.close()

    # except Exception as e:
    #     print('Could not convert {}: {}'.format(old_file_name, str(e)))


def main():
    for csv_file in os.listdir('csv_data'):
        if 'first_second_third' not in csv_file:
            create_clean_csv('csv_data/' + csv_file)


if __name__ == '__main__':
    main()
