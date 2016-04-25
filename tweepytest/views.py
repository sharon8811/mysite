from django.shortcuts import render
from django.http import HttpResponse
#import tweepy
import urllib3
# Create your views here.


def index(request):
    auth = tweepy.OAuthHandler("LjaddEJ3rtgp9ockHxODxW3Ee", "so9P4QQSOMSTSM16wbqaWqeuQFDyJrHIjEbwVsIJMQ2hqRWFvE")
    auth.set_access_token("722041452705017856-Ft276rNW20OmzRIxkkhTI0ccHHbI3JC", "tiGRgfxaIEkQEbp7CI8efvXV0naLApTxQIfTn0qfNI7cM")

    api = tweepy.API(auth)
    text = ""
    #public_tweets = api.home_timeline()
    #for tweet in public_tweets:
    #    text += tweet.text + "<br>"
    text += "<br><br><br>"

    user = api.get_user('ynet')
    text += user.screen_name + "<br>"
    text += str(user.followers_count) + "<br>"
    api.create_friendship("ynet")
    #for friend in user.friends():
    #    text += friend.screen_name + "<br>"
    #text += "<br><br><br>"
    #for follower in user.followers():
    #    text += follower.screen_name + "<br>"
    #    api.create_friendship(follower.user_id)
    #for user in tweepy.Cursor(api.followers, screen_name="IronScales").items():
    #    text += user.screen_name + "<br>"
    return HttpResponse(text)