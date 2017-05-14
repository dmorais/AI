# This script studies the emotional content of a twitter

import tweepy
from textblob import TextBlob


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

# get the tweets
public_tweets = api.search('Dana White')

for tweet in public_tweets:
    print tweet.text
    analysis = TextBlob(tweet.text)
    print analysis.sentiment
