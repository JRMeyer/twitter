# Lots of good info about the API at https://dev.twitter.com/overview/api/tweets
import time
import sys
import tweepy
import csv
# Keys are on your application's Details page at https://dev.twitter.com/apps
from accessKeys import consumer_key, consumer_secret, access_key, access_secret
from tweepy.api import API
from tweepy.models import Status
from tweepy.utils import import_simplejson
json = import_simplejson()


class CustomStreamListener(tweepy.StreamListener):
    '''
    This is the listener, resposible for receiving data
    '''
    def __init__(self, api=None):
        self.api = API(retry_count=100, timeout=1000)

    def on_data(self, raw_data):
        """
        Called when raw data is received from connection.
        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """
        print(type(raw_data))
        data = json.loads(raw_data)
        print(type(data))

        if 'in_reply_to_status_id' in data:
            status = Status.parse(self.api, data)
            if self.on_status(status) is False:
                return False
        elif 'delete' in data:
            delete = data['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'event' in data:
            status = Status.parse(self.api, data)
            if self.on_event(status) is False:
                return False
        elif 'direct_message' in data:
            status = Status.parse(self.api, data)
            if self.on_direct_message(status) is False:
                return False
        elif 'friends' in data:
            if self.on_friends(data['friends']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(data['limit']['track']) is False:
                return False
        elif 'disconnect' in data:
            if self.on_disconnect(data['disconnect']) is False:
                return False
        elif 'warning' in data:
            if self.on_warning(data['warning']) is False:
                return False
        else:
            print("Unknown message type: " + str(raw_data))

    def on_status(self, tweet):
        # throw out any tweet without geotags
        if tweet.coordinates == None:
            pass
        else:
            tweet_coordinates = str(tweet.coordinates['coordinates'])
            # replace newline characters with commas in tweet and replace
            # double quotes with singles so we only have exterior doubles
            text = ((tweet.text).replace("\"","'")).replace("\n", ", ")
            hashtags = str(tweet.entities['hashtags'])
            timeStamp = str(tweet.created_at)
            tweetLang = tweet.lang
            userLang = tweet.user.lang
            tweetID = tweet.id_str
            userID = tweet.user.id_str

            fileName = timeStamp.split(' ')[0] +'.txt'
            with open(fileName,'a',encoding='utf-8') as outFile:
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

