# -*- coding:utf8 -*-
# @TIME     :2019/12/17 20:45
# @Author   : 洪松
# @File     : urls.py

from django.urls import path
from . import views

'''
教程项目只有一个应用，polls 。在一个真实的 Django 项目中，可能会有五个，十个，二十个，甚至更多应用。
Django 如何分辨重名的 URL 呢？举个例子，polls 应用有 detail 视图，可能另一个博客应用也有同名的视图。
Django 如何知道 {% url %} 标签到底对应哪一个应用的 URL 呢？

答案是：在根 URLconf 中添加命名空间。在 polls/urls.py 文件中稍作修改，加上 app_name 设置命名空间：
'''

# 为 URL名称添加命名空间
app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
