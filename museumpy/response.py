# -*- coding: utf-8 -*-

from . import xmlparse
from . import errors

ZETCOM_NS = "http://www.zetcom.com/ria/ws/module"


class SearchResponse(object):
    def __init__(self, data_loader, limit=100, offset=0, map_function=None):
        self.data_loader = data_loader
        self.xmlparser = xmlparse.XMLParser()
        self.records = []
        self.count = 0
        self.limit = limit
        self.offset = offset
        self.map_function = map_function

        xml = data_loader.load(limit=limit, offset=offset)
        self._parse_content(xml)

    def _parse_content(self, xml):
        self.count = self.maybe_int(self.xmlparser.find(xml, f'.//{{{ZETCOM_NS}}}module').attrib['totalSize'])  # noqa
        self._extract_records(xml)

    def maybe_int(self, s):
        try:
            return int(s)
        except (ValueError, TypeError):
            return s

    def _extract_records(self, xml):
        new_records = []
        xml_recs = self.xmlparser.findall(xml, f'.//{{{ZETCOM_NS}}}module/{{{ZETCOM_NS}}}moduleItem')  # noqa
        for xml_rec in xml_recs:
            record = self._map_xml(xml_rec)
            record['raw'] = self.xmlparser.todict(xml_rec, xml_attribs=True)
            if self.map_function:
                record = self.map_function(record, xml_rec)
            new_records.append(record)
        self.records.extend(new_records)

    def _map_xml(self, xml_rec):
        def xml_text(xpath):
            return self.xmlparser.find(xml_rec, xpath).text

        def xml_group(xpath, sep='; '):
            groups = self.xmlparser.findall(xml_rec, xpath)
            return sep.join([g.text for g in groups])

        record = {
            'hasAttachments': xml_rec.attrib['hasAttachments'],
            'ObjObjectNumberTxt': xml_text(
                f".//{{{ZETCOM_NS}}}dataField[@name='ObjObjectNumberTxt']/{{{ZETCOM_NS}}}value"
            ),
            'ObjObjectTitleGrp': xml_text(
                f".//{{{ZETCOM_NS}}}repeatableGroup[@name='ObjObjectTitleGrp']"
                f"//{{{ZETCOM_NS}}}dataField[@name='TitleTxt']"
                f"//{{{ZETCOM_NS}}}value"
            ),
            'ObjPerAssociationRef': xml_text(
                f".//{{{ZETCOM_NS}}}moduleReference[@name='ObjPerAssociationRef']"
                f"/{{{ZETCOM_NS}}}moduleReferenceItem"
                f"/{{{ZETCOM_NS}}}formattedValue"
            ),
            'ObjGeograficGrp': xml_text(
                f".//{{{ZETCOM_NS}}}repeatableGroup[@name='ObjGeograficGrp']"
                f"//{{{ZETCOM_NS}}}vocabularyReference[@name='PlaceVoc']"
                f"//{{{ZETCOM_NS}}}formattedValue"
            ),
            'ObjDateTxt': xml_text(
                f".//{{{ZETCOM_NS}}}dataField[@name='ObjDateTxt']/{{{ZETCOM_NS}}}value"
            ),
            'ObjDimAllGrp': xml_text(
                f".//{{{ZETCOM_NS}}}repeatableGroup[@name='ObjDimAllGrp']"
                f"//{{{ZETCOM_NS}}}virtualField[@name='PreviewVrt']"
                f"//{{{ZETCOM_NS}}}value"
            ),
            'ObjMaterialTechniqueGrp': xml_text(
                f".//{{{ZETCOM_NS}}}repeatableGroup[@name='ObjMaterialTechniqueGrp']"
                f"//{{{ZETCOM_NS}}}dataField[@name='DetailsTxt']"
                f"//{{{ZETCOM_NS}}}value"
            ),
            'ObjCreditlineGrp': xml_text(
                f".//{{{ZETCOM_NS}}}repeatableGroup[@name='ObjCreditlineGrp']"
                f"//{{{ZETCOM_NS}}}dataField[@name='CreditlineTxt']"
                f"//{{{ZETCOM_NS}}}value"
            ),
            'ObjOwnershipRef': xml_group(
                f".//{{{ZETCOM_NS}}}moduleReference[@name='ObjOwnershipRef']"
                f"/{{{ZETCOM_NS}}}moduleReferenceItem"
                f"/{{{ZETCOM_NS}}}formattedValue"
            ),
            'ObjScientificNotesClb': xml_text(
                f".//{{{ZETCOM_NS}}}dataField[@name='ObjScientificNotesClb']/{{{ZETCOM_NS}}}value"
            ),
            'ObjLiteratureRef': xml_text(
                f".//{{{ZETCOM_NS}}}moduleReference[@name='ObjLiteratureRef']"
                f"/{{{ZETCOM_NS}}}moduleReferenceItem"
                f"/{{{ZETCOM_NS}}}formattedValue"
            ),
            'ObjMultimediaRef': xml_text(
                f".//{{{ZETCOM_NS}}}moduleReference[@name='ObjMultimediaRef']"
                f"/{{{ZETCOM_NS}}}moduleReferenceItem"
                f"/{{{ZETCOM_NS}}}formattedValue"
            ),
        }
        return record

    def __repr__(self):
        try:
            return (
                'SearchResponse('
                'count=%r,'
                'limit=%r,'
                'offset=%r)'
                ) % (
                   self.count,
                   self.limit,
                   self.offset
                )
        except AttributeError:
            return 'SearchResponse(empty)'

    def __length_hint__(self):
        return self.count

    def __iter__(self):
        # use while loop since self.records could grow while iterating
        i = 0
        while True:
            # load new data when near end
            if i == len(self.records):
                try:
                    self._load_new_data()
                except errors.NoMoreRecordsError:
                    break
            yield self.records[i]
            i += 1

    def __getitem__(self, key):
        if isinstance(key, slice):
            limit = max(key.start or 0, key.stop or self.count)
            self._load_new_data_until(limit)
            count = len(self.records)
            return [self.records[k] for k in range(*key.indices(count))]

        if not isinstance(key, int):
            raise TypeError("Index must be an integer or slice")

        limit = key
        if limit < 0:
            # if we get a negative index, load all data
            limit = self.count
        self._load_new_data_until(limit)
        return self.records[key]

    def _load_new_data_until(self, limit):
        while limit >= len(self.records):
            try:
                self._load_new_data()
            except errors.NoMoreRecordsError:
                break

    def _load_new_data(self):
        self.offset = self.offset + self.limit
        if self.offset >= self.count:
            raise errors.NoMoreRecordsError("There are no more records")
        xml = self.data_loader.load(limit=self.limit, offset=self.offset)
        self._parse_content(xml)
