from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import SimpleRouter


from API import settings
from BillSays import views
from views import schema_view, FacebookLogin, VKLogin, UserViewSet

router = SimpleRouter()

from django.views.generic import TemplateView

router.register(r'checks', views.CheckViewSet)
router.register(r'mention', views.MentionViewSet)
router.register(r'usercheckelement',views.BookViewSet)


#router.register(r'search',views.UserListView)

urlpatterns = patterns('',

    url(r'^', include(router.urls)),

    url(r'^users_list/(?P<name>[a-z,A-Z]+)/$', UserViewSet.as_view({'get': 'list'}),name='get_queryset'),

    url(r'^friend/', views.FriendAPIListView.as_view()),
    url(r'^friend_instance/(?P<id>[0-9]+)/$',views.FriendAPIView.as_view()),

    url(r'^login/', views.LoginView.as_view()),

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
