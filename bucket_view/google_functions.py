from zipfile import ZipFile
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import io

def extract_zip(input_zip):
    input_zip = ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def get_assistant_file(unzip_dict):

    file_names = unzip_dict.keys()
    html_file = [html_file for html_file in file_names if "html" in html_file]

    for file in html_file:
        if len(file.split('/')) > 2: #and 'Asistente' in file:
            print(file)
            get_file = unzip_dict[(file)]
            get_string = get_file.decode("utf-8")
            soup = bs(get_string, 'html.parser')
            if soup.findAll('source', type='audio/mpeg'):
                print(file)
                assistant_file = soup
                print("Found Audio File")
    return assistant_file

def get_metadata(assistant_file, unzip_dict):

    file_names = unzip_dict.keys()
    audio_soup_list = assistant_file.findAll('div', attrs = {'class':'outer-cell'})

    audio_list = []
    for element in audio_soup_list:
        if element.find('source', type='audio/mpeg'):

            text = element.find('div', attrs={'class': 'content-cell'}).getText(separator=';').split(';')
            source = element.source['src']

            if len(text) > 2:
                t = pd.to_datetime(text[-1], infer_datetime_format=True)
                t_unix = int(t.timestamp() * 1e3)

                audio_data = {}
                audio_data['source'] = source
                audio_data['transcript'] = text[1]
                audio_data['time'] = text[-1]
                audio_data['timestamp'] = t_unix
                audio_data['file_name'] = str(t_unix) + '.mp3'

                for file_name in file_names:
                    if source in file_name:
                        audio_data['file'] = io.BytesIO(unzip_dict[(file_name)])

                audio_list.append(audio_data)
    return audio_list

def get_values_files(audio_list):
    values = []
    files = []
    for record in audio_list:
        v = [record['timestamp'], record['transcript']]
        f = ('speech-record-mp3', (record['file_name'], record['file'], 'audio/mpeg'))
        values.append(v)
        files.append(f)

    return values, files

