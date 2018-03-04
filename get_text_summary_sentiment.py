import json
import sys
from google.cloud import language
from google-cloud.language import enums
from google.cloud.language import types

__author__ = 'Tim Woods'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018, Tim Woods'

TEST_FILENAME = 'foo.json'
REAL_FILENAME = 'real.json'
WRITE_TO = 'sentiment_out.json'


def get_sentiment_from_text(vote_text, client, encoding):
    ret = {}
    document = types.Document(
        content=vote_text,
        type=enums.Document.Type.PLAIN_TEXT)

    results = client.analyze_entity_sentiment(document, encoding)
    for entity in results.entities:
        if not -0.2 < entity.sentiment < 0.2:
            ret[entity] = {
                'salience': entity.salience,
                'sentiment': entity.sentiment
            }
    if not ret:
        print('Well, that entity analysis did not work.')
    return ret


def json_sentiments_from_json_texts(json_filename, encoding):
    client = language.LanguageServiceClient()
    sentiments_by_id = {}
    with open(json_filename, 'r') as texts:
        id_text_dict = json.load(texts)
    for vote_id in id_text_dict.keys():
        sentiments_by_id[vote_id] = get_sentiment_from_text(id_text_dict[vote_id], client, encoding)

    print('all text analyzed')
    with open(WRITE_TO, 'w') as json_output:
        json.dump(sentiments_by_id, json_output)


def main():
    client = language.LanguageServiceClient()
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    json_sentiments_from_json_texts(TEST_FILENAME, encoding)

if __name__ == '__main__':
    main()
