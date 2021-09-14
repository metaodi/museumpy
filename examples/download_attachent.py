# flake8: noqa
import museumpy
from dotenv import load_dotenv, find_dotenv
import os
import tempfile

load_dotenv(find_dotenv())
user = os.getenv('MP_USER')
pw = os.getenv('MP_PASS')

client = museumpy.MuseumPlusClient(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    requests_kwargs={'auth': (user, pw)},
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
    if item['hasAttachments'] == 'true':
        with tempfile.TemporaryDirectory() as tmpdir:
            attachment_path = client.download_attachment(ref_item['moduleItemId'], ref['targetModule'], tmpdir)
            print(f"Attachment downloaded and saved at {attachment_path}")
