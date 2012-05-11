from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^twitter/$', 'hellodjango.views.twitter.home', name='home'),
    url(r'^twitter/auth/$', 'hellodjango.views.twitter.auth', name='auth'),
    url(r'^twitter/cb/$', 'hellodjango.views.twitter.cb', name='cb'),
    url(r'^twitter/friends/$', 'hellodjango.views.twitter.friends', name='friends'),


    url(r'^facebook/$', 'hellodjango.views.facebook.home', name='home'),
    url(r'^facebook/auth/$', 'hellodjango.views.facebook.auth', name='auth'),
    url(r'^facebook/cb/$', 'hellodjango.views.facebook.cb', name='cb'),
    url(r'^facebook/friends/$', 'hellodjango.views.facebook.friends', name='friends'),
    # url(r'^hellodjango/', include('hellodjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
