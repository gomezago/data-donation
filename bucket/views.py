import json
import requests
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from django.contrib.auth import authenticate, login, logout
from .models import OAuth2Token

OAUTH2_INTROSPECT_URL='https://dwd.tudelft.nl/oauth2/introspect'
OAUTH2_TOKEN_URL='https://dwd.tudelft.nl/oauth2/token'
OAUTH2_REVOKE_URL='https://dwd.tudelft.nl/oauth2/revoke'
OAUTH2_AUTH_URL='https://dwd.tudelft.nl/oauth2/auth'
OAUTH2_PROFILE_URL='https://dwd.tudelft.nl/userinfo'
OAUTH2_REDIRECT_URL='http://localhost:8000/bucket/auth'

THING_URL = "https://dwd.tudelft.nl/bucket/api/things"

oauth = OAuth()
#Register remote application on OAuth registry
oauth.register(
    name='bucket',

    access_token_url=OAUTH2_TOKEN_URL,
    access_token_params=None,

    authorize_url=OAUTH2_AUTH_URL,
    authorize_params=None,

    userinfo_endpoint=OAUTH2_PROFILE_URL,

    client_kwargs={
        'scope':'openid profile email offline dcd:things',
    },
    kwargs={
        'token_endpoint_auth_methods_supported': None,
        'grant_types_supported': ["refresh_token", "authorization_code"],
        'response_types_supported': ["id_token", "token", "code"],
        'introspection_endpoint' : OAUTH2_INTROSPECT_URL,
        'revocation_endpoint' : OAUTH2_REVOKE_URL,
        'authorization_endpoint' : OAUTH2_AUTH_URL,
    }
)

def home(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'bucket.html', context={'user': user})

def bucket_login(request):
    bucket = oauth.create_client('bucket')
    redirect_uri = OAUTH2_REDIRECT_URL
    return bucket.authorize_redirect(request, redirect_uri)

def auth(request):
    token = oauth.bucket.authorize_access_token(request)
    resp = oauth.bucket.get(OAUTH2_PROFILE_URL, token=token)
    resp.raise_for_status()
    profile = resp.json()
    request.session['user'] = profile

    bucket_user = authenticate(request, user=profile) #Returns QuerySet
    bucket_user = list(bucket_user).pop()

    login(request, bucket_user, backend="bucket.auth.BucketAuthenticationBackend")
    return redirect('/bucket/')

def create_thing(request, token):
    hed = {'Authorization': 'bearer ' + token['access_token']}

    my_thing = {
        "name": "Random Thingy",
        "description": "Test thing.",
        "type": "Type can't be empty",
        "pem": None
                }

    response = requests.post(THING_URL, json=my_thing, headers=hed)
    return response

def list_thing(request, token):
    hed = {'Authorization': 'bearer ' + token['access_token']}

    response = requests.get(THING_URL, headers=hed)
    return response

def bucket_logout(request):
    logout(request)
    request.session.pop('user', None)
    return redirect('/bucket/')
