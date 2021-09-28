# museumpy

**museum**py is a client for python to get data from [Zetcom MuseumPlus](https://www.zetcom.com/en/museumplus-en/) instances.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
    * [`search`](#search)
    * [`fulltext_search`](#fulltext_search)
* [Advanced Usage](#advanced-usage)
    * [`module_item`](#module_item)
    * [`download_attachement`](#download_attachement)
    * [Custom mapping of fields](#custom-mapping-of-fields)
* [Release](#release)

## Installation

[museumpy is available on PyPI](https://pypi.org/project/museumpy/), so to install it simply use:

```
$ pip install museumpy
```

## Usage

See the [`examples` directory](/examples) for more scripts.

### `search`

```python
import museumpy

records = museumpy.search(
    base_url='https://mpzurichrietberg.zetcom.com/MpWeb-mpZurichRietberg',
    field='ObjObjectNumberTxt',
    value='2019.184',
)


for record in records:
    print(record)
```


The return value of `search` is iterable, so you can easily loop over it. Or you can use indices to access elements, e.g. `records[1]` to get the second element, or `records[-1]` to get the last one.

Even [slicing](https://python-reference.readthedocs.io/en/latest/docs/brackets/slicing.html) is supported, so you can do things like only iterate over the first 5 elements using

```python
for records in records[:5]:
   print(record)
```

### `fulltext_search`
```python
import museumpy

records = museumpy.fulltext_search(
    base_url='https://test.zetcom.com/MpWeb-mpTest',
    query='Patolu',
)


for record in records:
    print(record)
```

## Advanced usage

For more advanced usage of this library, it is recommened to first create a client instance and then use this to request data:

```python
import museumpy

client = museumpy.MuseumPlusClient(
    base_url='https://test.zetcom.com/MpWeb-mpTest',
    requests_kwargs={'auth': (user, pw)}
)

```


### `module_item`
```python
import museumpy

id = '98977'
module = 'Multimedia'
item = client.module_item(id, module)
```

### `download_attachement`
```python
import museumpy

id = '98977'
module = 'Multimedia'
# download attachment to a directory called `files`
attachment_path = client.download_attachment(id, module, 'files')
print(attachment_path)
```

### Custom mapping of fields

There are most likely custom fields on the MuseumPlus Instance you want to query.
The returned XML is converted to a python `dict` using the [`xmltodict` library](https://pypi.org/project/xmltodict/).
The raw dict is returned on the `raw` key of the result:

```python
import museumpy

records = museumpy.search(
    base_url='https://test.zetcom.com/MpWeb-mpTest',
    query='Patolu',
)
for record in records:
    print(record['raw'])
```

For convenience a default mapping is provided to access some fields more easily:


```python
for record in records:
    print(record['hasAttachments'])
    print(record['ObjObjectNumberTxt'])
```

If you want to customize this mapping, you can pass a `map_function` to the client, which is then used on all subsequent calls to `search` and `fulltext_search`:


```python
import museumpy

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
    base_url='https://test.zetcom.com/MpWeb-mpTest',
    map_function=my_custom_map,
)

records = client.search(
    base_url='https://test.zetcom.com/MpWeb-mpTest',
    query='Patolu',
)
for record in records:
    print(record['my_id'])
    print(record['my_title'])

```

## Release

To create a new release, follow these steps (please respect [Semantic Versioning](http://semver.org/)):

1. Adapt the version number in `museumpy/__init__.py`
1. Update the CHANGELOG with the version
1. Create a [pull request to merge `develop` into `main`](https://github.com/metaodi/museumpy/compare/main...develop?expand=1) (make sure the tests pass!)
1. Create a [new release/tag on GitHub](https://github.com/metaodi/museumpy/releases) (on the main branch)
1. The [publication on PyPI](https://pypi.python.org/pypi/museumpy) happens via [GitHub Actions](https://github.com/metaodi/museumpy/actions?query=workflow%3A%22Upload+Python+Package%22) on every tagged commit
