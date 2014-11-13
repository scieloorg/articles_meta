# coding: utf-8
import zerorpc
import argparse


from articlemeta import controller

class ArticleMetaRPC(object):

    def __init__(self, database):
        self.databroker = controller.DataBroker.from_dsn(
            'mongodb://localhost:27017/scielo_network',
            reuse_dbconn=True
        )

    def add_journal(self, metadata):
        """
        RPC interface for add_journal controller.
        """
        self.databroker.add_journal(metadata)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Article Meta RPC Server"
    )

    parser.add_argument(
        '--server',
        '-s',
        default="tcp://0.0.0.0:4242",
        help='RPC Server domain'
    )

    parser.add_argument(
        '--database',
        '-d',
        default="mongodb://127.0.0.1:27017/scielo_network",
        help='Mongodb Database'
    )

    args = parser.parse_args()

    server = zerorpc.Server(ArticleMetaRPC(args.database))
    server.bind(args.server)
    server.run()
