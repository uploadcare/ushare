from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ushare.views.home', name='home'),
    # url(r'^ushare/', include('ushare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^files/', include('ushare.files.urls', namespace='files')),
    url(r'^$', 'ushare.files.views.index', name='index'),
)
