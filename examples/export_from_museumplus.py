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

client = museumpy.MuseumPlusClient(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    session=s
)

exports = client.exports(module='ObjectGroup')

# find a csv export
csv_export_id = None
for export in exports:
    if export['extension'] == 'csv':
        csv_export_id = export['id']
        break

print(f"CSV-Export ID: {csv_export_id}")

# export all
all_csv_path = client.module_export(csv_export_id, module='ObjectGroup')
print(f"Full CSV export: {all_csv_path}")

# export with filter
filtered_module_export_path = client.module_export(
    csv_export_id,
    field='OgrNameTxt',
    value='Himmelheber-Fotoarchiv (Furbo)',
    module='ObjectGroup'
)
print(f"Filtered CSV: {filtered_module_export_path}")

# export single item
result = client.search(
    field='OgrNameTxt',
    value='Himmelheber-Fotoarchiv (Furbo)',
    module='ObjectGroup'
)[0]

item_id = result['raw']['moduleItem']['id']
single_item_path = client.module_item_export(item_id, csv_export_id, module='ObjectGroup')
print(f"Single item export: {single_item_path}")