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
        self.assertEqual(r[0]['ObjDateTxt'], 'Meiji-Zeit, ca. 1890er-Jahre')  # noqa
        self.assertEqual(r[0]['ObjObjectTitleGrp'], 'Die Prinzessin Shokujo betrachet ds Spinnennetz in der Box vor ihr')  # noqa
        self.assertEqual(len(r[0]['refs']), 5)
        self.assertEqual(r[0]['refs']['Multimedia']['name'], 'ObjMultimediaRef')
        self.assertEqual(r[0]['refs']['Multimedia']['items'][0]['moduleItemId'], '45320')
        assert isinstance(r[0]['raw'], dict)
