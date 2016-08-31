from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from rest_auth.registration.views import VerifyEmailView
from rest_framework.routers import SimpleRouter
import rest_framework_swagger
from rest_framework_jwt.views import obtain_jwt_token


from API import settings
from BillSays import views
from views import schema_view, FacebookLogin, VKLogin

router = SimpleRouter()
from rest_framework import renderers, response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from allauth.account.views import confirm_email as allauthemailconfirmation
from django.views.generic import TemplateView, RedirectView

#router.register(r'checks', views.CheckViewSet)

urlpatterns = patterns('',

    url(r'^', include(router.urls)),

    url(r'^friend/', views.FriendAPIListView.as_view()),
    url(r'^friend/(?P<pk>[0-9]+)/$',views.FriendAPIView.as_view()),

    #swagger documentation for API
    url('^docs/', schema_view),

    #loginning
    url(r'^rest-auth/', include('rest_auth.urls')),

    #registration
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # login via facebook
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

    # login via facebook
    url(r'^rest-auth/vk/$', VKLogin.as_view(), name='vk_login'),

    # admin site
    url(r'^admin/', include(admin.site.urls)),

    #allauth needed
    url(r'^accounts/', include('allauth.urls')),

    #email verification
    url(r'^email-verification/$',TemplateView.as_view(template_name="email_verification.html"),
        name='email-verification'),

    )

urlpatterns += patterns('',(r'^static/(?P<path>.*)$','django.views.static.serve',
     {'document_root':settings.STATIC_ROOT,'show_indexes': False}))
