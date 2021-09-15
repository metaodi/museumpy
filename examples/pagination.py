import museumpy
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import os

load_dotenv(find_dotenv())
user = os.getenv('MP_USER')
pw = os.getenv('MP_PASS')


client = museumpy.MuseumPlusClient(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    requests_kwargs={'auth': (user, pw)}
)

result = client.fulltext_search(
    query='Patolu',
    limit=2
)

print(result)
print(result.count)
for rec in result[:5]:
    pprint(rec, depth=1)
print(result)
