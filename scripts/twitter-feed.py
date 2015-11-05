#!/usr/bin/env python
#system tools
import os, sys
#api tools
import requests, base64, json, pprint
#handy
from unidecode import unidecode
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from app.models import Tweet

CONSUMER_KEY = 'E2As2Jix81jnskyDheTSYmkXJ'
CONSUMER_SECRET = 'jAAi5i4XsrjldtY2MWTNMrNYBR1PGKNWKmzsRUnSWCA5RlzHtZ'

#the base twitter url for sending api requests
URL = 'https://api.twitter.com/oauth2/token'

#the search term to be used
SEARCH_TERM = 'blue jays'

credentials = base64.urlsafe_b64encode("%s:%s" % (CONSUMER_KEY, CONSUMER_SECRET))

custom_headers = {
        'Authorization': 'Basic %s' % (credentials),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

grant_type_data = 'grant_type=client_credentials'

response = requests.post(URL, headers=custom_headers, data=grant_type_data)

# print response.json()

access_token = response.json().get('access_token')

#custom header that passes in the accces token 
search_headers = {'Authorization': 'Bearer %s' % (access_token), }
response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=%s&count=100' %SEARCH_TERM, headers=search_headers)

pp = pprint.PrettyPrinter(indent=2)

# print response.json().keys()
# pp.pprint(response.json())

# print response.json().get('statuses')[0]['text']
# print '--------'
# pp.pprint(response.json().get('statuses')[0]['user']['screen_name'])
# profile_image_url, screen_name
# pp.pprint(response.json().get('statuses'))

tweet_list = response.json().get('statuses')

for tweet in tweet_list:
    locat = str(unidecode(tweet.get('user').get('location')))
    if locat != "" and locat != None:
        new_tweet, created = Tweet.objects.get_or_create(screen_name=str(unidecode(tweet.get('user').get('screen_name'))))
        try:
            image_response = requests.get(str(unidecode(tweet.get('user').get('profile_image_url')))) 
            temp_image = NamedTemporaryFile(delete=True)
            temp_image.write(image_response.content)
            new_tweet.profile_image.save('%s.jpg' % new_tweet.screen_name, File(temp_image)) 
            print 'yes'
        except Exception, e:
            print e
        new_tweet.created_at = str(unidecode(tweet.get('user').get('created_at')))
        new_tweet.location = locat
        new_tweet.text = str(unidecode(tweet.get('text')))

        new_tweet.save()




