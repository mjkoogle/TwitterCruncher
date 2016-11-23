import twitter
import twitter.stream
import twitter.oauth
import base64
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

#
# The OAuth consumer key to use for the twitter API
#
def CONSUMER_KEY():
    return ''

#
# The OAuth consumer secret to use for the twitter API
#
def CONSUMER_SECRET():
    return ''

#
# The OAuth token to use for the twitter API
#
def OAUTH_TOKEN():
    return ''

#
# The OAuth token secret to use for the twitter API
#
def OAUTH_TOKEN_SECRET():
    return ''

#
# Get the OAuth object needed to authenticate to twitter
#
def get_auth():
    return twitter.oauth.OAuth(OAUTH_TOKEN(), OAUTH_TOKEN_SECRET(), CONSUMER_KEY(), CONSUMER_SECRET())

#
# Get a connection to the twitter search API
#
def twitter_connect():
    return twitter.Twitter(auth=get_auth())

#
# Get a connection to the twitter stream API
#
def stream_connect():
    return twitter.stream.TwitterStream(auth=get_auth())

#
# Given a set of tweets, base64 encode and log each of the tweets in a file called tweets.txt
#
def save_tweets(datas):
    file = open('tweets.txt','w')
    for data in datas:
        file.write(base64.b64encode(data['text'].encode('utf-8')) + '\n')
    file.close()

#
# Given a tweet, compute sentiment and output text and sentiment
#
def process_tweet(tweet):
    text = tweet['text'].encode('utf-8')
    vs = vaderSentiment(text)['compound']

    print "Text: " + text
    print "Sentiment: %f" % (vs)

#
# Connect to the twitter stream api, filter returned tweets to those containing "cocacola"
# or "coca cola", and then process each tweet and output it to stdout.
#
def main():
    stream = stream_connect()
    iterator = stream.statuses.filter(track="cocacola,coca cola", language='en')

    for status in iterator:
        process_tweet(status)

main()