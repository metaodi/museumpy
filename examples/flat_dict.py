# flake8: noqa
# pip install flatten-dict
import museumpy
import requests
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
from flatten_dict import flatten
import os


def flat_dict(record, xml):
    d = record['raw']
    def leaf_reducer(k1, k2):
        if k1 is None or k2.lower() in k1.lower():
            return k2
        if k2 == "text":
            return k1
        return f"{k1}_{k2}"

    flat_data = flatten(d, max_flatten_depth=2, reducer=leaf_reducer)
    return flat_data


load_dotenv(find_dotenv())
user = os.getenv('MP_USER')
pw = os.getenv('MP_PASS')
s = requests.Session()
s.auth = (user, pw)

client = museumpy.MuseumPlusClient(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    map_function=flat_dict,
    session=s
)

records = client.search(field='ObjObjectNumberTxt', value='2019.184')
pprint(records[0])
