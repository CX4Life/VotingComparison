import json
import sys
import time
from google.cloud import language
from census_loader import printProgressBar
from google.cloud.language import enums
from google.cloud.language import types

__author__ = 'Tim Woods'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018, Tim Woods'

TEST_FILENAME = 'foo.json'
REAL_FILENAME = 'bill_summaries.json'
WRITE_TO = 'sentiment_out.json'
LOG_FILE = 'errors_sentiment.txt'


def get_sentiment_from_text(vote_text, client, encoding, vote_name):
    ret = {}
    try:
        document = types.Document(
            content=vote_text.lower(),
            type=enums.Document.Type.PLAIN_TEXT)

        results = client.analyze_entity_sentiment(document, encoding)
        for entity in results.entities:
            if not -0.2 < entity.sentiment.score < 0.2:
                ret[entity.name] = {
                    'salience': entity.salience,
                    'score': entity.sentiment.score,
                    'magnitude': entity.sentiment.magnitude
                }
    except:
        print('Error on', vote_name)
        with open(LOG_FILE, 'wr') as log:
            log.write(time.time() + vote_name)
    return ret


def json_sentiments_from_json_texts(json_filename, encoding):
    client = language.LanguageServiceClient()
    sentiments_by_id = {}
    with open(json_filename, 'r') as texts:
        id_text_dict = json.load(texts)
    for i, vote_id in enumerate(id_text_dict.keys()):
        num_to_iterate = max(len(id_text_dict.keys()) - 1, 1)
        if num_to_iterate == 1:
            i = 1
        printProgressBar(i, num_to_iterate, "Analyzing sentiments")
        sentiments_by_id[vote_id] = get_sentiment_from_text(id_text_dict[vote_id], client, encoding)

    print('all text analyzed')
    with open(WRITE_TO, 'w') as json_output:
        json.dump(sentiments_by_id, json_output, indent=2, sort_keys=True)


def main():
    client = language.LanguageServiceClient()
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    json_sentiments_from_json_texts(REAL_FILENAME, encoding)

if __name__ == '__main__':
    main()
