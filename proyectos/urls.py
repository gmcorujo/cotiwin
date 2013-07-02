from django.conf.urls import patterns, include, url
from django.contrib import admin


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^cotizacion/', include('cotizacion.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^activate/(?P<user_id>\d+)/(?P<confirm>\w{32})/$','proyectos.solicitudes.activateAccount'),
    url(r'^create/$', 'proyectos.solicitudes.add', name='add'),
    url(r'^waiting/$','proyectos.solicitudes.waiting',name="waiting"),
    url(r'^sucessful/$','proyectos.solicitudes.sucessful',name="sucessful")

)
