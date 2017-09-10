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
        line = regex.sub("", line.strip())

        if line.startswith('@'):
            hashtag_list.append(line)

        else:
            hashtag_list.append('#' + line)

    return hashtag_list


def get_tweet(file_name):
    file = open(file_name, 'r')
    tweet_list = []

    for line in file:
        tweet_list.append(line.strip())

    return tweet_list


def reduce_list(t_list):

    file = open("text/test_tweet.txt", 'w')

    if len(t_list) > 0:
        for item in t_list:
            file.write(item + "\n")

        file.close

    else:
        print "No more items to tweet"


    return 0