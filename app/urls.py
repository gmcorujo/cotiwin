from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.settings import STATIC_ROOT
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    # url(r'^cotizacion/', include('cotizacion.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login/$','app.views.loginUser',name="loginUser"),
    url(r'^logout/$','app.views.logoutUser',name="logoutUser"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^proyectos/', include('proyectos.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT})
)
