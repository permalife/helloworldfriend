"""
helloworld URL Configuration
"""

from django.conf.urls import include, url
from django.contrib import admin
from hwf import views
from hwf.views import GreetFriendView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^greet/', GreetFriendView.as_view(), name='greet'),
]
