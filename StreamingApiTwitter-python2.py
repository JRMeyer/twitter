# Lots of good info about the API at https://dev.twitter.com/overview/api/tweets
import sys
import tweepy
import csv
# Keys are on your application's Details page at https://dev.twitter.com/apps
from accessKeys import consumer_key, consumer_secret, access_key, access_secret


class CustomStreamListener(tweepy.StreamListener):
    '''
    This is the listener, resposible for receiving data
    '''
    def __init__(self, api=None):
        self.api = tweepy.API(retry_count=100, timeout=1000)
        
    def on_status(self, tweet):
        # throw out any tweet without geotags
        if tweet.coordinates == None:
            pass
        else:
            tweet_coordinates = \
              (str(tweet.coordinates['coordinates'])).encode('utf-8')

            # replace newline characters with commas in tweet and replace
            # double quotes with singles so we only have exterior doubles
            text = (((tweet.text).replace("\"","'")
                 ).replace("\n", ", ")).encode('utf-8')
            hashtags = (str(tweet.entities['hashtags'])).encode('utf-8')
            timeStamp = (str(tweet.created_at)).encode('utf-8')
            tweetLang = (tweet.lang).encode('utf-8')
            userLang = (tweet.user.lang).encode('utf-8')
            tweetID = (tweet.id_str).encode('utf-8')
            userID = (tweet.user.id_str).encode('utf-8')

            with open(timeStamp.split(' ')[0] +'.txt', 'a') as outFile:
                writer = csv.writer(outFile, delimiter ='\t', quotechar='"')
                writer.writerow([tweet_coordinates, 
                                 text,
                                 hashtags,
                                 timeStamp,
                                 tweetLang,
                                 userLang,
                                 tweetID,
                                 userID])
        return True

    def on_error(self, status_code):
        print('status_code error: ' + str(status_code))
        # Don't kill the stream on an error
        return True
    
    def on_timeout(self):
        print('timeout error!')
        # Don't kill the stream on timeout
        return True


if __name__ == '__main__':
    # [Western-longitude,Southern-latitude,Eastern-longitude,Northern-latitude]
    world = [-180,-90,180,90]
    ukraine = [22.1357201,44.386383,40.227172,52.379475]
    kyrgyzstan = [69.2193603,39.1130136,80.2606201,43.3011962]
    central_asia = [46.25, 29.25, 87.5, 55.5]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
    sapi.filter(locations=central_asia)

