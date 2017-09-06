import tweepy
from time import sleep
from keys import *
import argparse
import random




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


def retweet(hashtag):

    done = 1

    # For loop to iterate over tweets with hashtag key words limit to 2
    for tweet in tweepy.Cursor(api.search,
                               q=hashtag,
                               lang='pt').items(2):

        try:
            # Print out usernames of the last 2 people to use the hashtag
            print('Tweet by: @' + tweet.user.screen_name)

            tweet.retweet()
            print('Retweeted the tweet')
            done = 0
            sleep(5)

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break

    if done == 1:
        return "No tweet"


def main():

    parser = argparse.ArgumentParser(description="A simple tweetbot")
    parser.add_argument("-f", "--file", action="store", help= "file", required=True)
    args = parser.parse_args()

    text = get_text(args.file)
    #tweet(text)

    # hashtags
    keywords = ["#funpresp", "#ricardoamorim", "#fundosdeinvestimento", "#multimercado",
                "fundosprevidenciario", "#estrategiacomdividendos", "#planejamentofinanceiro",
                "#magnetis", "#fintech", "#exploritasalfa", "#pimcoincome",
                "#verdescena"]

    tweeted = retweet(random.choice(keywords))
    count = 0

    while tweeted == "No tweet" or count > 100:
        tweeted = retweet(random.choice(keywords))
        count += 1





if __name__ == '__main__':
    main()



