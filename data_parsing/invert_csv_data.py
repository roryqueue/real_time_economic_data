import csv
import os
import re
from pprint import pprint
import clean_data


def invert_csv(csv_file_path):

    old_file_name = csv_file_path.split('/')[-1][:-4]
    with open(csv_file_path, 'r') as old_file:
        file_in_memory = [line.split(',') for line in old_file]
        print(file_in_memory)
        new_file = open('inverted_csv_data/' + old_file_name, 'w')

        # csv_writer = csv.writer(new_file, quoting=csv.QUOTE_ALL)
        for line in zip(*file_in_memory):
            row = ','.join(value for value in line).replace('\n', '') + '\n'
            new_file.write(row)
        new_file.close()


def main():
    for csv_file in os.listdir('csv_data'):
        if 'first_second_third' not in csv_file:
            invert_csv('csv_data/' + csv_file)


if __name__ == '__main__':
    main()
