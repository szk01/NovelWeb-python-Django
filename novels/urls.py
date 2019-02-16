from django.contrib import admin
from django.urls import path
from novels import views

urlpatterns = [
    path('cate_<int:category_pk>/',views.novel_type,name='novels_with_type'),
    path('contents/<int:novel_pk>',views.charpter_contents,name='charpter_contents'),
    path('read/<int:charpter_pk>/',views.charpter_detail,name='charpter_detail'),
    path('search/',views.search,name='search')#以get请求方法来传入参数，所以不用写参数显示在前端。透明安全
]
