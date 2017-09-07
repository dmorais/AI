import os
import re


def f_exists(file_name):

    if os.path.isfile(file_name):
        return True
    else:
        return False


def get_hashtags(file_name):

    regex = re.compile("\s+")

    file = open(file_name, 'r')

    hashtag_list = []

    for line in file:

        line = regex.sub("",line.strip())
        hashtag_list.append('#' + line )

    return hashtag_list


def get_tweet(file_name):


    file = open(file_name, 'r')
    tweet_list = []

    for line in file:
        tweet_list.append( line.strip() )

    return tweet_list



