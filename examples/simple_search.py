import museumpy
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import os

load_dotenv(find_dotenv())
user = os.getenv('MP_USER')
pw = os.getenv('MP_PASS')

records = museumpy.search(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    requests_kwargs={'auth': (user, pw)},
    field='ObjObjectNumberTxt',
    value='2019.184',
)

pprint(records)
print(len(records))
pprint(records[0], depth=1)
