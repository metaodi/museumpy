# flake8: noqa
import museumpy
import requests
from dotenv import load_dotenv, find_dotenv
import os
from pprint import pprint
import tempfile

load_dotenv(find_dotenv())
user = os.getenv('MP_USER')
pw = os.getenv('MP_PASS')
s = requests.Session()
s.auth = (user, pw)

client = museumpy.MuseumPlusClient(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    session=s
)

group_result = client.search(
    field='OgrNameTxt',
    value='Patolu, MAP',
    module='ObjectGroup'
)
group = group_result[0]['raw']
ref = group['moduleItem']['moduleReference']


for ref_item in ref['moduleReferenceItem'][:5]:
    item = client.module_item(ref_item['moduleItemId'], ref['targetModule'])
    pprint(item, depth=1)
    if item['hasAttachments'] == 'true':
        with tempfile.TemporaryDirectory() as tmpdir:
            attachment_path = client.download_attachment(ref_item['moduleItemId'], ref['targetModule'], tmpdir)
            print(f"Attachment downloaded and saved at {attachment_path}")
