"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^tweet_list/$', views.TweetList.as_view(), name="tweet_list"),
    # url(r'^$', 'app.views.api_test', name="api_test"),

    url(r'^tweet_detail/(?P<pk>\d+)/$', 'app.views.tweet_detail_view', name="tweet_detail"),
    url(r'^map_view/$', views.LocationList.as_view(), name="map_view"),
    # url(r'^map_view/$', 'app.views.map_view', name='map_view'),
    url(r'^location_detail/(?P<slug>.+)/$', views.LocationDetail.as_view(), name='location_detail'),
    url(r'^trend_detail/(?P<slug>.+)/$', 'app.views.trend_detail_view', name='trend_detail'),
    url(r'^trend_list/$', 'app.views.trend_list_view', name='trend_list_view'),
    url(r'^nimda/', include(admin.site.urls)),
    url(r'^no_twitter_feed/$', 'app.views.no_twitter_feed', name='no_twitter_feed'),
    url(r'^$', 'app.views.home', name='home'),
    url(r'^location-changer/$', 'app.views.location_changer', name='location_changer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
