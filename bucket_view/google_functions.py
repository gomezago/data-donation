from zipfile import ZipFile
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import io
import json
import os
import itertools
from utils.bucket_functions import *
import time

def extract_zip(input_zip):
    input_zip = ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def validate_voice(file_names_dict):
    file_dirs = list(set([os.path.dirname(x) for x in file_names_dict]))
    ext = [os.path.splitext(x)[1] for x in file_names_dict]
    if len(file_dirs) == 2:
        if '.json' and '.html' and '.mp3' in ext:
            valid = True
            error_string = ''
        if '.json' not in ext:
            valid = False
            error_string = "Your .zip does not contain JSON files. Did you click on JSON under 'Activity Records' when downloading your data?"
        if '.mp3' not in ext:
            valid = False
            error_string = "Your .zip does not contain .mp3 files. Make sure the collection of 'Voice and Audio' is enabled in your device. If not, enable it and come back in a couple of weeks!"
    else:
        valid = False
        error_string = "Your .zip contains unexpected files. Did you select 'Assistant' when downloading your data?"

    return valid, error_string

def get_assistant_file(unzip_dict):

    file_names = unzip_dict.keys()
    json_file = [json_file for json_file in file_names if "json" in json_file]
    json_data = json.loads(unzip_dict[json_file[0]])
    return json_data

def get_metadata(assistant_file, unzip_dict, thingId, propertyId, token,n):

    file_names = unzip_dict.keys()

    for i in range(0, len(assistant_file), n):
        values = []
        files = []
        for item in assistant_file[i:i + n]:
            if 'audioFiles' in item:
                file_source = item['audioFiles'][0]
                file_path = [file for file in file_names if file_source in file]

                if file_path:
                    time = item['time']
                    t = pd.to_datetime(time, infer_datetime_format=True)
                    t_unix = int(t.timestamp() * 1e3)

                    v = [t_unix, item['title']]
                    f = ('speech-record-mp3', (str(t_unix) + ".mp3", io.BytesIO(unzip_dict[(file_path[0])]), 'audio/mpeg'))

                    values.append(v)
                    files.append(f)

        yield update_property_media(thingId, propertyId, values, files, token)


def send_chunks_bucket(values, files, thingId, propertyId, token, n):
    for i in range(0, len(values), n):
        yield update_property_media(thingId, propertyId, values[i:i + n], files[i:i + n],token)
