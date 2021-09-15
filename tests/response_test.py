from museumpy_test import ResponseTestCase
from museumpy.response import SearchResponse


class TestSearchResponse(ResponseTestCase):
    def test_response_single(self):
        data_loader = self._data_loader_mock(['test_simple_search.xml'])
        res = SearchResponse(data_loader)

        self.assertEqual(res.count, 1)

    def test_response_iterator(self):
        filenames = [
            'response_multiple_1.xml',
            'response_multiple_2.xml',
            'response_multiple_3.xml',
        ]
        data_loader = self._data_loader_mock(filenames)
        res = SearchResponse(data_loader, limit=2, offset=0)

        next_res = next(iter(res))
        self.assertIsNotNone(next_res)
        self.assertIsInstance(next_res, dict)
        self.assertEqual(res.count, 5)

        records = [r for r in res]
        self.assertEqual(len(records), 5)
        self.assertEqual(data_loader.load.call_count, 3)
