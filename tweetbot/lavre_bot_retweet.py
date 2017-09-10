import tweepy
from time import sleep
from datetime import datetime
from keys import *
import argparse
import random
import sys
import os
import util.tweet as ut
import logging
import util.loggerinitializer as utl

# Create Log dirs and object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
utl.initialize_logger(os.getcwd() + "/logs/", logger)

# Access and authorize our Twitter credentials from keys.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def send_tweet(text):
    if len(text) == 0:
        return text

    for line in text:
        sleep(10)
        try:
            if line != '\n':

                api.update_status(line)
                text.remove(line)

                logger.info("Tweeting new message")
                return text
            else:
                pass

        except tweepy.TweepError as e:
            if 'Status is a duplicate' in e.reason:
                logger.debug(e.reason)
                pass

            else:
                logger.error(e.reason)
                print e.reason
                sleep(5)

    return text


def retweet(hashtag):
    done = 1
    lang = random.choice(['pt', 'en'])

    logger.info("hashtag: " + hashtag + " lang: " + lang)

    for tweet in tweepy.Cursor(api.search,
                               q=hashtag,
                               lang=lang).items(50):

        try:

            # Prevent self tweets
            if tweet.user.screen_name == 'dallavre':
                continue

            # Only post tweets where user screen name is equals to the handle
            if (hashtag.startswith('@') and tweet.user.screen_name == hashtag[1:]) or (hashtag.startswith('#')):

                logger.info('Tweet by: @' + tweet.user.screen_name)

                tweet.retweet()
                logger.info("Retweeted the tweet from hashtag: " + hashtag + " in lang:" + lang)

                done = 0
                return 0

            else:
                logger.info("User: " + tweet.user.screen_name + " do not own the handle: " + hashtag)

            sleep(5)

        except tweepy.TweepError as e:

            logger.debug(e.reason)
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
                logger.info("Tweet file was modified")
                tweet_last_modif = os.path.getmtime(file_name)
                tweet_list = ut.get_tweet(file_name)

        else:
            logger.debug("list is empty")
            tweet_list = ut.get_tweet(file_name)

    else:
        logger.error("ERROR: The file containing the tweets was not found")
        print "ERROR: The file containing the tweets was not found"
        sys.exit(1)

    return tweet_list, tweet_last_modif


def fetch_hashtag_data(file_name, kw_last_modif, keywords):
    if ut.f_exists(file_name):

        if len(keywords) > 1:

            # if the file was modified since last read
            if os.path.getmtime(file_name) != kw_last_modif:
                logger.info("Hashtags file was modified")
                kw_last_modif = os.path.getmtime(file_name)
                keywords = ut.get_hashtags(file_name)
        else:
            logger.debug("list is empty")
            keywords = ut.get_hashtags(file_name)
    else:
        logger.error("ERROR: The file containing the hashtags was not found")
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

        logger.info("\n#################\nGetting list of tweets")
        tweet_list, tweet_last_modif = fetch_tweet_data(args.file, tweet_last_modif, tweet_list)

        logger.info("Getting hashtags")
        keywords, kw_last_modif = fetch_hashtag_data(args.key, kw_last_modif, keywords)

        tweet_list = send_tweet(tweet_list)
        ut.reduce_list(tweet_list)

        tweeted = retweet(random.choice(keywords))
        count = 0

        while tweeted == "No tweet" or count > 20:
            sleep(60)
            logger.debug("No tweet found with hashtag used. Trying again in 60 secs")
            tweeted = retweet(random.choice(keywords))
            count += 1

        logger.info("Time now is:" + str(datetime.now()) + "see you in 1 hour...")
        # sleep(10800) # each 2 hours for testing purpose only
        sleep(3600)


if __name__ == '__main__':
    main()
