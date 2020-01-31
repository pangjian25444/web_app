# author: pangjian
# time: 2019/12/28 12:25
# software: PyCharm

from django.contrib import admin
from django.urls import path, include

from course_app import views

app_name = 'course_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    path('add/<int:id>/', views.add, name="add"),
    path('save_info/<int:id>/', views.save_info, name="save_info"),
    path('search/<str:name>/', views.search, name="search"),
]
