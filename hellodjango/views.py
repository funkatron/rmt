from django.http import HttpResponse
import pprint
from oauth_hook import OAuthHook
import requests
from cgi import parse_qs


CONSUMER_KEY = "S8EPnyIi1mlQFeO2cOomNg"
CONSUMER_SECRET = "sUt3kzCoovukVtXrdsvUWqo1M5VCHRzhWeF3dkvOG4"
CALLBACK_URL = "http://127.0.0.1:8000/twitter/cb"


def dump(obj):

    return pprint.PrettyPrinter().pformat(obj)


def home(request):

    oauth_hook = OAuthHook(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, header_auth=True)
    client = requests.session(hooks={'pre_request': oauth_hook})
    response = client.post('https://api.twitter.com/oauth/request_token', {'oauth_callback': 'http://127.0.0.1:8000/twitter/cb'})

    qs = parse_qs(response.content)

    auth_url = "https://api.twitter.com/oauth/authorize?oauth_token=" + qs['oauth_token'][0]

    return HttpResponse(auth_url)


def cb(request):

    oauth_token = request.GET['oauth_token']
    oauth_verifier = request.GET['oauth_verifier']

    oauth_hook = OAuthHook(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, header_auth=True)
    client = requests.session(hooks={'pre_request': oauth_hook})
    response = client.post('https://api.twitter.com/oauth/access_token', {'oauth_verifier': oauth_verifier, 'oauth_token': oauth_token})

    qs = parse_qs(response.content)

    return HttpResponse(dump(qs))
