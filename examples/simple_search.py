import museumpy
import requests
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import os

load_dotenv(find_dotenv())
user = os.getenv('MP_USER')
pw = os.getenv('MP_PASS')
s = requests.Session()
s.auth = (user, pw)

records = museumpy.search(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    session=s,
    field='ObjObjectNumberTxt',
    value='2019.184',
)

pprint(records)
print(records.count)
pprint(records[0], depth=1)
