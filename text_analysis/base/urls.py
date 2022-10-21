from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, result

urlpatterns = [
    path('', home, name='tweeter_scrape'),
    path('result/', result, name='result'),
    path('result_with_no_text/', result, name='result_with_no_text')
]