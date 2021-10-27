# flake8: noqa
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


# you can create your own custom mapping for the fields you need
# by parsing the given XML (e.g. using XPATH expressions)
def my_custom_map(record, xml_rec):
    NS = "http://www.zetcom.com/ria/ws/module"
    ID_XPATH = f".//{{{NS}}}dataField[@name='ObjObjectNumberTxt']/{{{NS}}}value"
    TITLE_XPATH = f".//{{{NS}}}repeatableGroup[@name='ObjObjectTitleGrp']//{{{NS}}}dataField[@name='TitleTxt']//{{{NS}}}value"

    xml_parser = museumpy.xmlparse.XMLParser()
    my_new_record = {
        'my_id': xml_parser.find(xml_rec, ID_XPATH).text,
        'my_title': xml_parser.find(xml_rec, TITLE_XPATH).text
    }
    return my_new_record


client = museumpy.MuseumPlusClient(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    map_function=my_custom_map,
    session=s
)

records = client.search(field='ObjObjectNumberTxt', value='2019.184')
pprint(records[0])
