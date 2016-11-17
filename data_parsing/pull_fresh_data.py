import requests
from bs4 import BeautifulSoup, SoupStrainer
import subprocess
from pprint import pprint
import xlrd
import csv


def grab_philly_fed_page(subpage):
    # some sort of SSL issue when using requests so curling instead
    return subprocess.call([
        'curl',
        '-o',
        'raw_html/index.html' if not subpage else 'raw_html/{}.html'.format(subpage),
        'https://www.philadelphiafed.org/research-and-data/real-time-center/real-time-data/data-files/' + subpage
    ])


def find_sub_index_pages():
    rtds_index_file = open('raw_html/index.html', 'r')
    rtds_index_html = BeautifulSoup(rtds_index_file, 'html.parser')
    dataset_links = []
    for dataset_list in rtds_index_html.find('div', {'id': 'center-content-2column'}).find_all('ul'):
        for link_list_item in dataset_list.find_all('li'):
            try:
                dataset_links.append(link_list_item.a['href'].split('/')[-1])
            except:
                print('Could not find link in {}'.format(link_list_item))

    return set(dataset_links)


def find_excel_files(subindex):
    rtds_subindex_file = open('raw_html/{}.html'.format(subindex), 'r')
    filenames = []
    for link in BeautifulSoup(rtds_subindex_file, 'html.parser', parse_only=SoupStrainer('a')).find_all('a'):
        href = link.get('href', '')
        if 'xls' in href:
            filenames.append(href.split('/')[-1].split('?')[0])

    return filenames


def download_excel(filename):
    fed_file = requests.get(
        'http://www.philadelphiafed.org/-/media/research-and-data/real-time-center/real-time-data/data-files/files/{}?la=en'.format(filename),
        verify=False
    )
    with open('excel_data/' + filename.replace(' ', ''),'wb') as f:
    	f.write(fed_file.content)


def convert_to_csv(excel_file):
    print(excel_file)
    try:
        excel_workbook = xlrd.open_workbook('excel_data/' + excel_file)
        first_sheet = excel_workbook.sheet_by_index(0)
        csv_file = open('csv_data/' + excel_file.replace('.xls', '.csv'), 'wb')
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for row_index in xrange(first_sheet.nrows):
            csv_writer.writerow(first_sheet.row_values(row_index))
        csv_file.close()
    except Exception as e:
        print('Could not convert {}: {}'.format(excel_file, str(e)))

if __name__ == '__main__':
    grab_philly_fed_page('')
    excel_files = []
    for subpage in find_sub_index_pages():
        grab_philly_fed_page(subpage)
        excel_files.extend(find_excel_files(subpage))

    for file in set(excel_files):
        download_excel(file)
        convert_to_csv(file.replace(' ', ''))
