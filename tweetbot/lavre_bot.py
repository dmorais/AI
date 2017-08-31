import tweepy
from time import sleep
from keys import *
import argparse




# Access and authorize our Twitter credentials from keys.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_text(file_name):

    my_file = open(file_name, 'r')
    lines = my_file.readlines()

    return lines


def tweet(text):

    for line in text:
        try:
            if line != '\n':
                api.update_status(line)
                sleep(60)
            else:
                pass
        except tweepy.TweepError as e:
            if 'Status is a duplicate' in e.reason:
                pass
            else:
                print e.reason
                sleep(5)



def main():

    parser = argparse.ArgumentParser(description="A simple tweetbot")
    parser.add_argument("-f", "--file", action="store", help= "file", required=True)
    args = parser.parse_args()

    text = get_text(args.file)
    tweet(text)



if __name__ == '__main__':
    main()



