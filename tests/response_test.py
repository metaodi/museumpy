from museumpy_test import ResponseTestCase
from museumpy.response import SearchResponse


class TestSearchResponse(ResponseTestCase):
    def test_response_single(self):
        data_loader = self._data_loader_mock(['test_simple_search.xml'])
        res = SearchResponse(data_loader)

        self.assertEqual(len(res), 1)

