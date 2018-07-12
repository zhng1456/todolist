from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/get-msg', views.get_msg),
    url(r'^api/add-msg', views.add_msg),
    url(r'^api/del-msg/(?P<pk>[0-9]+)', views.del_msg),
    url(r'^api/edit-msg/(?P<pk>[0-9]+)', views.edit_msg),
]