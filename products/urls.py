from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from products import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[a-z\d]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[a-z\d]+)/search/$', views.filteredIndexView, name='search'),
    url(r'^(?P<pk>[a-z\d]+)/add_opinion/$', views.addOpinion, name='opinion'),
    url(r'^(?P<pk>[a-z\d]+)/vote/$', views.vote, name='vote'),
    url(r"^([a-z\d]+)/$", views.post),
)