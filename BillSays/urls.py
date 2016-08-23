from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from rest_auth.registration.views import VerifyEmailView
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
from allauth.account.views import confirm_email as allauthemailconfirmation

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Pastebin API')
    return response.Response(generator.get_schema(request=request))


urlpatterns = patterns('',

    url(r'^', include(router.urls)),

    url('^docs/', schema_view),

    #loginning
    url(r'^rest-auth/', include('rest_auth.urls')),

    #registration
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),


    # login via facebook
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

    # admin site
    url(r'^admin/', include(admin.site.urls)),


    url(r'^accounts/', include('allauth.urls')),

    url(r'^rest-auth/registration/account-confirm-email/(?P<key>\w+)/$',
    allauthemailconfirmation, name="account_confirm_email"),

#    url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),
 #   url(r'^accounts/', include('allauth.urls')),

)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT,'show_indexes': False}),
)
