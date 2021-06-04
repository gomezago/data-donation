import json
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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

#@login_required(login_url="/bucket")
#def get_authenticated_user(request):
#    return JsonResponse({"msg" : "Authenticated"})

def bucket_login(request):
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

    # Bucket Authenticate method (from auth.py)
    bucket_user = authenticate(request, user=profile)
    bucket_user = list(bucket_user).pop()
    print(bucket_user)

    #login(request, bucket_user)
    # Do something with the token and profile.. For example: Store in db, mark user as logged in and etc!

    #print(profile)
    return redirect('/bucket/')

def logout(request):
    request.session.pop('user', None)
    return redirect('/bucket/')