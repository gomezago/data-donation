import json
import environ
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from django.contrib.auth import authenticate, login, logout
from .models import OAuth2Token

env = environ.Env()
environ.Env.read_env()
oauth = OAuth()

def fetch_bucket_token(request):
    token = OAuth2Token.find(user = request.user)
    return token.to_token()

def update_bucket_token(token, refresh_token=None, access_token=None):
    if refresh_token:
        item = OAuth2Token.find(refresh_token=refresh_token)
    elif access_token:
        item = OAuth2Token.find(access_token=access_token)

    # Update Token
    item.access_token = token['access_token']
    item.refresh_token = token.get('refresh_token')
    item.expires_at = token['expires_at']
    item.save()

oauth = OAuth(update_token=update_bucket_token)

#Register remote application on OAuth registry
oauth.register(
    name='bucket',

    access_token_url=env('OAUTH2_TOKEN_URL'),
    access_token_params=None,

    authorize_url=env('OAUTH2_AUTH_URL'),
    authorize_params=None,

    userinfo_endpoint=env('OAUTH2_PROFILE_URL'),

    fetch_token = fetch_bucket_token,

    client_kwargs={
        'scope':env('DATA_DONATION_SCOPE')
    },
    kwargs={
        'token_endpoint_auth_methods_supported': None,
        'grant_types_supported': ["refresh_token", "authorization_code"],
        'response_types_supported': ["id_token", "token", "code"],
        'introspection_endpoint' : env('OAUTH2_INTROSPECT_URL'),
        'revocation_endpoint' : env('OAUTH2_REVOKE_URL'),
        'authorization_endpoint' : env('OAUTH2_AUTH_URL'),
    }
)

def home(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'bucket.html', context={'user': user})

def bucket_login(request):
    bucket = oauth.create_client('bucket')
    redirect_uri = env('OAUTH2_REDIRECT_URL')
    return bucket.authorize_redirect(request, redirect_uri)

def auth(request):
    token = oauth.bucket.authorize_access_token(request)
    request.session['token'] = token

    resp = oauth.bucket.get(env('OAUTH2_PROFILE_URL'), token=token)
    resp.raise_for_status()
    profile = resp.json()
    #request.session['user'] = profile

    bucket_user = authenticate(request, user=profile) #Returns Bucket User
    login(request, bucket_user, backend="bucket.auth.BucketAuthenticationBackend")

    #save_token(request, token)

    return redirect('/hello/')


def save_token(request, token):
    print(request.user)
    if OAuth2Token.objects.filter(user=request.user.user_id).exists():

        OAuth2Token.objects.filter(user=request.user.user_id).update(
            token_type=token['token_type'],
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            expires_at=token['expires_at'],
        )

    else:
        oauth2_token = OAuth2Token(
                token_type=token['token_type'],
                access_token=token['access_token'],
                refresh_token=token['refresh_token'],
                expires_at=token['expires_at'],
                user=request.user,
            )
        oauth2_token.save()

def bucket_logout(request):
    logout(request)
    request.session.pop('user', None)
    return redirect('/')