# coding: utf-8
"""
This processing import affiliation metadata for the Article Meta database.

input: CSV file formated as below

    PID;Collection;Publication Year;Journal Title;number label;Affiliation ID [aff1, aff2];Affiliaton as it was markedup; Affiliation Country as it was markedup;Normalized Affiliation;Normalized Affiliation Country;iso-3661

input example:

    S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|iso-3661

CSV Total parameters size: 11
"""
import os
import logging
import codecs
import re
import argparse
import csv

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

iso3661codes = [
    'BD', 'BE', 'BF', 'BG', 'BA', 'BB', 'WF', 'BL', 'BM', 'BN', 'BO', 'BH',
    'BI', 'BJ', 'BT', 'BU', 'BV', 'BW', 'WS', 'BQ', 'BR', 'BS', 'JE', 'WK',
    'BX', 'BY', 'BZ', 'RU', 'RW', 'RP', 'PC', 'TL', 'JT', 'TM', 'RA', 'RC',
    'RL', 'RM', 'RN', 'RO', 'RH', 'RI', 'TK', 'GW', 'GU', 'GT', 'GS', 'GR',
    'GQ', 'GP', 'JP', 'GY', 'GG', 'GF', 'GE', 'GD', 'GC', 'GB', 'GA', 'SV',
    'VN', 'GN', 'GM', 'GL', 'GI', 'GH', 'OM', 'TN', 'WV', 'WG', 'JM', 'WL',
    'OA', 'JO', 'UN', 'TA', 'HR', 'HV', 'HT', 'HU', 'HK', 'HN', 'SU', 'HM',
    'VD', 'VE', 'PR', 'PS', 'UA', 'PW', 'PT', 'PU', 'PZ', 'PY', 'JA', 'IQ',
    'PA', 'PF', 'PG', 'ZW', 'PE', 'PK', 'PH', 'PI', 'PN', 'PL', 'PM', 'EM',
    'ZM', 'EH', 'EE', 'EG', 'EF', 'EA', 'ZA', 'EC', 'IT', 'UK', 'TJ', 'EZ',
    'EU', 'ET', 'EW', 'EV', 'EP', 'ES', 'ER', 'ME', 'MD', 'MG', 'MF', 'MA',
    'MC', 'UZ', 'MM', 'ML', 'MO', 'MN', 'MI', 'MH', 'MK', 'MU', 'MT', 'MW',
    'MV', 'MQ', 'MP', 'MS', 'MR', 'IM', 'UG', 'TZ', 'MY', 'MX', 'IL', 'FQ',
    'FR', 'IO', 'FX', 'SH', 'RE', 'SJ', 'FI', 'FJ', 'FK', 'FL', 'FM', 'FO',
    'NH', 'NI', 'IB', 'NL', 'NO', 'NA', 'VU', 'NC', 'NE', 'NF', 'NG', 'NZ',
    'ZR', 'NP', 'NQ', 'NR', 'SO', 'NT', 'NU', 'CK', 'CI', 'CH', 'CO', 'CN',
    'CM', 'CL', 'CC', 'CA', 'CG', 'CF', 'CD', 'CZ', 'CY', 'CX', 'WO', 'CS',
    'CR', 'CP', 'CW', 'CV', 'CU', 'CT', 'SZ', 'SY', 'SX', 'KG', 'KE', 'SS',
    'SR', 'KI', 'KH', 'KN', 'KM', 'ST', 'SK', 'KR', 'SI', 'KP', 'KW', 'SN',
    'SM', 'SL', 'SC', 'KZ', 'KY', 'SG', 'SF', 'SE', 'SD', 'DO', 'DM', 'DJ',
    'DK', 'VG', 'DG', 'DD', 'DE', 'YE', 'YD', 'DZ', 'US', 'DY', 'UY', 'YU',
    'YT', 'YV', 'LF', 'UM', 'LB', 'LC', 'LA', 'TV', 'TW', 'TT', 'RB', 'TR',
    'LK', 'TP', 'LI', 'LV', 'TO', 'LT', 'LU', 'LR', 'LS', 'TH', 'TF', 'TG',
    'TD', 'TC', 'LY', 'VA', 'AC', 'VC', 'AE', 'AD', 'AG', 'AF', 'AI', 'VI',
    'IS', 'IR', 'AM', 'AL', 'AO', 'AN', 'AQ', 'AP', 'AS', 'AR', 'AU', 'AT',
    'AW', 'IN', 'AX', 'IC', 'AZ', 'IE', 'ID', 'SB', 'RS', 'QA', 'SA', 'MZ'
]


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


