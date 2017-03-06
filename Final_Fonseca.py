import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim()

from textblob import TextBlob

#declare variables
ckey = "oNO6zXpEoelUV90kmxSfILbcX"
csecret = "xffXAKq9o9bh445F6ZUGP0t8QfGWeXqS4lsJy2KIzTJcSSjzuT"
atoken = "2876135420-YHx1s2QQFFXs1MlDZESgN0TEeXHqqCQqIfomb4U"
asecret = "Ui9icV64RF7tnpOqyf1XBGFy3cSED4VgEQpZGWqlpWjpY"

OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret, 'access_token_key':atoken, 'access_token_secret':asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)

#Here we create a CSV and the tables that will go in.
saveFile = open('Tweets.csv', 'a')
headers = 'Time; User; Text; Sentiment; Question; Place; Latitude; Longitude;'
saveFile.write(headers + '\n')

#Lets grab the tweets
for tweet in tweepy.Cursor(api.search, q ='#Legion').items(): #Here is where we put our keyword with what we want to search for I put Legion cuz it's currently my favorite show
    '''
    Parameters (*required):
    q*: word, hashtag of interest [#hashtag]
    geocode: returns tweets by users located within a given radius of the given latitude/longitude [37.781157,-122.398720,1km]
    lang: language [es]
    result_type: [mixed, popular or recent]
    count: [15-100]
    until: YYYY-MM-DD, 7-day limit [2017-3-5]
    since_id: returns results with an ID greater than (that is, more recent than) the specified ID [12345]
    '''

    if tweet.coordinates:
        print "==========="
        #date & time
        moment = tweet.created_at
        print 'Date & Time: ', moment
        #text
        string = tweet.text.replace('|', ' ')
        string = tweet.text.replace('\n', ' ')
        print 'Text: ', string.encode('utf8')
        #user
        user = tweet.author.name.encode('utf8')
        print 'User: ', user
        #sentiment
        text = TextBlob(string)
        if text.sentiment.polarity < 0:
            sentiment = "negative"
        elif text.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"
        print 'Sentiment: ', sentiment
        #question
        if '?' in string:
            question = 'Yes'
        else:
            question = 'No'
        print 'Question: ', question
        #location    
        place = geolocator.reverse(str(tweet.coordinates))
        print 'Place: ', place
        latitude = tweet.coordinates[0]
        longitude = tweet.coordinates[1]
        print 'Coords:', tweet.coordinates
        print "==========="

        #save tweets
        saveThis = str(moment) + '; ' + str(string.encode('ascii', 'ignore')) + '; ' + user + '; ' + sentiment + '; ' + question + '; ' + place + '; ' + str(latitude) + '; ' + str(longitude) + '; '
        saveFile.write(saveThis + '\n')

    if tweet.place:
        print "==========="
        #date & time
        moment = tweet.created_at
        print 'Date & Time: ', moment
        #text
        string = tweet.text.replace('|', ' ')
        string = tweet.text.replace('\n', ' ')
        print 'Text: ', string.encode('utf8')
        #user
        user = tweet.author.name.encode('utf8')
        print 'User: ', user
        #sentiment
        text = TextBlob(string)
        if text.sentiment.polarity < 0:
            sentiment = "negative"
        elif text.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"
        print 'Sentiment: ', sentiment
        #question
        if '?' in string:
            question = 'Yes'
        else:
            question = 'No'
        print 'Question: ', question
        #location
        place = tweet.place.full_name
        print 'Place:', place
        location = geolocator.geocode(place)
        latitude = location.latitude
        longitude = location.longitude
        print 'Coords: ', location.latitude, location.longitude
        print "==========="

        #save tweets
        saveThis = str(moment) + '; ' + str(string.encode('ascii', 'ignore')) + '; ' + user + '; ' + sentiment + '; ' + question + '; ' + place + '; ' + str(latitude) + '; ' + str(longitude) + '; '
        saveFile.write(saveThis + '\n')

    else:
        print "==========="
        #date & time
        moment = tweet.created_at
        print 'Date & Time: ', moment
        #text
        string = tweet.text.replace('|', ' ')
        string = tweet.text.replace('\n', ' ')
        print 'Text: ', string.encode('utf8')
        #user
        user = tweet.author.name.encode('utf8')
        print 'User: ', user
        #sentiment
        text = TextBlob(string)
        if text.sentiment.polarity < 0:
            sentiment = "negative"
        elif text.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"
        print 'Sentiment: ', sentiment
        #question
        if '?' in string:
            question = 'Yes'
        else:
            question = 'No'
        print 'Question: ', question
        #location
        place = ''
        latitude = ''
        longitude = ''
        print 'Place: ', place
        print 'Coords: ', latitude, longitude
        print "==========="

        #save tweets
        saveThis = str(moment) + '; ' + str(string.encode('ascii', 'ignore')) + '; ' + user + '; ' + sentiment + '; ' + question + '; ' + place + '; ' + str(latitude) + '; ' + str(longitude) + '; '
        saveFile.write(saveThis + '\n')

#close file
saveFile.close()


#The Carto Import Part

from cartodb import CartoAPIKey, CartoException, FileImport
from carto import FileImport
API_KEY ='Here you write your API'
cartodb_domain = 'Here you write your domain'
cl = CartoDBAPIKey(API_KEY, cartodb_domain)

# Import csv file, set privacy as 'link' 
fi = FileImport("Tweets.csv", cl, create_vis='true', privacy='link')
fi.run()