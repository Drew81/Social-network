from django.conf.urls import url
from . import views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm
)

app_name = 'UserPost'

urlpatterns = [
    url(r'^list/$', views.post_list, name='list'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^login/$', login, {'template_name': 'UserPost/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'UserPost/logout.html'}, name='logout'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^UserPost/add-details/$', views.DetailsCreate.as_view(), name='detail-add'),
    url(r'^profile/create/$', views.ProfileCreate.as_view(), name='profile_create'),
    url(r'^UserPost/add/$', views.PostCreate.as_view(), name='post-add'),
    url(r'^UserPost/(?P<pk>[0-9]+)/$', views.PostUpdate.as_view(), name='post-update'),
    url(r'^UserPost/(?P<pk>[0-9]+)/delete/$', views.PostDelete.as_view(), name='post-delete'),

]