import mock
import unittest
import os
from museumpy import xmlparse

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


class MuseumpyTestCase(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch('museumpy.client.requests.Session')
        self.session_mock = self.patcher.start()
        self._session_mock(self.session_mock)

    def tearDown(self):
        self.patcher.stop()

    def _session_mock(self, session_mock, filename=None):
        if not filename:
            filename = self._testMethodName + ".xml"
        path = os.path.join(
            __location__,
            'fixtures',
            filename
        )
        if not os.path.exists(path):
            return

        with open(path) as file:
            content=file.read()
            session_mock.return_value.get.return_value = mock.MagicMock(content=content)  # noqa
            session_mock.return_value.post.return_value = mock.MagicMock(content=content)  # noqa


class ResponseTestCase(MuseumpyTestCase):
    def _data_loader_mock(self, filenames):
        xmls = []
        for filename in filenames:
            xmls.append(self._load_xml(filename))
        m = mock.Mock()
        m.load.side_effect = xmls
        return m

    def _load_xml(self, filename):
        path = os.path.join(
            __location__,
            'fixtures',
            filename
        )
        xmlparser = xmlparse.XMLParser()
        with open(path) as file:
            content = file.read()
        return xmlparser.parse(content)
