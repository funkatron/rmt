from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson as json
import pprint
import uuid
import requests
from cgi import parse_qs
import sys

FACEBOOK_APP_ID = "347481978638466"
FACEBOOK_APP_SECRET = "ffd2266e518e493c25da0cf322c29419"
FACEBOOK_APP_REDIRECT = "http://127.0.0.1:8000/facebook/cb"


def dump(obj):

    return pprint.PrettyPrinter().pformat(obj)


def home(request):

    facebook_data = None

    if request.session.get('facebook_data'):
        facebook_data = request.session.get('facebook_data')

    print >>sys.stderr, dump(facebook_data)

    return render_to_response('facebook/home.html', {'facebook_data': facebook_data})


def auth(request):

    fb_uuid = uuid.uuid1().hex
    request.session['facebook_auth_uuid'] = fb_uuid

    auth_url = "https://www.facebook.com/dialog/oauth?client_id=" + FACEBOOK_APP_ID + "&redirect_uri=" + FACEBOOK_APP_REDIRECT + "&state=" + fb_uuid

    return redirect(auth_url)


def friends(request):

    if request.session.get('facebook_data'):
        facebook_data = request.session.get('facebook_data')
    else:
        return redirect('/facebook/')

    # get following graph
    response = requests.get('https://graph.facebook.com/me/friends?access_token=' + facebook_data['oauth_token'])

    friends = json.loads(response.content)['data']

    return render_to_response('facebook/friends.html', {'facebook_friends': friends})


def cb(request):

    facebook_data = {}
    state = request.GET['state']
    code = request.GET['code']

    if state != request.session.get('facebook_auth_uuid'):
        print >>sys.stderr, request.session['facebook_auth_uuid']
        return HttpResponse('bad state key')

    response = requests.get("https://graph.facebook.com/oauth/access_token?client_id=" + FACEBOOK_APP_ID + "&redirect_uri=" + FACEBOOK_APP_REDIRECT + "&client_secret=" + FACEBOOK_APP_SECRET + "&code=" + code)

    print >>sys.stderr, dump(response.headers)

    qs = parse_qs(response.content)

    facebook_data['oauth_token'] = qs['access_token'][0]
    facebook_data['expires'] = qs['expires'][0]

    response = requests.get("https://graph.facebook.com/me?access_token=" + facebook_data['oauth_token'])
    user = json.loads(response.content)

    facebook_data['user'] = user

    request.session['facebook_data'] = facebook_data

    return redirect('/facebook/')
