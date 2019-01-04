from django.conf.urls import url

from . import views
from . import forms

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    url(r'^index$', views.IndexView.as_view(), name='index'),
    url(r'^login$', LoginView.as_view(
      template_name='dev/login.html', authentication_form=forms.LoginForm),
      name='login'),
    url(r'^logout$', LogoutView.as_view(next_page='login'), name='logout'),
    url(r'^message/all$', views.MessageListView.as_view(), name='message list'),
    url(r'^message/new$', views.MessageCreateView.as_view(), name='message new'),
    url(r'^message/(?P<pk>[0-9]+)/$', views.MessageDetailView.as_view(),
      name='message-detail'),
    url(r'^map$', views.MapView.as_view(), name='map'),
    url(r'^locations$', views.LocationAJAXView.as_view(), name='locations'),
    url(r'^waypoints$', views.WaypointAJAXView.as_view(), name='waypoints'),
]