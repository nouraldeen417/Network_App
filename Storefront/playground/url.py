from django.urls import path
from . import views

urlpatterns=[
    path('hello/',views.sayhello,name='sayhello'),
    path('dowork/',views.dowork,name='dowork')   
]