from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, tweet, result, about, signup

urlpatterns = [
    path('', home, name='home'),
    path('tweet/', tweet, name='tweeter_scrape'),
    path('tweet/result/', result, name='result'),
    path('tweet/result_with_no_text/', result, name='result_with_no_text'),
    path('about/', about, name='about'),
    path('signup/', signup, name='signup')
]