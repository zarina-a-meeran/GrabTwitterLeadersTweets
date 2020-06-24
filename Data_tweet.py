from tweepy import API
from tweepy import Cursor

from tweepy.streaming import StreamListener
#class from the module that allows you to listen to the tweets 
from tweepy import OAuthHandler
#allows you to authenticate 
from tweepy import Stream
 
import twitter_credentials
#needs to be in the same folder 

import numpy as np
import pandas as pd




class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client
        #to interface with the api and get the data from it 

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth 
# # # # TWITTER STREAMER # # # #
class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        # This handles Twitter authetification and the connection to Twitter Streaming API

        stream.filter(track=hash_tag_list)
        # This line filter Twitter Streams to capture data by the keywords:

# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    #overriding the stream class 

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
    #takes data and then prints them out 
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
        #take in the tweets data 

    

    def on_error(self, status):
        if status == 500:
            return False
        #adding rate limiting to the code 
        print(status)
        #print the data 

class TweetAnalyser():
#to analyse and categorise the tweets 
    
    def tweets_to_data_frame(self, tweets):
    #take tweets from below to convert to a data frame
        pd.set_option('display.max_colwidth', -1)
        df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['Tweets'])
       
        #pass in the list of tweets 

      #  df['id'] = np.array([tweet.id for tweet in tweets])
        #give me the id of every tweet from the tweets passed through this function and store in an array
        
        return df
 
if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyser = TweetAnalyser()
    #create a tweet analyser object
    api = twitter_client.get_twitter_client_api()

    #List = ["@cbAbdullahGul"]
    #print(List)

    tweets1 = api.user_timeline(screen_name="@narendramodi", count=3, tweet_mode='extended')
    tweets2 = api.user_timeline(screen_name="@BorisJohnson", count=3, tweet_mode='extended')
    tweets3 = api.user_timeline(screen_name="@realDonaldTrump", count=3, tweet_mode='extended')
    tweets4 = api.user_timeline(screen_name="@justinTrudeau", count=3, tweet_mode='extended')
    tweets5 = api.user_timeline(screen_name="@HHShkMohd", count=3, tweet_mode='extended')

    print '\033[1m' + ("Narendra Modi - India")
    print '\033[0m'
    df1 = tweet_analyser.tweets_to_data_frame(tweets1)
    print(df1.head(3))

    print("")
    print '\033[1m' + ("Boris Johnson - UK")
    print '\033[0m'
    df2 = tweet_analyser.tweets_to_data_frame(tweets2)
    print(df2.head(3))

    print("")
    print '\033[1m' + ("Donald Trump - USA")
    print '\033[0m'
    df3 = tweet_analyser.tweets_to_data_frame(tweets3)
    print(df3.head(3))

    print("")
    print '\033[1m' + ("justin Trudeau - Canada")
    print '\033[0m'
    df4 = tweet_analyser.tweets_to_data_frame(tweets4)
    print(df4.head(3))

    print("")
    print '\033[1m' + ("Sheikh Mohammed bin Rashid Al Maktoum - UAE")
    print '\033[0m'

    df5 = tweet_analyser.tweets_to_data_frame(tweets5)
    print(df5.head(3))

    #print(dir(tweets1[0]))
    #this will show you all the headings you can get from a tweet
   # print(tweets1[0].text)

#    print(df.head(10))

   # tweets2 = api.user_timeline(screen_name="@lopezobrador_", count=20)

   # print("lopezobrador_ - Mexico")
   # df2 = tweet_analyser.tweets_to_data_frame(tweets2)

    #print(dir(tweets[0]))
    #this will show you all the headings you can get from a tweet
   # print(tweets4[0].text)

  #  print(df2.head(10))

    #@KremlinRussia_E russia , philliapenes @RRD_Davao, Borisjohnson, therealtrump