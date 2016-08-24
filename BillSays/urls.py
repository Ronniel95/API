from django.conf.urls import patterns, include, url
from django.contrib import admin
from BillSays import views


urlpatterns = patterns('',

    url(r'^person/(?P<id>[0-9]+)$', views.PersonAPIView.as_view()),
    url(r'^person/$', views.PersonAPIListView.as_view()),

)
