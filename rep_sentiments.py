import json
import os

USER_HOME_DIR = os.path.expanduser('~')
VOTING_COMPARISON_DIR = USER_HOME_DIR + '/PycharmProjects/VotingComparison'
PATH_TO_VOTES = USER_HOME_DIR + '/PycharmProjects' + '/congress/data'


def json_dump(filepath, data):
    with open(filepath, 'w') as current:
        json.dump(data, current, indent=4)

def get_entities(bill):
    with open('sentiments.json', 'r') as sentiment_json:
        sentiments = json.load(sentiment_json)

        return sentiments.get(bill)
        # if bill in sentiments:
        #     return bill, sentiments[bill]
        # else:
        #     print("ERROR: could not find bill %s" % bill)


def rep_votes():
    rep_sentiment = {}

    for congress_meeting in os.listdir(PATH_TO_VOTES):
        if congress_meeting >= "113":
            for year in os.listdir(PATH_TO_VOTES + '/' + congress_meeting + '/votes'):

                for vote_folder in os.listdir(PATH_TO_VOTES + '/' + congress_meeting + '/votes/' + year):
                    with open(PATH_TO_VOTES
                              + '/'
                              + congress_meeting
                              + '/votes/'
                              + year
                              + '/'
                              + vote_folder
                              + '/data.json', 'r') as vote_file:
                        with open('bill_summaries.json', 'r') as bill_summaries_json:
                            vote_data = json.load(vote_file)
                            bill_summaries = json.load(bill_summaries_json)

                            if 'bill' in vote_data:
                                congress = str(vote_data['bill']['congress'])
                                number = str(vote_data['bill']['number'])
                                bill_type = vote_data['bill']['type']

                                if (congress is not None
                                        and number is not None
                                        and bill_type is not None):
                                    bill_id = bill_type + number + '-' + congress
                                    if (bill_id in bill_summaries
                                            and vote_data['category'] is 'passage'):

                                        entities = get_entities(bill_id)
                                        if entities is not None:
                                            if 'votes' in vote_data:
                                                if 'Nay' in vote_data['votes']:
                                                    for Nay in vote_data['votes']['Nay']:
                                                        process_vote(rep_sentiment, Nay['id'], False, entities)

                                                if 'No' in vote_data['votes']:
                                                    for No in vote_data['votes']['No']:
                                                        process_vote(rep_sentiment, No['id'], False, entities)

                                                if 'Aye' in vote_data['votes']:
                                                    for Aye in vote_data['votes']['Aye']:
                                                        process_vote(rep_sentiment, Aye['id'], True, entities)

                                                if 'Yes' in vote_data['votes']:
                                                    for Yes in vote_data['votes']['Yes']:
                                                        process_vote(rep_sentiment, Yes['id'], True, entities)

                                                if ('Nay' not in vote_data['votes']
                                                        and 'No' not in vote_data['votes']
                                                        and 'Aye' not in vote_data['votes']
                                                        and 'Yes' not in vote_data['votes']):
                                                    print("ERROR: no votes in %s" % bill_id)
                                        else:
                                            print("ERROR: could not find bill %s" % bill)



                                else:
                                    raise ValueError("No data for get_bill")

    json_dump(VOTING_COMPARISON_DIR + "/rep_sentiments.json", rep_sentiment)


def process_vote(rep_sentiment, repID, add, entities):
    #plus = ['Yes', 'Aye']
    #minus = ['Nay', 'No']

    if repID not in rep_sentiment:
        rep_sentiment['repID'] = repID

        for entity in entities:
            salience = entity['salience']
            score = entity['score']
            magnitude = entity['magnitude']

            current_rep = rep_sentiment[repID]

            if entity not in current_rep:
                current_rep['key'] = entity
                current_rep['score'] = 0

            #if Yea_or_Nay is in plus:
            if add:
                current_rep[entity] += score

            else:
                current_rep[entity] -= score


def main():
    sentiment_stuff = {'salience': 1, 'score': 2, 'magnitude': 0.9}
    entity = {'apples':sentiment_stuff}
    sentiments = {'hr2-113':entity}
    json_dump(VOTING_COMPARISON_DIR + "/sentiments.json", sentiments)
    rep_votes()


if __name__ == '__main__':
    main()