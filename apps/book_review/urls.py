from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add_book),
    url(r'^process$', views.process),
    url(r'^logout$', views.logout),
    url(r'^books/(?P<id>\d+)$', views.show),
    url(r'^users/(?P<id>\d+)$', views.show_user),
    url(r'^books/(?P<id>\d+)/add_review$', views.add_review),
]