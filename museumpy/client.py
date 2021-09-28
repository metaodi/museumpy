# -*- coding: utf-8 -*-

import re
import os
import requests
from . import errors
from . import xmlparse
from . import response

FULLTEXT_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<application xmlns="http://www.zetcom.com/ria/ws/module/search" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.zetcom.com/ria/ws/module/search http://docs.zetcom.com/ws/module/search/search_1_4.xsd">
  <modules>
    <module name="{module_name}">
      <search limit="{limit}" offset="{offset}">
        <fulltext>{query}</fulltext>
      </search>
    </module>
  </modules>
</application>"""  # noqa


SEARCH_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<application xmlns="http://www.zetcom.com/ria/ws/module/search" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.zetcom.com/ria/ws/module/search http://docs.zetcom.com/ws/module/search/search_1_4.xsd">
  <modules>
    <module name="{module_name}">
      <search limit="{limit}" offset="{offset}">
        <expert>
          <and>
            <equalsField fieldPath="{field}" operand="{value}" />
          </and>
        </expert>
      </search>
    </module>
  </modules>
</application>"""  # noqa


class MuseumPlusClient(object):
    def __init__(self, base_url=None, map_function=None, requests_kwargs=None):
        self.session = requests.Session()
        self.base_url = base_url
        self.xmlparser = xmlparse.XMLParser()
        self.map_function = map_function
        self.requests_kwargs = requests_kwargs or {}

    def fulltext_search(self, query, module='Object', limit=100, offset=0):
        url = f"{self.base_url}/ria-ws/application/module/{module}/search"
        params = {
            'module_name': module,
            'query': query,
        }
        data_loader = DataPoster(url, params, FULLTEXT_TEMPLATE, self.requests_kwargs)
        return response.SearchResponse(data_loader, limit, offset, self.map_function)

    def search(self, field, value, module='Object', limit=100, offset=0):
        url = f"{self.base_url}/ria-ws/application/module/{module}/search"
        params = {
            'module_name': module,
            'field': field,
            'value': value,
            }
        data_loader = DataPoster(url, params, SEARCH_TEMPLATE, self.requests_kwargs)
        return response.SearchResponse(data_loader, limit, offset, self.map_function)

    def module_item(self, id, module='Object'):
        url = f"{self.base_url}/ria-ws/application/module/{module}/{id}"
        data_loader = DataLoader(url, self.requests_kwargs)
        resp = response.SearchResponse(data_loader, map_function=self.map_function)
        if resp.count == 1:
            return resp[0]
        return resp

    def download_attachment(self, id, module='Object', dir='.'):
        url = f"{self.base_url}/ria-ws/application/module/{module}/{id}/attachment"
        data_loader = DataLoader(url, self.requests_kwargs)
        return data_loader.download_file(url, dir)


class DataPoster(object):
    def __init__(self, url, params=None, template=None, requests_kwargs=None):
        self.session = requests.Session()
        self.url = url
        self.params = params
        self.template = template
        self.xmlparser = xmlparse.XMLParser()
        self.requests_kwargs = requests_kwargs or {}

    def load(self, **kwargs):
        self.params.update(kwargs)
        xml = self.template.format(**self.params).encode('utf-8')
        return self._post_xml(self.url, xml)

    def _post_xml(self, url, xml):
        headers = {'Content-Type': 'application/xml'}
        res = self._post_content(url, xml, headers)
        return self.xmlparser.parse(res.content)

    def _post_content(self, url, data, headers):
        try:
            res = self.session.post(
                url,
                data=data,
                headers=headers,
                **self.requests_kwargs
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise errors.MuseumPlusError("HTTP error: %s" % e)
        except requests.exceptions.RequestException as e:
            raise errors.MuseumPlusError("Request error: %s" % e)

        return res


class DataLoader(object):
    def __init__(self, url, requests_kwargs=None):
        self.session = requests.Session()
        self.url = url
        self.xmlparser = xmlparse.XMLParser()
        self.requests_kwargs = requests_kwargs or {}

    def load(self, **kwargs):
        xml = self._get_xml(self.url)
        return xml

    def download_file(self, url, dir):
        headers = {'Accept': 'application/octet-stream'}
        res = self._get_content(url, headers)
        d = res.headers.get('Content-Disposition')
        fname = re.findall("filename=(.+)", d)[0]
        assert fname, "Could not find filename in Content-Disposition header"
        path = os.path.join(dir, fname)
        with open(path, 'wb') as f:
            for chunk in res.iter_content(1024):
                f.write(chunk)
        return path

    def _get_xml(self, url):
        res = self._get_content(url)
        return self.xmlparser.parse(res.content)

    def _get_content(self, url, headers={}):
        try:
            res = self.session.get(
                url,
                headers=headers,
                **self.requests_kwargs
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise errors.MuseumPlusError("HTTP error: %s" % e)
        except requests.exceptions.RequestException as e:
            raise errors.MuseumPlusError("Request error: %s" % e)

        return res
