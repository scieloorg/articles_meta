# coding: utf-8
import os

import thriftpy

articlemeta_thrift = thriftpy.load(
    os.path.dirname(__file__)+'/articlemeta.thrift',
    module_name='articlemeta_thrift'
)

from thriftpy.rpc import make_client

if __name__ == '__main__':
    client = make_client(
        articlemeta_thrift.ArticleMeta,
        '127.0.0.1',
        11720
    )

    #article = client.get_article('S0034-71672014000600891', collection='scl', replace_journal_metadata=True)

    identifiers = client.get_journal_identifiers('scl', 1000, 0)

