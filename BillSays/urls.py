from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter
import rest_framework_swagger
from rest_framework_jwt.views import obtain_jwt_token

from API import settings
from BillSays import views
from views import schema_view, FacebookLogin

router = SimpleRouter()
from rest_framework import renderers, response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Pastebin API')
    return response.Response(generator.get_schema(request=request))


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

    url('^$', schema_view),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

    url(r'^api-token-auth/', obtain_jwt_token),




    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),

)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT,'show_indexes': False}),
)
