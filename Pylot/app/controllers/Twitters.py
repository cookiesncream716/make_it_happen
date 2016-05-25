from system.core.controller import *
import tweepy
from instagram.client import InstagramAPI

class Twitters(Controller):
    def __init__(self, action):
        super(Twitters, self).__init__(action)
        self.load_model("Twitter")
      
    def index(self, id):

        ckey = "[INSERT CONSUMER KEY]"
        csecret = "[INSERT CONSUMER SECRET]"
        atoken = "[INSERT ACCESS TOKEN KEY]"
        asecret = "[INSERT ACCESS TOKEN SECRET]"

        OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret,
        'access_token_key':atoken, 'access_token_secret':asecret}
        auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
        api = tweepy.API(auth)
        query = '#python'


        

        # x = "travel"
        # tweet = api.search(x)
        # print tweet
        # tweet_length = len(tweet)
        # print 'LENGTH RIGHT ABOVE THIS'
     

        # tweet.entities["media"]["media_url"]
        # for media in tweet.entities.get("media",[{}]):
        # #checks if there is any media-entity
        #     if media.get("type",None) == "photo":
        # # checks if the entity is of the type "photo"
        #         image_content=requests.get(media["media_url"])
        #         print media
        # # save to file etc

        search = self.models['Twitter'].get_activites_name(id)
        tweet = api.search(search, count=50)
        tweet_length = len(tweet)    
        print "works"

        
        return self.load_view('/users/inspire_me.html', tweet=tweet , tweet_length = tweet_length)



       
       
   
