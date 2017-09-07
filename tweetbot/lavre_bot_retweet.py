import tweepy
from time import sleep
from keys import *
import argparse
import random
import sys
import os
import util.tweet as ut

# Access and authorize our Twitter credentials from keys.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def send_tweet(text):
    for line in text:

        try:
            if line != '\n':
                print "Tweeting new message"
                api.update_status(line)
                return
            else:
                pass
        except tweepy.TweepError as e:
            if 'Status is a duplicate' in e.reason:
                pass
            else:
                print e.reason
                sleep(5)


def retweet(hashtag):
    done = 1
    print "hashtag:", hashtag
    # For loop to iterate over tweets with hashtag key words limit to 2
    for tweet in tweepy.Cursor(api.search,
                               q=hashtag,
                               lang='pt').items(2):

        try:
            # Print out usernames of the last 2 people to use the hashtag
            print('Tweet by: @' + tweet.user.screen_name)

            tweet.retweet()
            print 'Retweeted the tweet from hashtag:' + hashtag
            done = 0
            sleep(5)

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break

    if done == 1:
        return "No tweet"


def fetch_tweet_data(file_name, tweet_last_modif, tweet_list):
    if ut.f_exists(file_name):

        if len(tweet_list) > 1:

            # if the file was modified since last read
            if os.path.getmtime(file_name) != tweet_last_modif:
                print "Tweet file was modified"
                tweet_last_modif = os.path.getmtime(file_name)
                tweet_list = ut.get_tweet(file_name)

        else:
            print "list is empty"
            tweet_list = ut.get_tweet(file_name)

    else:
        print "ERROR: The file containing the tweets was not found"
        sys.exit(1)

    return tweet_list, tweet_last_modif


def fetch_hashtag_data(file_name, kw_last_modif, keywords):
    if ut.f_exists(file_name):

        if len(keywords) > 1:

            # if the file was modified since last read
            if os.path.getmtime(file_name) != kw_last_modif:
                print "Hashtags file was modified"
                kw_last_modif = os.path.getmtime(file_name)
                keywords = ut.get_hashtags(file_name)
        else:

            print "list is empty"
            keywords = ut.get_hashtags(file_name)
    else:
        print "ERROR: The file containing the hashtags was not found"
        sys.exit(1)

    return keywords, kw_last_modif


def main():
    parser = argparse.ArgumentParser(description="A simple tweetbot")
    parser.add_argument("-f", "--file", action="store", help="tweet file", required=True)
    parser.add_argument("-k", "--key", action="store", help="keywords file", required=True)
    args = parser.parse_args()

    tweet_list = list()
    tweet_last_modif = 0

    keywords = list()
    kw_last_modif = 0

    while True:
        print "Getting list of tweets"
        tweet_list, tweet_last_modif = fetch_tweet_data(args.file, tweet_last_modif, tweet_list)

        print "Getting hashtags"
        keywords, kw_last_modif = fetch_hashtag_data(args.key, kw_last_modif, keywords)

        send_tweet(tweet_list)

        tweeted = retweet(random.choice(keywords))
        count = 0

        while tweeted == "No tweet" or count > 100:
            tweeted = retweet(random.choice(keywords))
            count += 1
            sleep(2)

        sleep(86400)


if __name__ == '__main__':
    main()
