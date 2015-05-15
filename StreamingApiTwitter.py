import sys
import tweepy
from accessKeys import consumer_key, consumer_secret, access_key, access_secret # These keys are on your application's Details
                                                                                # page at https://dev.twitter.com/apps

                                                                                # Lots of good info about the API: 
                                                                                # https://dev.twitter.com/overview/api/tweets

outFile = '/home/josh/google_drive/fetched_tweets.txt'                          # file to which fetched tweets are saved, and it
                                                                                # does not need to already exist

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

class CustomStreamListener(tweepy.StreamListener):
    '''
    This is the listener, resposible for receiving data
    '''
    def on_status(self, tweet):
        with open(outFile,'a') as tf:
            if tweet.coordinates == None:                                       # throw out any tweet without geotag
                pass
            else:                                                               # get relevant info and encode in utf-8
                tweet_coordinates = \
                  (str(tweet.coordinates['coordinates'])).encode('utf-8')
                text = (((tweet.text).replace("\"","'")
                     ).replace("\n", ", ")).encode('utf-8')                     # replace newline characters with commas in tweet
                                                                                # and replace double quotes with singles so 
                                                                                # we only have exterior doubles
                hashtags = (str(tweet.entities['hashtags'])).encode('utf-8')
                time = (str(tweet.created_at)).encode('utf-8')
                tweet_lang = (tweet.lang).encode('utf-8')
                user_lang = (tweet.user.lang).encode('utf-8')
                tweet_id = (tweet.id_str).encode('utf-8')
                user_id = (tweet.user.id_str).encode('utf-8')

                tf.write(tweet_coordinates +"\t"+
                          '"'+ text +'"' +"\t"+
                          hashtags +"\t"+
                          time +"\t"+
                          tweet_lang +"\t"+
                          user_lang +"\t"+
                          tweet_id +"\t"+
                          user_id +"\n")
        return True

    def on_error(self, status_code):
        with open(outFile,'a') as tf:
            tf.write(sys.stderr, 'Encountered error with status code:', 
                     status_code)
        return True                                                             # Don't kill the stream on an error

    def on_timeout(self):
        with open(outFile,'a') as tf:
            tf.write(sys.stderr, 'Timeout...')
        return True                                                             # Don't kill the stream on timeout


sapi = tweepy.streaming.Stream(auth, CustomStreamListener())

# to get all geotagged tweets, use [-180,-90,180,90]
sapi.filter(locations=[22.1357201, # Western longitude
                       44.386383,  # Southern latitude
                       40.227172,  # Eastern longitude
                       52.379475]) # Northern latitude
