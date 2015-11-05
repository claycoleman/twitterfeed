#! /usr/bin/env python
from __future__ import absolute_import, print_function
import requests, base64, json, tweepy, pprint, os, sys, urllib
from unidecode import unidecode

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from app.models import Location, Trend, Tweet
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings

import django
django.setup()
# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")

# sets up tweepy and custom requests to the server

CONSUMER_KEY = 'E2As2Jix81jnskyDheTSYmkXJ'
CONSUMER_SECRET = 'jAAi5i4XsrjldtY2MWTNMrNYBR1PGKNWKmzsRUnSWCA5RlzHtZ'

#the base twitter url for sending api requests
URL = 'https://api.twitter.com/oauth2/token'

#the search term to be used
credentials = base64.urlsafe_b64encode("%s:%s" % (CONSUMER_KEY, CONSUMER_SECRET))
custom_headers = {
        'Authorization': 'Basic %s' % (credentials),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
grant_type_data = 'grant_type=client_credentials'
response = requests.post(URL, headers=custom_headers, data=grant_type_data)
# print response.json()
access_token = response.json().get('access_token')
search_headers = {'Authorization': 'Bearer %s' % (access_token), }

access_token = "3972931574-TBQCKeBRwpWKrcxoecGmIlb6OYUdawcNYtwJTEJ"
access_token_secret = "LoUKpnhj6MS0SdlE1bE4TpvIJejT9nk6p1t3gwWkxVYff"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print('\n')
print(api.me().name)

pp = pprint.PrettyPrinter(indent=2)

# place_id = api.geo_search(query="San Francisco", max_results=1)
# pp.pprint(place_id)
# for tweet in tweepy.Cursor(api.search, q="delicious place:247f43d441defc03").items(10):
    # pp.pprint(tweet)

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps

# api.update_status(status='Updating using OAuth authentication via Tweepy!')
# mom = api.get_user(screen_name='adcoleman')
# print(dir(mom))
# print(mom.status.text)

# for tweet in tweepy.Cursor(api.user_timeline, screen_name="adcoleman").items(10):
#     print(tweet.text)

# country codes! World 1. USA 23424977. Mexico 23424900. Canada 23424775.
# Japan 23424856. Brazil 23424768. UK 23424975. China 23424781. Russia 23424936.
# Southeast Asia 23424846. Africa 23424908. France 23424819. Spain 23424950. 
# Australia 23424748. Guatemala 23424834. UAE 23424738. NZ 23424916.
# Portugal 23424925. Germany 23424829. Peru 23424919. Korea 23424868
locations = Location.objects.all()
for new_location in locations[(len(locations)/2 - 1):]:
    place = api.trends_place(id=new_location.woeid)[0]

# if True:

#     place = api.trends_place(id=23424975)[0]
#     location_info = place.get('locations')[0]

#     new_location, created = Location.objects.get_or_create(name=str(unidecode(location_info.get('name'))))
#     new_location.woeid = location_info.get('woeid')
#     new_location.saveSlug
#    # pp.pprint(location_info)

    trends = place.get('trends')
    # pp.pprint(trends)
    for trend in trends[:1]:
        print(str(unidecode(trend.get('name'))))
        new_trend, created = Trend.objects.get_or_create(name=str(unidecode(trend.get('name'))))
        new_trend.url = str(unidecode(trend.get('url'))) 
        new_trend.query = str(unidecode(trend.get('query')))
        
        SEARCH_TERM = new_trend.name  # + ('+place:{}'.format(new_location.place_id))
        SEARCH_TERM = urllib.quote_plus(SEARCH_TERM)

        pp.pprint(SEARCH_TERM)

        
        # tweets = api.search(q='%23CanYouRespectNiall', near="Worldwide", count=1)
        # pp.pprint(len(tweets))
        response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q={}&with_twitter_user_id=true&count=50'.format(SEARCH_TERM), headers=search_headers)
        # pp.pprint(response.json().get('statuses')[0])
        for tweet in response.json().get('statuses'):
            new_tweet, created = Tweet.objects.get_or_create(tweet_id=tweet.get('id'))
            if created:
                try:
                    image_response = requests.get(str(unidecode(tweet.get('user').get('profile_image_url')))) 
                    temp_image = NamedTemporaryFile(delete=True)
                    temp_image.write(image_response.content)
                    new_tweet.profile_image.save('%s.jpg' % new_tweet.screen_name, File(temp_image)) 
                    print('yes')
                except Exception, e:
                    print(e)
                new_tweet.screen_name = str(unidecode(tweet.get('user').get('screen_name')))
                new_tweet.created_at = str(unidecode(tweet.get('user').get('created_at')))
                if tweet.get('user').get('location'):
                    new_tweet.location = str(unidecode(tweet.get('user').get('location')))
                else:
                    new_tweet.location = "No tweet location"
                new_tweet.text = str(unidecode(tweet.get('text')))
                new_tweet.trend = new_trend
                new_tweet.save()
        for counter, tweet in enumerate(new_trend.tweet_set.all().order_by('-pk')):
            print(tweet.tweet_id + ": " + str(counter))
            if (counter >= 50):
                tweet.delete()
        new_trend.location.add(new_location)
        new_trend.saveSlug()
        new_trend.save()
    print("------")
    for counter, trend in enumerate(new_location.trend_set.all().order_by('-pk')):
        print(trend.name + ": " + str(counter))
        if (counter >= 10):
            trend.delete()
    new_location.saveSlug
    new_location.save()


# SEARCH_TERM = 'BeliebersVoteEMA%20near%3A"Worldwide"'
# pp.pprint(SEARCH_TERM)
# SEARCH_TERM = base64.urlsafe_b64encode(SEARCH_TERM)








# p2 = api.trends_place(id=23424977)

# for trend in place[0].get('trends'):
#     # pp.pprint(str(unidecode(trend.get('query'))))
#     pp.pprint(trend)
#     print("-------\n")
