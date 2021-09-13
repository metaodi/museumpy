from museumpy_test import MuseumpyTestCase
from museumpy.client import MuseumPlusClient
import os

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


class TestClient(MuseumpyTestCase):
    def test_simple_search(self):
        client = MuseumPlusClient('http://test.com/MpWeb-test')
        r = client.search(field='TestField', value='TestValue')
        self.assertEqual(len(r), 1)

        self.assertEqual(r[0]['hasAttachments'], 'true')
        self.assertEqual(r[0]['ObjCreditlineGrp'], 'Geschenk Gisela Müller und Erich Gross')
        self.assertEqual(r[0]['ObjDateTxt'], 'Meiji-Zeit, ca. 1890er-Jahre')
        self.assertEqual(r[0]['ObjDimAllGrp'], 'Objektmass: 21,6 x 18,7 cm')
        self.assertEqual(r[0]['ObjGeograficGrp'], 'Japan')
        self.assertEqual(r[0]['ObjMaterialTechniqueGrp'], 'Vielfarbendruck (nishiki-e)')
        self.assertEqual(r[0]['ObjMultimediaRef'], 'Bild, 2019.184.jpg')
        self.assertEqual(r[0]['ObjObjectNumberTxt'], '2019.184')
        self.assertEqual(r[0]['ObjObjectTitleGrp'], 'Die Prinzessin Shokujo betrachet ds Spinnennetz in der Box vor ihr')
        self.assertEqual(r[0]['ObjOwnershipRef'], 'Gisela Müller und Erich Gross, Zürich; Familie Missionar Hunziker (Flury); Schuler-Auktion, München, Nr. 6689')
        self.assertEqual(r[0]['ObjPerAssociationRef'], 'Yashima Gakutei (1786-1868)')
        assert isinstance(r[0]['raw'], dict)

