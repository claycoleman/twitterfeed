#! /usr/bin/env python
import os, sys

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

import django
django.setup()

from app.models import Trend, Tweet, Location

count = 0
for trend in Trend.objects.all():
    for tweet in trend.tweet_set.all():
        count+=1

print count
len_tweet = len(list(Tweet.objects.all()))


print len_tweet

dir_name = os.path.dirname(os.path.abspath(__file__).replace('scripts/how-many-per-trend.py', 'media/profile_images/'))

print dir_name

onlyfiles=[f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f)) and f.lower().endswith('.jpg')]

count_name = {}


for r in onlyfiles:
    temp_name = r.replace('.jpg', '')
    if '-1' in temp_name:
        if temp_name.partition('-1')[0] not in count_name:
            count_name[temp_name.partition('-1')[0]] = 1

for trend in Trend.objects.all():
    if trend.name.replace(' ','_').replace('#', '').replace('\'', '') in count_name:
        count_name[trend.name.replace(' ','_').replace('#', '').replace('\'', '')]

for key in count_name:
    print "%s: %d" % (key, count_name[key])
print len(count_name)