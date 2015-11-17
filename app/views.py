from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, JsonResponse
from django import forms
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template import RequestContext
from app.models import Tweet, Location, Trend


class TweetList(ListView):
    model = Tweet
    template_name = 'tweet_list.html'
    context_object_name = 'tweets'
    paginate_by = 50

class TweetUpdateForm(forms.Form):  
    title = forms.CharField(required=False)
    info = forms.CharField(required=False, widget=forms.Textarea)
    image = forms.ImageField(required=False)

class TweetDetail(DetailView):
    model = Tweet
    template_name = 'tweet_detail.html'
    context_object_name = 'tweet'


class LocationDetail(DetailView):
    model = Location
    template_name = 'location_detail.html'
    context_object_name = 'location'


class TrendDetail(DetailView):
    model = Trend
    template_name = 'trend_detail.html'
    context_object_name = 'trend'    


def trend_list_view(request):

    locations = Location.objects.all()

    context = {}
    context['locations'] = locations

    return render_to_response('trend_list.html', context, context_instance=RequestContext(request))


class LocationList(ListView):
    model = Location
    template_name = 'map_view.html'
    context_object_name = 'locations'
    
    # def get_queryset(self):
    #     return Location.objects.all().exclude(woeid=1)


def map_view(request):
    return render(request, 'map_view.html')

def no_twitter_feed(request):
    context = {}
    loc = request.GET.get('loc')
    loc_name = ""
    loc_reason = ""
    if (loc == None):
        return redirect('map_view')
    if loc in "china":
        loc_name = "China"
        loc_reason = "because their government doesn't allow them to use social media or Google..."
    elif loc in "greenland":
        loc_name = "Greenland"
        loc_reason = "because there aren't really any people on Greenland... Hahaha just kidding."
    elif loc in "madagascar": 
        loc_name = "Madagascar"
        loc_reason = "because... wait, do they even have internet in Madagascar?!"
    elif loc in "antarctica":
        loc_name = "Antarctica"
        loc_reason = "because... hold on, did actually you think there actually would be tweets from Antarctica?"
    else:
        return redirect('map_view')
    context['loc_name'] = loc_name
    context['loc_reason'] = loc_reason

    return render_to_response('no_twitter_feed.html', context, context_instance=RequestContext(request))


def location_changer(request):
    title = request.GET.get('title') 
    if title == 'Africa':
        title = 'Nigeria'
    elif title == 'Middle East':
        title = 'United Arab'
    elif title == 'South America':
        title = 'Peru'
    elif title == 'Pacific Islands':
        title = 'New Zealand'
    elif title == 'Central America':
        title = 'Guatemala'
    elif title == 'Central Europe':
        title = 'Germany'
    elif title == "Eastern Europe":
        title = 'Russia'
    elif title == "Southeast Asia":
        title = 'Indonesia'
    elif title in ['China', 'Madagascar', 'Greenland', 'Antarctica']:
        title = 'no_twitter_feed/?loc=%s' % title.lower()
        return JsonResponse({'location':[title]}, safe=False)
    api_dict = {}
    location = []
    api_dict['location'] = location
    loc = Location.objects.get(name__icontains=title)
    location.append("location_detail/%s/" % loc.slug)

    return JsonResponse(api_dict, safe=False)


def home(request):
    context = {}
    context['locations'] = Location.objects.all()[:4]

    return render_to_response('home.html', context, context_instance=RequestContext(request))

# def api_test(request):
#     import requests, base64, json, tweepy, pprint, os, sys, urllib
#     from unidecode import unidecode

#     # == OAuth Authentication ==
#     #
#     # This mode of authentication is the new preferred way
#     # of authenticating with Twitter.

#     # The consumer keys can be found on your application's Details
#     # page located at https://dev.twitter.com/apps (under "OAuth settings")

#     # sets up tweepy and custom requests to the server

#     CONSUMER_KEY = 'E2As2Jix81jnskyDheTSYmkXJ'
#     CONSUMER_SECRET = 'jAAi5i4XsrjldtY2MWTNMrNYBR1PGKNWKmzsRUnSWCA5RlzHtZ'

#     #the base twitter url for sending api requests
#     URL = 'https://api.twitter.com/oauth2/token'

#     #the search term to be used
#     credentials = base64.urlsafe_b64encode("%s:%s" % (CONSUMER_KEY, CONSUMER_SECRET))
#     custom_headers = {
#             'Authorization': 'Basic %s' % (credentials),
#             'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
#         }
#     grant_type_data = 'grant_type=client_credentials'
#     response = requests.post(URL, headers=custom_headers, data=grant_type_data)
#     # print response.json()
#     access_token = response.json().get('access_token')
#     search_headers = {'Authorization': 'Bearer %s' % (access_token), }

#     access_token = "3972931574-TBQCKeBRwpWKrcxoecGmIlb6OYUdawcNYtwJTEJ"
#     access_token_secret = "LoUKpnhj6MS0SdlE1bE4TpvIJejT9nk6p1t3gwWkxVYff"

#     auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#     auth.secure = True
#     auth.set_access_token(access_token, access_token_secret)

#     api = tweepy.API(auth)

#     SEARCH_TERM = "Adele"

#     response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q={}%20near%3AUSA&lang=en&count=50'.format(SEARCH_TERM), headers=search_headers)
#     test = json.dumps(response.json())

#     return HttpResponse(test)
