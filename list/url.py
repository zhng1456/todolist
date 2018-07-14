# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/page/', views.PageView.as_view()),#用于分页
    url(r'^api/msg/$', views.MsgList.as_view()),#获取所有todo和新增todo
    url(r'^api/get-msg-order/$', views.get_msg_order),#用于排序
    url(r'^api/msg/(?P<pk>[0-9]+)', views.MsgDetail.as_view()),#修改和删除todo
    #url(r'^api/edit-msg/(?P<pk>[0-9]+)', views.edit_msg),
]