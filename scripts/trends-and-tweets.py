#! /usr/bin/env python
from __future__ import absolute_import, print_function
import requests, base64, json, tweepy, pprint, os, sys, urllib, time
from unidecode import unidecode

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from app.models import Location, Trend, Tweet
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from project.local import CONSUMER_KEY, CONSUMER_SECRET

import django
django.setup()


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

# print('\n')
# print(api.me().name)

pp = pprint.PrettyPrinter(indent=2)

# country codes! World 1. USA 23424977. Mexico 23424900. Canada 23424775.
# Japan 23424856. Brazil 23424768. UK 23424975. China 23424781. Russia 23424936.
# Southeast Asia 23424846. Africa 23424908. France 23424819. Spain 23424950. 
# Australia 23424748. Guatemala 23424834. UAE 23424738. NZ 23424916.
# Portugal 23424925. Germany 23424829. Peru 23424919. Korea 23424868
locations = Location.objects.all()
while True:
    # print('\n')
    print('\nStart')
    for count, new_location in enumerate(locations):
        successful = False
        while not successful:
            try:
                place = api.trends_place(id=new_location.woeid)[0]
                # print("\n-------")
                # print("place %d: %s" % (count,new_location.name))
                successful = True
            except Exception, e:
                print(e)
                time.sleep(15*60)



    # if True:

    #     place = api.trends_place(id=23424975)[0]
    #     location_info = place.get('locations')[0]

    #     new_location, created = Location.objects.get_or_create(name=str(unidecode(location_info.get('name'))))
    #     new_location.woeid = location_info.get('woeid')
    #     new_location.saveSlug
       # pp.pprint(location_info)

        trends = place.get('trends')
        # pp.pprint(trends)
        for trend in trends:
            # print(str(unidecode(trend.get('name'))))
            new_trend, created = Trend.objects.get_or_create(name=str(unidecode(trend.get('name'))))
            new_trend.url = str(unidecode(trend.get('url'))) 
            new_trend.query = str(unidecode(trend.get('query')))
            
            SEARCH_TERM = new_trend.name  # + ('+place:{}'.format(new_location.place_id))
            SEARCH_TERM = urllib.quote_plus(SEARCH_TERM)

            # pp.pprint(SEARCH_TERM)

            response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q={}&with_twitter_user_id=true&count=50'.format(SEARCH_TERM), headers=search_headers)
            for tweet in response.json().get('statuses'):
                new_tweet, created = Tweet.objects.get_or_create(tweet_id=tweet.get('id'))
                if created:
                    
                    new_tweet.screen_name = str(unidecode(tweet.get('user').get('screen_name')))
                    new_tweet.created_at = str(unidecode(tweet.get('user').get('created_at')))
                    try:
                        image_response = requests.get(str(unidecode(tweet.get('user').get('profile_image_url')))) 
                        temp_image = NamedTemporaryFile(delete=True)
                        temp_image.write(image_response.content)
                        new_tweet.profile_image.save('%s.jpg' % new_tweet.screen_name, File(temp_image)) 
                    except Exception, e:
                        print(e)
                    if tweet.get('user').get('location'):
                        new_tweet.location = str(unidecode(tweet.get('user').get('location')))
                    else:
                        new_tweet.location = "No tweet location"
                    new_tweet.text = str(unidecode(tweet.get('text')))
                    new_tweet.trend = new_trend
                    new_tweet.save()
            for counter, tweet in enumerate(new_trend.tweet_set.all().order_by('-pk')):
                # print(tweet.tweet_id + ": " + str(counter))
                if (counter >= 50):
                    tweet.delete()
            new_trend.location.add(new_location)
            new_trend.saveSlug()
            new_trend.save()
        # print("------")
        # print(new_location.name)
        for counter, trend in enumerate(new_location.trend_set.all().order_by('-pk')):
            # print(trend.name + ": " + str(counter))
            if (counter >= 10):
                new_location.trend_set.remove(trend)
                if len(trend.location.all()) is 0:
                    print("deleted %s" % trend.name)
                    trend.delete()
        new_location.saveSlug
        new_location.save()






    # If the application settings are set for "Read and Write" then
    # this line should tweet out the message to your account's
    # timeline. The "Read and Write" setting is on https://dev.twitter.com/apps

    # api.update_status(status='Updating using OAuth authentication via Tweepy!')
    # mom = api.get_user(screen_name='adcoleman')
    # print(mom.status.text)

    # for tweet in tweepy.Cursor(api.user_timeline, screen_name="adcoleman").items(10):
    #     print(tweet.text)

    # for trend in place[0].get('trends'):
    #     # pp.pprint(str(unidecode(trend.get('query'))))
    #     pp.pprint(trend)
    #     print("-------\n")
