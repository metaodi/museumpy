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
        self.assertEqual(r.__length_hint__(), 1)
        self.assertEqual(r.count, 1)

        self.assertEqual(r[0]['hasAttachments'], 'true')  # noqa
        self.assertEqual(r[0]['ObjCreditlineGrp'], 'Geschenk Gisela Müller und Erich Gross')  # noqa
        self.assertEqual(r[0]['ObjDateTxt'], 'Meiji-Zeit, ca. 1890er-Jahre')  # noqa
        self.assertEqual(r[0]['ObjDimAllGrp'], 'Objektmass: 21,6 x 18,7 cm')  # noqa
        self.assertEqual(r[0]['ObjGeograficGrp'], 'Japan')  # noqa
        self.assertEqual(r[0]['ObjMaterialTechniqueGrp'], 'Vielfarbendruck (nishiki-e)')  # noqa
        self.assertEqual(r[0]['ObjMultimediaRef'], 'Bild, 2019.184.jpg')  # noqa
        self.assertEqual(r[0]['ObjObjectNumberTxt'], '2019.184')  # noqa
        self.assertEqual(r[0]['ObjObjectTitleGrp'], 'Die Prinzessin Shokujo betrachet ds Spinnennetz in der Box vor ihr')  # noqa
        self.assertEqual(r[0]['ObjOwnershipRef'], 'Gisela Müller und Erich Gross, Zürich; Familie Missionar Hunziker (Flury); Schuler-Auktion, München, Nr. 6689')  # noqa
        self.assertEqual(r[0]['ObjPerAssociationRef'], 'Yashima Gakutei (1786-1868)')  # noqa
        assert isinstance(r[0]['raw'], dict)
