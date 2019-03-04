"""
This file contains all the core functions needed for the module such
as pickling/unpickling data, downloading data updates, etc.
"""
import glob
import gzip
import logging
from pathlib import Path
import pickle
import tempfile
import time
import zipfile

import requests

import allcities
from allcities.city import City
from allcities.cityset import CitySet

logger = logging.getLogger('allcities')

data_path = Path(allcities.__file__).parent / Path('data')
cities_data_path = data_path / Path('cities1000.pickle.gz')

def configure_logger():
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s] %(name)s-%(asctime).19s | %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def download_update(update_url='http://download.geonames.org/export/dump/cities1000.zip'):
    try:
        resp = requests.get(update_url)
    except requests.exceptions.RequestException as e:
        logger.exception('Failed to download update!\n{}'.format(e))
        return False

    try:
        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_dir = Path(temp_dir_name)
            zip_file = temp_dir / Path('file.zip')
            with zip_file.open('wb') as zf:
                zf.write(resp.content)
            logger.info('Download complete. Extracting and parsing data. This may take a while...')
            with zipfile.ZipFile(zip_file, 'r') as zf:
                zf.extractall(temp_dir_name)

            glob_path = glob.escape(str(temp_dir))
            txt_file = Path(glob.glob('{}/*.txt'.format(glob_path))[0])
            cities = parse_cities(txt_file)
            update_data_file(cities)
    except Exception as e:
        """
        intentionally catching every exception here. If anything goes wrong
        we want to fail the update
        """
        logger.exception('Failed to download update!')
        return False
    return True

def find_last_update():
    last_update_file = data_path / Path('last_update')
    with last_update_file.open('r') as f:
        last_update = float(f.read())
    result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_update))
    return result

def update_data_file(cities):
    old_cities_path = data_path / Path('cities1000.pickle.gz.old')
    new_cities_path = data_path / Path('cities1000.pickle.gz.new')
    pickle_data(new_cities_path, cities)
    if cities_data_path.exists():
        cities_data_path.rename(old_cities_path)
    new_cities_path.rename(cities_data_path)
    if old_cities_path.exists():
        old_cities_path.unlink()
    last_update_file = data_path / Path('last_update')
    with last_update_file.open('w') as f:
        f.write(str(time.time()))


def parse_cities(file_path):
    """
    Accepts a file_path pointing to cities1000.txt and parses it.
    """
    cities = []
    with file_path.open() as f:
        for line in f:
            split_line = line.rstrip('\n').split('\t')
            cities.append(City.geonames_factory(split_line))
    return cities

def pickle_data(file_path, pickle_object):
    with gzip.open(str(file_path), 'wb') as gzf:
        pickle.dump(pickle_object, gzf)

def unpickle_data(file_path):
    with gzip.open(str(file_path), 'rb') as gzf:
        pickle_object = pickle.load(gzf)
    return pickle_object

all_cities = CitySet(unpickle_data(cities_data_path))
last_update = find_last_update()

def init():
    if not cities_data_path.exists():
        logger.warning('Unable to locate data file. Downloading Update...')
        if download_update():
            logger.info('Update Successful')
        else:
            logger.error('Unable to download data.')

def main():
    configure_logger()
    try:
        init()
        us_cities = list(all_cities.filter(country_code='US').filter(name='Albuquerque'))
        import pprint
        pprint.pprint(us_cities[0].dict)
    except Exception as e:
        import traceback
        traceback.print_exc()