def parse_csv_line(data):
    parsed_data = {}

    line = '|'.join(data)

    if len(data) != 12:
        logging.error('line has an invalid number of fields (%s)' % line)
        return False

    pid = data[1].strip()

    if not is_valid_pid(pid):
        logging.error('line has an invalid PID (%s)' % line)
        return False

    data[2] = data[2].strip().lower()
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
    parsed_data['normalized_affiliation_iso_3661_country'] = data[11].strip()

    logging.debug('line has been parsed')

    return parsed_data


def is_clean_checked(parsed_line, original_article):
    """
        Check's if the metadata in the given parsed_line is
        valid. To be valid it must have some similarities with
        the original_article.
    """

    if parsed_line['pid'] != original_article.publisher_id:
        logging.error('Invalid metadata (PID) reading line (%s)' % parsed_line['mfn'])
        return False

    affstr = parsed_line['affiliation_index'].strip().lower()

    if not original_article.affiliations:
        logging.error('Invalid metadata (Affiliation Index) reading (%s). Record does not have affiliations' % parsed_line['mfn'])
        return False

    if not parsed_line['normalized_affiliation_iso_3661_country'] in iso3661codes:
        logging.error('Invalid metadata (Country ISO-3661 code: %s) reading line (%s).' % (parsed_line['normalized_affiliation_iso_3661_country'], parsed_line['mfn']))

    aff = False
    for affiliation in original_article.affiliations:
        affstrorig = affiliation.get('index', '').strip().lower()
        if affstr == affstrorig:
            logging.debug('Affiliation match index input (%s) original (%s)' % (affstr, affstrorig))
            aff = True
            break

    if not aff:
        logging.error('Invalid metadata (Affiliation Index) reading line (%s). Record does not have a matching affiliation' % parsed_line['mfn'])
        return False

    logging.debug('line was validated agains original metadata (PID, Affiliation Index, Country ISO-3661 code)')

    return True


def get_original_article(pid, collection):
    query = {'code': pid, 'collection': collection}
    try:
        json_article = scielo_network_articles.find_one(query)

        if not json_article:
            return None

        article = Article(json_article)
        logging.debug('original metadata retrieved from Article Meta')
        return article
    except:
        logging.error('Fail to retrieve (%s)' % str(query))


def isis_like_json(data):
    institutions = []

    for item in data:
        institution = {}

        if 'affiliation_index' in item:
            institution['i'] = item['affiliation_index'].upper()

        if 'normalized_affiliation_name' in item:
            institution['_'] = item['normalized_affiliation_name']

        if 'normalized_affiliation_iso_3661_country' in item:
            institution['p'] = item['normalized_affiliation_iso_3661_country']

        institutions.append(institution)

    return institutions


def import_doc_affiliations(data):

    for key, value in data.items():
        ilj = isis_like_json(value)
        collection = value[0]['collection']
        code = value[0]['pid']

    try:
        scielo_network_articles.update(
            {
                'code': code,
                'collection': collection
            },
            {
                '$set': {
                    'article.v240': ilj
                }
            }
        )
        logging.debug('reacording at(%s): ' % code)
    except:
        logging.error('Error recording metadata at (%s): ' % code)


def check_affiliations(file_name='processing/normalized_affiliations.csv', import_data=False, encoding='utf-8'):

    logging.info('reading file (%s)' % file_name)

    original_article = None

    line_count = 0
    doc_affiliations = {}
    with codecs.open(file_name, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        for line in spamreader:
            line_count += 1

            logging.debug('reading line (%s)' % line_count)
            parsed_line = parse_csv_line([str(line_count)] + line)
            if not parsed_line:
                continue

            original_article = get_original_article(
                parsed_line['pid'], parsed_line['collection']
            )

            if not original_article:
                continue

            if not is_clean_checked(parsed_line, original_article):
                continue

            if import_data:
                if not parsed_line['pid'] in doc_affiliations and len(doc_affiliations) == 1:
                    import_doc_affiliations(doc_affiliations)
                    doc_affiliations = {}
                pl = doc_affiliations.setdefault(parsed_line['pid'], [])
                pl.append(parsed_line)

        # import the last document
        import_doc_affiliations(doc_affiliations)

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
