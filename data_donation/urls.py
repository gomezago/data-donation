"""data_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('pages.urls')),
    path('', include('bucket_view.urls')),
    path('admin/', admin.site.urls),
    #path('projects/', include("causes.urls")), # Includes all the URLs in the causes app
    #path('oauth2_test/', include('oauth2_test.urls')),
    path('bucket/', include('bucket.urls')), #TODO: Change to login
    #path("news/", include("about.urls")),
    path('', include('plot_test.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('', include('atm.urls')),
]

# Error Handlers
handler404 = 'pages.views.error_404'
handler500 = 'pages.views.error_500'
handler403 = 'pages.views.error_403'
handler400 = 'pages.views.error_400'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)