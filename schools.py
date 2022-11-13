import csv
from time import sleep
from typing import Tuple

import requests
from bs4 import BeautifulSoup, Tag


def get_soup(url: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(url, timeout=65535).content, 'html5lib')


base_url: str = 'https://www.tuttitalia.it'
schools_url: str = f'{base_url}/scuole'
schools_soup: BeautifulSoup = get_soup(schools_url)

with open('schools.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(('REGION', 'PROVINCE', 'CITY', 'GRADE', 'NAME OF THE SCHOOL', 'ADDRESS', 'TYPE', 'CODE'))

    for a_region in schools_soup.find('table', {'class': 'ct'}).find_all('a'):
        region_url: str = f'{base_url}{a_region["href"]}'
        region_name: str = a_region.text.strip()
        region_soup: BeautifulSoup = get_soup(region_url)

        for a_province in region_soup.find('table', {'class': 'ct'}).find_all('a'):
            province_url: str = f'{base_url}{a_province["href"]}'
            province_name: str = a_province.text.strip()
            province_soup: BeautifulSoup = get_soup(province_url)

            for a_municipality in province_soup.find('table', {'class': 'ct'}).find_all('a'):
                municipality_url: str = f'{base_url}{a_municipality["href"]}'
                municipality_name: str = a_municipality.text.strip()
                municipality_soup: BeautifulSoup = get_soup(municipality_url)

                for div_school_type in municipality_soup.find_all('div', {'class': 'mh'}):
                    h2_school_grade: Tag = div_school_type.find('h2')
                    school_grade: str = list(h2_school_grade.children)[0].text.strip()

                    for div_school in div_school_type.parent.find_all('div', {'class': 'if'}):
                        school_code: str = div_school['id'].strip()

                        h3_school_name: Tag = div_school.find('h3')
                        school_name: str = h3_school_name.text.strip()

                        div_kk: Tag = div_school.find('div', {'class': 'kk'})
                        list([h3.decompose() for h3 in div_kk.find_all('h3')])
                        list([br.decompose() for br in div_kk.find_all('br')])
                        list([dl.decompose() for dl in div_kk.find_all('dl')])
                        div_kk.find('b').insert_before('\n')
                        school_address: str = div_kk.text.strip().replace(' \n', '\n')

                        div_hz: Tag = div_school.find('div', {'class': 'hz'})
                        i_school_type: Tag = div_hz.find('i')
                        school_type: str = i_school_type.text.strip()

                        data_tuple: Tuple[str, str, str, str, str, str, str, str] = (
                            region_name,
                            province_name,
                            municipality_name,
                            school_grade,
                            school_name,
                            school_address,
                            school_type,
                            school_code
                        )
                        print(data_tuple)
                        csv_writer.writerow(data_tuple)
                sleep(5)
