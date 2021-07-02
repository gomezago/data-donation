import json
import requests
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from django.contrib.auth import authenticate, login, logout
from .models import OAuth2Token

from django.contrib.auth.decorators import login_required


oauth = OAuth()
#Register remote application on OAuth registry
oauth.register(
    name='bucket',

    access_token_url='https://dwd.tudelft.nl/oauth2/token',
    access_token_params=None,

    authorize_url='https://dwd.tudelft.nl/oauth2/auth',
    authorize_params=None,

    userinfo_endpoint='https://dwd.tudelft.nl/userinfo',

    client_kwargs={
        'scope':'openid profile email offline dcd:things',
    },
    kwargs={
        'token_endpoint_auth_methods_supported': None,
        'grant_types_supported': ["refresh_token", "authorization_code"],
        'response_types_supported': ["id_token", "token", "code"],
        'introspection_endpoint' : 'https://dwd.tudelft.nl/oauth2/introspect',
        'revocation_endpoint' : 'https://dwd.tudelft.nl/oauth2/revoke',
        'authorization_endpoint' : 'https://dwd.tudelft.nl/oauth2/auth',
    }
)


def home(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'bucket.html', context={'user': user})

def bucket_login(request):
    bucket = oauth.create_client('bucket')
    redirect_uri = 'http://localhost:8000/bucket/auth'
    return bucket.authorize_redirect(request, redirect_uri)

def auth(request):
    token = oauth.bucket.authorize_access_token(request)
    resp = oauth.bucket.get('https://dwd.tudelft.nl/userinfo', token=token)
    resp.raise_for_status()
    profile = resp.json()
    request.session['user'] = profile

    bucket_user = authenticate(request, user=profile) #Returns QuerySet
    bucket_user = list(bucket_user).pop()

    login(request, bucket_user, backend="bucket.auth.BucketAuthenticationBackend")

    return redirect('/bucket/')

def create_thing(request, token):

    hed = {'Authorization': 'bearer ' + token['access_token']}
    url = 'https://dwd.tudelft.nl:443/bucket/api/things'

    my_thing = {
        "name": "Thing B",
        "description": "Trying something.",
        "type": "Test",
        "pem": None
                }

    response = requests.post(
        url, json=my_thing, headers=hed
    )
    return response

def list_thing(request, token):
    hed = {'Authorization': 'bearer ' + token['access_token']}

    response = requests.get('https://dwd.tudelft.nl/bucket/api/things',
                     headers=hed)
    return response

def bucket_logout(request):
    logout(request)
    request.session.pop('user', None)
    return redirect('/bucket/')
