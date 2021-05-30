import json
from django.urls import reverse
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth


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

def login(request):
    bucket = oauth.create_client('bucket')
    redirect_uri = 'http://localhost:8000/bucket/auth'
    return bucket.authorize_redirect(request, redirect_uri)

def auth(request):
    token = oauth.bucket.authorize_access_token(request)
    #print(token)

    resp = oauth.bucket.get('https://dwd.tudelft.nl/userinfo', token=token)
    resp.raise_for_status()
    profile = resp.json()
    request.session['user'] = profile
    #print(profile)
    return redirect('/bucket/')

def logout(request):
    request.session.pop('user', None)
    return redirect('/bucket/')