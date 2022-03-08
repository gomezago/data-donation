from zipfile import ZipFile
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import io
import json

def extract_zip(input_zip):
    input_zip = ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def get_assistant_file(unzip_dict):

    file_names = unzip_dict.keys()
    json_file = [json_file for json_file in file_names if "json" in json_file]
    json_data = json.loads(unzip_dict[json_file[0]])
    return json_data

def get_metadata(assistant_file, unzip_dict):

    file_names = unzip_dict.keys()

    audio_list = []
    for item in assistant_file:
        if 'audioFiles' in item:

            file_source = item['audioFiles'][0]
            time = item['time']
            t = pd.to_datetime(time, infer_datetime_format=True)
            t_unix = int(t.timestamp() * 1e3)

            audio_data = {}
            audio_data['transcript'] = item['title']
            audio_data['time'] = time
            audio_data['timestamp'] = t_unix
            audio_data['file_name'] = file_source

            for file in file_names:
                if file_source in file:
                    audio_data['file'] = io.BytesIO(unzip_dict[(file)])

            audio_list.append(audio_data)

    return audio_list

def get_values_files(audio_list):
    values = []
    files = []
    for record in audio_list:
        v = [record['timestamp'], record['transcript']]
        f = ('speech-record-mp3', (str(record['timestamp'])+".mp3", record['file'], 'audio/mpeg'))
        values.append(v)
        files.append(f)

    return values, files

