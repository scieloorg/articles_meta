#coding: utf-8
import xml.etree.ElementTree as ET

import plumber


class SetupArticlePipe(plumber.Pipe):

    def transform(self, data):

        xml = ET.Element('ArticleSet')

        return data, xml
