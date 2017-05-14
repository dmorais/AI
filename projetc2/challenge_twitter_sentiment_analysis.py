# This script studies the emotional content of a twitter

import tweepy
from textblob import TextBlob


def auth_get_api():

    f = open('keys.txt', 'r')
    lines = f.read().splitlines()

    consumer_key = lines[0]
    consumer_secret = lines[1]

    access_token = lines[2]
    access_token_secret = lines[3]


    # autheticate
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create an object that interacts with twitter
    api = tweepy.API(auth)

    return api

def get_sentiments(sentiment):

    polarity = ''
    subjectivity = ''
    if sentiment[0] == 0:
        polarity = 'neutral'
    elif sentiment[0] < 0:
        polarity = 'negative'
    else:
        polarity = 'positive'

    if sentiment[1] < 0.45:
        subjectivity = 'opinion only'
    elif (sentiment[1] >= 0.45  or sentiment[1] < 0.55):
        subjectivity = 'opinion with some objectivity'
    else:
        subjectivity = 'objective'

    return "{}, {}, {}, {}".format(polarity,subjectivity, sentiment[0], sentiment[1])



def main():

    api = auth_get_api()
    # get the tweets
    public_tweets = api.search('Dana White', show_user=True, count=100)

    for tweet in public_tweets:

        analysis = TextBlob(tweet.text)
        evaluation = get_sentiments(analysis.sentiment)
        print "{}, {}".format(evaluation, analysis)

if __name__ == "__main__":
    main()
