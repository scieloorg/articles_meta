# coding: utf-8
"""
This processing import affiliation metadata for the Article Meta database.

input: CSV file formated as below

    isis record index;PID;Collection;Publication Year;Journal Title;number label;Affiliation ID [aff1, aff2];Affiliaton as it was markedup; Affiliation Country as it was markedup;Normalized Affiliation;Normalized Affiliation Country

input example:

    27136;S0001-37652013000100001;scl;2013;An. Acad. Bras. Ciênc.;v85n1;aff1;Museu Nacional/UFRJ;Brasil;Universidade Federal do Rio de Janeiro;Brazil

CSV Total parameters size: 10
"""
import os
import logging
import codecs
import re
import argparse
from ConfigParser import SafeConfigParser

from pymongo import Connection
from articlemeta import utils

from xylose.scielodocument import Article

config = utils.Configuration.from_file(os.environ.get('CONFIG_INI', os.path.dirname(__file__)+'/../config.ini'))
settings = dict(config.items())

REGEX_ARTICLE = re.compile("^S[0-9]{4}-[0-9]{3}[0-9xX][0-2][0-9]{3}[0-9]{4}[0-9]{5}$")

try:
    scielo_network_articles = Connection(settings['app']['mongo_uri'])['scielo_network']['articles']
except:
    logging.error('Fail to connect to (%s)' % settings['app']['mongo_uri'])


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

    logging_config = {
        'level': allowed_levels.get(logging_level, 'INFO'),
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }

    if logging_file:
        logging_config['filename'] = logging_file

    logging.basicConfig(**logging_config)


def is_valid_pid(pid):

    if REGEX_ARTICLE.search(pid):
        return True

    return False


def parse_csv_line(line):
    data = line.split(';')

    parsed_data = {}
    if len(data) != 11:
        logging.error('line has an invalid number of fields (%s)' % line)
        return False

    pid = data[1].strip()

    if not is_valid_pid(pid):
        logging.error('line has an invalid PID (%s)' % line)
        return False

    if not data[2] in trans_collections_code:
        logging.error('line has an invalid collection code (%s)' % line)
        return False

    parsed_data['mfn'] = data[0].strip()
    parsed_data['pid'] = pid
    parsed_data['collection'] = trans_collections_code[data[2]]
    parsed_data['publication_year'] = data[3].strip()
    parsed_data['journal_title'] = data[4].strip()
    parsed_data['issue_label'] = data[5].strip()
    parsed_data['affiliation_index'] = data[6].strip()
    parsed_data['markup_affiliation_name'] = data[7].strip()
    parsed_data['markup_affiliation_country'] = data[8].strip()
    parsed_data['normalized_affiliation_name'] = data[9].strip()
    parsed_data['normalized_affiliation_country'] = data[10].strip()

    logging.debug('line has been parsed')

    return parsed_data


def is_clean_checked(parsed_line, original_article):
    """
        Check's if the metadata in the given parsed_line is
        valid. To be valid it must have some similarities with
        the original_article.
    """
    if parsed_line['pid'] != original_article.publisher_id:
        logging.error('Invalid metadata (PID) reading line with mfn (%s)' % parsed_line['mfn'])
        return False

    affstr = parsed_line['affiliation_index'].strip().lower()

    if not original_article.affiliations:
        logging.error('Invalid metadata (Affiliation Index) reading line with mfn (%s). Record does not have affiliations' % parsed_line['mfn'])
        return False

    aff = False
    for affiliation in original_article.affiliations:
        affstrorig = affiliation.get('index', '').strip().lower()
        if affstr == affstrorig:
            logging.debug('Affiliation match index input (%s) original (%s)' % (affstr, affstrorig))
            aff = True
            break

    if not aff:
        logging.error('Invalid metadata (Affiliation Index) reading line with mfn (%s). Record does not have a matching affiliation' % parsed_line['mfn'])
        return False

    logging.debug('line was validated agains original metadata (PID, Affiliation Index)')

    return True


def get_original_article(pid, collection):
    query = {'code': pid, 'collection': collection}
    try:
        json_article = scielo_network_articles.find_one(query)
        article = Article(json_article)
        logging.debug('original metadata retrieved from Article Meta')
        return article
    except:
        logging.error('Fail to retrieve (%s)' % str(query))    


def isis_like_json(data):
    institution = {}

    if 'affiliation_index' in data:
        institution['i'] = data['affiliation_index'].upper()

    if 'normalized_affiliation_name' in data:
        institution['_'] = data['normalized_affiliation_name']

    if 'normalized_affiliation_country' in data:
        institution['p'] = data['normalized_affiliation_country']

    return institution


def import_affiliation(data):
    ilj = isis_like_json(data)

    try:
        scielo_network_articles.update(
            {
                'code': data['pid'],
                'collection': data['collection']
            },
            {
                '$push':
                {
                    'article.v240': ilj
                }
            }
        )
        logging.debug('reacording at(%s): ' % (data['pid'], str(ilj)))
    except:
        logging.error('Error recording metadata at(%s): ' % (data['pid'], str(ilj)))


def check_affiliations(file_name='processing/normalized_affiliations.csv', import_data=False, encoding='utf-8'):

    logging.info('reading file (%s)' % file_name)

    original_article = None

    with codecs.open(file_name, 'r', encoding=encoding) as f:
        for line in f:
            logging.debug('reading line (%s)' % line.strip())
            parsed_line = parse_csv_line(line.strip())

            if not parsed_line:
                continue

            original_article = get_original_article(parsed_line['pid'], parsed_line['collection'])

            if not original_article:
                continue

            if not is_clean_checked(parsed_line, original_article):
                continue

            if import_data:
                import_affiliation(parsed_data)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Load normalized affiliation data to the article meta database"
    )

    parser.add_argument(
        '--csv_file',
        '-f',
        default='/tmp/normalized_affiliations.csv',
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
        default='/tmp/import_affiliations.log',
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