import pandas as pd
import re
from textblob import TextBlob

df = pd.read_csv('Tweets.csv')

def cleanComment(cmnt):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", cmnt).split())

def getSentiment(cmnt):
    analysis = TextBlob(cleanComment(cmnt))
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

def getSentiment(airlines):
    global df
    df = df.loc[df['airline'] == airlines]
    tweets = df['text'].values

    positive = 0
    negative = 0
    nuetral = 0

    for tweet in tweets:
        sentiment = getSentiment(tweet)
        if sentiment == "Positive":
            positive = positive + 1
        elif sentiment == "Neutral":
            nuetral = nuetral + 1
        elif sentiment == "Negative":
            negative = negative + 1
    return positive, negative, nuetral

def getAirlinesSentiment(airlines):
    positive, negative, nuetral = getSentiment(airlines)
    print(positive, negative, nuetral)
    dic = {"Positive": positive, "Neutral": nuetral, "Negative": negative}
    Keymax = max(zip(dic.values(), dic.keys()))[1]
    print(Keymax)
    return Keymax
