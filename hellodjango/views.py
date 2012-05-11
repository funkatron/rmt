from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson as json
import pprint
from oauth_hook import OAuthHook
import requests
from cgi import parse_qs
import sys


TWITTER_CONSUMER_KEY = "S8EPnyIi1mlQFeO2cOomNg"
TWITTER_CONSUMER_SECRET = "sUt3kzCoovukVtXrdsvUWqo1M5VCHRzhWeF3dkvOG4"
CALLBACK_URL = "http://127.0.0.1:8000/twitter/cb"

FACEBOOK_APP_ID = "347481978638466"
FACEBOOK_APP_SECRET = "ffd2266e518e493c25da0cf322c29419"


def dump(obj):

    return pprint.PrettyPrinter().pformat(obj)


def home(request):

    twitter_data = None

    if request.session.get('twitter_data'):
        twitter_data = request.session.get('twitter_data')

    return render_to_response('twitter/home.html', {'twitter_data': twitter_data})


def auth(request):

    oauth_hook = OAuthHook(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET, header_auth=True)
    client = requests.session(hooks={'pre_request': oauth_hook})
    response = client.post('https://api.twitter.com/oauth/request_token', {'oauth_callback': 'http://127.0.0.1:8000/twitter/cb'})

    qs = parse_qs(response.content)

    auth_url = "https://api.twitter.com/oauth/authorize?oauth_token=" + qs['oauth_token'][0]

    return redirect(auth_url)


def friends(request):

    if request.session.get('twitter_data'):
        twitter_data = request.session.get('twitter_data')
    else:
        return redirect('/twitter/')

    # get following graph
    oauth_hook = OAuthHook(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET, access_token=twitter_data['oauth_token'], access_token_secret=twitter_data['oauth_token_secret'], header_auth=True)
    client = requests.session(hooks={'pre_request': oauth_hook})
    response = client.get('http://api.twitter.com/1/friends/ids.json?user_id=' + twitter_data['user_id'])

    friends = json.loads(response.content)

    return render_to_response('twitter/friends.html', {'twitter_friends': friends})


def cb(request):

    twitter_data = {}
    oauth_token = request.GET['oauth_token']
    oauth_verifier = request.GET['oauth_verifier']

    oauth_hook = OAuthHook(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET, header_auth=True)
    client = requests.session(hooks={'pre_request': oauth_hook})
    response = client.post('https://api.twitter.com/oauth/access_token', {'oauth_verifier': oauth_verifier, 'oauth_token': oauth_token})

    print >>sys.stderr, dump(response.headers)

    qs = parse_qs(response.content)

    twitter_data['oauth_token'] = qs['oauth_token'][0]
    twitter_data['oauth_token_secret'] = qs['oauth_token_secret'][0]
    twitter_data['screen_name'] = qs['screen_name'][0]
    twitter_data['user_id'] = qs['user_id'][0]

    request.session['twitter_data'] = twitter_data

    return redirect('/twitter/')
