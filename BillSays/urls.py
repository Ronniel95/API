from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import SimpleRouter
import rest_framework_swagger
from BillSays import views
from views import schema_view

router = SimpleRouter()
urlpatterns = patterns('',

    url(r'^achievement/(?P<id>[0-9]+)$', views.AchievementAPIView.as_view()),
    url(r'^achievement/$', views.AchievementAPIListView.as_view()),

    url(r'^checkelement/(?P<id>[0-9]+)$', views.CheckelementAPIView.as_view()),
    url(r'^checkelement/$', views.CheckelementAPIListView.as_view()),

    url(r'^checks/(?P<id>[0-9]+)$', views.ChecksAPIView.as_view()),
    url(r'^checks/$', views.ChecksAPIListView.as_view()),
    url(r'^debtelement/(?P<id>[0-9]+)$', views.DebtelementAPIView.as_view()),
    url(r'^debtelement/$', views.DebtelementAPIListView.as_view()),

    url(r'^dictachievement/(?P<id>[0-9]+)$', views.DictachievementAPIView.as_view()),
    url(r'^dictachievement/$', views.DictachievementAPIListView.as_view()),


    url(r'^djangomigrations/(?P<id>[0-9]+)$', views.DjangoMigrationsAPIView.as_view()),
    url(r'^djangomigrations/$', views.DjangoMigrationsAPIListView.as_view()),

    url(r'^friend/(?P<id>[0-9]+)$', views.FriendAPIView.as_view()),
    url(r'^friend/$', views.FriendAPIListView.as_view()),

    url(r'^usercheckelement/(?P<id>[0-9]+)$', views.UsercheckelementAPIView.as_view()),
    url(r'^usercheckelement/$', views.UsercheckelementAPIListView.as_view()),

    url(r'^users/(?P<id>[0-9]+)$', views.UsersAPIView.as_view()),
    url(r'^users/$', views.UsersAPIListView.as_view()),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),



)
