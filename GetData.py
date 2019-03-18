import os
import io
import shutil
import urllib
import zipfile
import requests

from bs4 import BeautifulSoup


def Downloader(years):

    SysDataPage = "https://www.divvybikes.com/system-data"
    page = requests.get(url=SysDataPage)
    soup = BeautifulSoup(page.content, 'html.parser')
    class_sub = "type-beta--s--xs text-color--gray spacing"
    contents = soup.find_all('span', class_=class_sub)

    tag_a = BeautifulSoup(str(contents[0]), 'lxml').find_all('a')
    tag_a_href = [href.get('href') for href in tag_a]
    tag_a_href = sorted(set(tag_a_href), key=tag_a_href.index)

    tag_a_name = list(filter(None, [name.string for name in tag_a]))
    tag_a_name.insert(6, "2016 Q3 & Q4 Data")

    csv_URL = [url for url in tag_a_href for yr in years if yr in url]

    for file_url in csv_URL:
        target = requests.get(file_url)
        zipfile.ZipFile(io.BytesIO(target.content)).extractall()


def main():

    desired_yr = ['2017', '2018']
    Downloader(desired_yr)  # Download the Datasets

    os.mkdir('Trip_CSV')
    os.mkdir('Station_CSV')
    AP = os.getcwd()

    for file in os.listdir(AP):
        if 'Trips' in file:
            shutil.move(file, AP + '/Trip_CSV')
        elif 'Stations' in file:
            shutil.move(file, AP + '/Station_CSV')
