import csv
import clean_data

def create_clean_csv(csv_file_path):
	try:
	    old_file_name = csv_file_path.split('/')[-1][:-4]

	    with open(csv_file_path, 'r') as csv_file:
	        csv_contents = csv.DictReader(csv_file)

	        new_file_name = old_file_name + '_'\
	        	+ clean_data.monthly_or_quarterly(row) + '.csv'

	        new_csv_file = open('d3_csv/' + new_file_name, 'wb')
	        csv_writer = csv.writer(new_csv_file)

	      	for index, row in enumerate(csv_contents):
	            csv_writer.writerow(first_sheet.row_values(row_index))

	        csv_file.close()

    except Exception as e:
        print('Could not convert {}: {}'.format(base_csv, str(e)))


def main():
    for csv_file in os.listdir('csv_data'):
        if 'first_second_third' not in csv_file:
            create_clean_csv('csv_data/' + csv_file)


if __name__ == '__main__':
    main()
