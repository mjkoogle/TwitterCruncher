import twitter
import twitter.stream
import twitter.oauth
import base64
import sqlite3

from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

#
# The OAuth consumer key to use for the twitter API
#
def CONSUMER_KEY():
    return '4BMyLIvZhkHqz9KJcrneRn2AD'

#
# The OAuth consumer secret to use for the twitter API
#
def CONSUMER_SECRET():
    return 'Kzf86123iHyzl2sZGH1DT5BfK4abDRrv16LRR4ZF6w4hxbsOFY'

#
# The OAuth token to use for the twitter API
#
def OAUTH_TOKEN():
    return '793875845031071745-1OQuvlqatDLXYYHN2k5Kgb54l3BeoHG'

#
# The OAuth token secret to use for the twitter API
#
def OAUTH_TOKEN_SECRET():
    return 'gmLH8ikUH3Ajp7RgEBBrShN7FQFTXkSLIQPweWUlT0BDs'

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


# Create a database connection to the SQLite database
#    specified by db_file
# param db_file: database file
# return: Connection object or None
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        #conn.text_factory = str
        return conn
    except sqlite3.Error as e:
        print(e)

    return None

#
#   Create a new project into the projects table
#    params: conn, text, sentiment
def insert_entry(conn, text, sentiment):
    sql = ''' INSERT INTO tweets(text,sent)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (unicode(text, 'utf-8'), sentiment))

#
# Connect to the twitter stream api, filter returned tweets to those containing "cocacola"
# or "coca cola", and then process each tweet and output it to stdout.
#
def main():
    conn = create_connection("/mnt/x/UMBC/Code/TwitterCruncher/DB")
#    conn = create_connection("X:\\UMBC\Code\TwitterCruncher\DB")
    with conn:
        stream = stream_connect()

        iterator = stream.statuses.filter(track="cocacola,coca cola", language='en')

        for status in iterator:
            text = status["text"].encode('utf-8')
            vs = vaderSentiment(text)['compound']
            insert_entry(conn, text, vs)
            print "Text: " + text
            print "Sentiment: %f" % (vs)
            conn.commit()

if __name__ == '__main__':
    main()