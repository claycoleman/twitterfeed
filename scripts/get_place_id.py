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
for count, location in enumerate(Location.objects.all()):
    if location.place_id != None:
        continue
    print(location.name)
    try: 
        places = api.geo_search(query=location.name, granularity="country")
        pp.pprint(places)
        place_id = places[0].id
        location.place_id = place_id
        location.save()
    except Exception, e:
        print(e)