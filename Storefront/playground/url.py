from django.urls import path
from . import views

urlpatterns=[
    path('hello/',views.sayhello,name='sayhello'),
    path('dowork/',views.dowork,name='dowork'),
    path('RoutersView/',views.RoutersView,name='RoutersView'),
    path('SwitchesView/',views.SwitchesView,name='SwitchesView'),
    path('FirewallView/',views.FirewallView,name='FirewallView'),
    path('api/routers/', views.RouterList.as_view(), name='router_list_api'),
    path('RouterDoWork/',views.RouterDoWork,name='RouterDoWork'),  
    path('api/devices/', views.device_list, name='device_list'),
]