# coding: utf-8
"""
This processing fix documents pages.

input: CSV file formated as below

    Collection|PID|Publication Year|Journal Title|s

input example:
    scl|S0001-37652013000100001|first page|first page seq|last page|e-location|ahead id
"""
import logging
import codecs
import re
import argparse
import csv

from xylose.scielodocument import Article

from articlemeta import utils
from articlemeta import controller


logger = logging.getLogger(__name__)


REGEX_ARTICLE = re.compile("^S[0-9]{4}-[0-9]{3}[0-9xX][0-2][0-9]{3}[0-9]{4}[0-9]{5}$")

try:
    articlemeta_db = controller.DataBroker.from_dsn(MONGODB_HOST).db
except:
    raise ValueError('Fail to connect to (%s)', MONGODB_HOST)

trans_collections_code = {
    'bra': 'scl',
    'scl': 'scl',
    'arg': 'arg',
    'col': 'col',
    'esp': 'esp',
    'spa': 'spa',
    'prt': 'prt',
    'chl': 'chl',
    'ven': 'ven',
    'ury': 'ury',
    'cri': 'cri',
    'sza': 'sza',
    'cub': 'cub'
}


def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.setLevel(allowed_levels.get(logging_level, 'INFO'))

    if logging_file:
        hl = logging.FileHandler(logging_file, mode='a')
    else:
        hl = logging.StreamHandler()

    hl.setFormatter(formatter)
    hl.setLevel(allowed_levels.get(logging_level, 'INFO'))

    logger.addHandler(hl)

    return logger


def is_valid_pid(pid):

    if REGEX_ARTICLE.search(pid):
        return True

    return False


def parse_csv_line(data):
    parsed_data = {}

    line = ','.join(data)

    if len(data) != 8:
        logger.error(u'line has an invalid number of fields (%s)', line)
        return False

    pid = data[2].strip()

    if not is_valid_pid(pid):
        logger.error(u'line has an invalid PID (%s)', line)
        return False

    data[1] = data[1].strip().lower()
    if not data[1] in trans_collections_code:
        logger.error(u'line has an invalid collection code (%s)', line)
        return False

    parsed_data['mfn'] = data[0].strip()
    parsed_data['pid'] = pid
    parsed_data['collection'] = trans_collections_code[data[1]]
    parsed_data['first_page'] = data[3]
    parsed_data['first_page_seq'] = data[4]
    parsed_data['last_page'] = data[5]
    parsed_data['elocation'] = data[6]
    parsed_data['ahead_id'] = data[7]
    logger.debug('line has been parsed')

    return parsed_data


def get_original_article(pid, collection):
    query = {'code': pid, 'collection': collection}
    try:
        json_article = scielo_network_articles.find_one(query)

        if not json_article:
            return None

        article = Article(json_article)
        logger.debug(u'original metadata retrieved from Article Meta')
        return article
    except:
        logger.error(u'Fail to retrieve (%s)', str(query))


def fix_pages(data):

    pages = {'_': ''}

    if data['first_page']:
        pages['f'] = data['first_page']

    if data['first_page_seq']:
        pages['s'] = data['first_page_seq']

    if data['last_page']:
        pages['l'] = data['last_page']

    if data['elocation']:
        pages['e'] = data['elocation']

    try:
        scielo_network_articles.update(
            {
                'code': data['pid'],
                'collection': data['collection']
            },
            {
                '$set': {
                    'article.v14': [pages],
                    'sent_wos': 'False'
                }
            }
        )
        logger.debug(u'reacording at (%s-%s): %s', data['collection'], data['pid'], unicode(pages))
    except:
        logger.error(u'Error recording metadata at (%s-%s): %s', data['collection'], data['pid'], unicode(pages))


def check_affiliations(file_name, import_data=False, encoding='utf-8'):

    logger.info('reading file (%s)', file_name)

    line_count = 0
    with codecs.open(file_name, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        lines = []
        for line in spamreader:
            lines.append([i.decode(encoding) for i in line])

    for line in sorted(lines):
        line_count += 1

        logger.debug('reading line (%s)', line_count)
        parsed_line = parse_csv_line([str(line_count)] + line)

        if not parsed_line:
            continue

        if not import_data:
            continue

        fix_pages(parsed_line)


def main():

    parser = argparse.ArgumentParser(
        description="Load normalized affiliation data to the article meta database"
    )

    parser.add_argument(
        '--csv_file',
        '-f',
        required=True,
        help='Input CSV file within the normalized metadata'
    )

    parser.add_argument(
        '--data_encoding',
        '-e',
        default='utf-8',
        help='Encoding of the csv file'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        help='Full path to the log file'
    )

    parser.add_argument(
        '--logging_level',
        '-l',
        default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logggin level'
    )

    parser.add_argument(
        '--import_data',
        '-i',
        action='store_true',
        help='Define if the data will be imported or the processing you just run to check the input file and logs'
    )

    args = parser.parse_args()

    _config_logging(args.logging_level, args.logging_file)

    check_affiliations(
        file_name=args.csv_file,
        import_data=args.import_data
    )
