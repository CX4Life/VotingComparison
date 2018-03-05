import json
import os

USER_HOME_DIR = os.path.expanduser('~')
VOTING_COMPARISON_DIR = USER_HOME_DIR + '/PycharmProjects/VotingComparison'
PATH_TO_VOTES = USER_HOME_DIR + '/PycharmProjects' + '/congress/data'


def json_loader(filepath):
    with open(filepath, 'r') as current:
        return json.load(current)


def json_dump(filepath, data):
    with open(filepath, 'w') as current:
        json.dump(data, current, indent=4)


def get_entities(bill):
    sentiments = json_loader('sentiment_out.json')
    return sentiments.get(bill)


def rep_votes():
    rep_sentiment = {}

    bill_summaries = json_loader('bill_summaries.json')

    for congress_meeting in os.listdir(PATH_TO_VOTES):
        if congress_meeting >= "113":
            for year in os.listdir(PATH_TO_VOTES + '/' + congress_meeting + '/votes'):

                for vote_folder in os.listdir(PATH_TO_VOTES + '/' + congress_meeting + '/votes/' + year):
                    vote_data = json_loader(PATH_TO_VOTES
                                            + '/'
                                            + congress_meeting
                                            + '/votes/'
                                            + year
                                            + '/'
                                            + vote_folder
                                            + '/data.json')

                    if 'bill' in vote_data:
                        congress = str(vote_data['bill']['congress'])
                        number = str(vote_data['bill']['number'])
                        bill_type = vote_data['bill']['type']

                        if (congress is not None
                                and number is not None
                                and bill_type is not None):
                            bill_id = bill_type + number + '-' + congress
                            #passage = vote_data['category']
                            #result = vote_data['result']
                            if bill_id in bill_summaries:
                                #if vote_data['category'] is 'passage':

                                entities = get_entities(bill_id)
                                if entities is not None:
                                    if 'votes' in vote_data:
                                        if 'Nay' in vote_data['votes']:
                                            for Nay in vote_data['votes']['Nay']:
                                                rep_sentiment = process_vote(rep_sentiment, Nay['id'], False, entities)

                                        if 'No' in vote_data['votes']:
                                            for No in vote_data['votes']['No']:
                                                rep_sentiment = process_vote(rep_sentiment, No['id'], False, entities)

                                        if 'Aye' in vote_data['votes']:
                                            for Aye in vote_data['votes']['Aye']:
                                                rep_sentiment = process_vote(rep_sentiment, Aye['id'], True, entities)

                                        if 'Yes' in vote_data['votes']:
                                            for Yes in vote_data['votes']['Yes']:
                                                rep_sentiment = process_vote(rep_sentiment, Yes['id'], True, entities)

                                        if ('Nay' not in vote_data['votes']
                                                and 'No' not in vote_data['votes']
                                                and 'Aye' not in vote_data['votes']
                                                and 'Yes' not in vote_data['votes']):
                                            print("ERROR: no votes in %s" % bill_id)
                                else:
                                    print("ERROR: could not find entites for bill %s" % bill_id)

                        else:
                            raise ValueError("No data for get_bill")

    json_dump(VOTING_COMPARISON_DIR + "/rep_sentiments.json", rep_sentiment)


def process_vote(rep_sentiment, repID, add, entities):
    if repID in rep_sentiment:
        current_rep = rep_sentiment[repID]
    else:
        current_rep = {}

    for entity in entities:
        salience = entities[entity]['salience']
        score = entities[entity]['score']
        magnitude = entities[entity]['magnitude']

        if entity not in current_rep:
            current_rep[entity] = 0

        if add:
            current_rep[entity] += score
        else:
            current_rep[entity] -= score

    rep_sentiment[repID] = current_rep
    return rep_sentiment


def main():
    #sentiment_stuff = {'salience': 1, 'score': 2, 'magnitude': 0.9}
    #entity = {'apples':sentiment_stuff}
    #sentiments = {'hr244-115':entity}
    #json_dump(VOTING_COMPARISON_DIR + "/sentiments.json", sentiments)
    rep_votes()


if __name__ == '__main__':
    main()