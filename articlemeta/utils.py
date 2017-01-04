# coding: utf-8
import os
import weakref

from configparser import ConfigParser


def convert_ahref_to_extlink(xml_etree):
    """
        This methods receives an etree node and replace all "a href" elements to
        a valid ext-link jats compliant format.
    """

    for ahref in xml_etree.findall('.//a'):
        uri = ahref.get('href', '')
        ahref.tag = 'ext-link'
        ahref.set('ext-link-type', 'uri')
        ahref.set('{http://www.w3.org/1999/xlink}href', uri)
        for key in [i for i in ahref.keys() if i not in ['ext-link-type', '{http://www.w3.org/1999/xlink}href']]:
            ahref.attrib.pop(key)

    return xml_etree


def convert_html_tags_to_jats(xml_etree):
    """
        This methods receives an etree node and replace all "html tags" to
        jats compliant tags.
    """

    tags = (
        ('strong', 'bold'),
        ('i', 'italic'),
        ('u', 'underline'),
        ('small', 'sc')
    )

    for from_tag, to_tag in tags:
        for element in xml_etree.findall('.//'+from_tag):
            element.tag = to_tag

    return xml_etree


def convert_all_html_tags_to_jats(xml_etree):
    xml_etree = convert_ahref_to_extlink(xml_etree)
    xml_etree = convert_html_tags_to_jats(xml_etree)

    return xml_etree


class SingletonMixin(object):
    """
    Adds a singleton behaviour to an existing class.

    weakrefs are used in order to keep a low memory footprint.
    As a result, args and kwargs passed to classes initializers
    must be of weakly refereable types.
    """
    _instances = weakref.WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        key = (cls, args, tuple(kwargs.items()))

        if key in cls._instances:
            return cls._instances[key]

        new_instance = super(type(cls), cls).__new__(cls, *args, **kwargs)
        cls._instances[key] = new_instance

        return new_instance


class Configuration(SingletonMixin):
    """
    Acts as a proxy to the ConfigParser module
    """
    def __init__(self, fp, parser_dep=ConfigParser):
        self.conf = parser_dep()
        self.conf.readfp(fp)

    @classmethod
    def from_env(cls):
        try:
            filepath = os.environ['ARTICLEMETA_SETTINGS_FILE']
        except KeyError:
            raise ValueError('missing env variable ARTICLEMETA_SETTINGS_FILE')

        return cls.from_file(filepath)

    @classmethod
    def from_file(cls, filepath):
        """
        Returns an instance of Configuration

        ``filepath`` is a text string.
        """
        fp = open(filepath, 'r')
        return cls(fp)

    def __getattr__(self, attr):
        return getattr(self.conf, attr)

    def items(self):
        """Settings as key-value pair.
        """
        return [(section, dict(self.conf.items(section, raw=True))) for \
            section in [section for section in self.conf.sections()]]
