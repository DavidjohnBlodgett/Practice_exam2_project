from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^users/create', views.create),
    url(r'^users/(\d+)/delete', views.delete),
    url(r'^users/(\d+)', views.showOne),
    url(r'^users/update/(\d+)', views.update),
    url(r'^users/delete/(\d+)', views.delete),
    url(r'^users/login', views.login),
    url(r'^dashboard', views.dashboard),
    url(r'^update', views.update),
    url(r'^play', views.play),
    url(r'^logout', views.logout),
    url(r'^users', views.show),
    url(r'^', views.index),
]
