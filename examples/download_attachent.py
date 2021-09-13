import museumpy
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import os

load_dotenv(find_dotenv())
user = os.getenv('MP_USER')
pw = os.getenv('MP_PASS')

client = museumpy.client(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    requests_kwargs={'auth': (user, pw)},
)

group_result = client.search('ObjObjectGroupTxt', 'MyGroup')
group = group_result[0]['raw']
ref = group['moduleIm']['moduleReference']

for ref_item in ref['moduleReferenceItem']:
    item = client.module_item(ref_item['moduleItemId'], ref['targetModule'])
    if item['hasAttachments'] == 'true':
        attachment_path = client.download_attachment(ref_item['moduleItemId'], ref['targetModule'], arguments['--attachments'])
        print(f"Attachment downloaded and saved at {attachment_path}")
