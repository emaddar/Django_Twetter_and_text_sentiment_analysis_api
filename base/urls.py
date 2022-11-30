from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import  home, tweet, result, about, your_text, your_text_result, upload_file, upload_file_result, SignupPage
from . import views



urlpatterns = [
    path('', home, name='home'),
    path('tweet/', tweet, name='tweeter_scrape'),
    path('tweet/result/', result, name='result'),
    path('tweet/result_with_no_text/', result, name='result_with_no_text'),
    path('about/', about, name='about'),
    path('your_text/', your_text, name='your_text'),
    path('your_text/your_text_result', your_text_result, name='your_text_result'),
    path('upload_file/', upload_file, name = 'upload_file'),
    path('upload_file/upload_file_result/', upload_file_result, name = 'upload_file_result'),
    path('signup/', SignupPage.as_view(), name='signup'),
    path('signup/get_api/', TemplateView.as_view(template_name="get_api.html"), name='get_api'),
]

