# Declare the libraries needed
import tweepy
import pandas as pd
import sys
import csv
from wordcloud import WordCloud, STOPWORDS
import matplotlib as mpl
import matplotlib.pyplot as plt
import re
from PIL import Image
import pandas_profiling

consumer_key = 'xxx'
consumer_secret = 'xxx'
access_token_key = 'xxx'
access_token_secret = 'xxx'

api = tweepy.Api(consumer_key,
                 consumer_secret,
                 access_token_key,
                 access_token_secret)


# Function to extract tweets
def get_tweets(username):
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_token_key, access_token_secret)

    # Calling api
    api = tweepy.API(auth)
    # set count to however many tweets you want - max count is 3200 and this doesn't have any effect if it is more than 3200
    #        number_of_tweets = 5000

    tfile = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items():
        # username, tweet id, date/time, text
        tfile.append([username, tweet.id_str, tweet.source, tweet.created_at, tweet.retweet_count, tweet.favorite_count,
                      tweet.text.encode("utf-8")])

    # write to a new csv file from the array of tweets
    outfile = username + "_tweets_V1.csv"
    print("writing to " + outfile)
    with open(outfile, 'w+') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['User_Name', 'Tweet_ID', 'Source', 'Created_date', 'Retweet_count', 'Favorite_count', 'Tweet'])
        writer.writerows(tfile)

def main():
    # user name
    get_tweets("@KingJames")

    bg2 = []
    import re
    pattern1 = re.compile(" ' # S % & ' ( ) * + , - . / : ; < = >  @ [ / ] ^ _ { | } ~")
    pattern2 = re.compile("@[A-Za-z0-9]+")
    pattern3 = re.compile("https?://[A-Za-z0-9./]+")

    for item in bg2:
        tweet = re.sub(pattern1, "", item)  # version 1 of the tweet
        tweet = re.sub(pattern2, "", tweet)
        tweet = re.sub(pattern3, "", tweet)
        bg2.append(tweet)

    bg3 = pd.DataFrame(bg2, columns=['tweet'])

    mpl.rcParams['figure.figsize'] = (16.0, 10.0)
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['savefig.dpi'] = 1400
    mpl.rcParams['figure.subplot.bottom'] = .1

    stopwords = set(STOPWORDS)
    text = " ".join(tweet for tweet in bg3.tweet)
    print("There are {} words in the combination of all tweets.".format(len(text)))

    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40,
        random_state=42
    ).generate(str(text))

    print(wordcloud)
    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    fig.savefig("word1.png", dpi=1400)
