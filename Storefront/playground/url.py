from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns=[
    path('hello/',views.sayhello,name='sayhello'),
    path('RoutersView/',views.RoutersView,name='RoutersView'),
    path('SwitchesView/',views.SwitchesView,name='SwitchesView'),
    path('AdvancedConfigView/',views.AdvancedConfigView,name='AdvancedConfig'),
    path('api/routers/', views.RouterList, name='router_list_api'),  
    path('api/devices/', views.devices_list, name='devices_list'),
    path('api/switches/', views.SwitchList, name='switch_list_api'),
    path('api/firewalls/', views.FirewallList, name='firewall_list_api'),
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('approve_users/', views.approve_users, name='approve_users'),
    path('routerconfiguration/', views.routerconfiguration, name='routerconfiguration'),
    path('switchconfiguration/', views.switchconfiguration, name='switchconfiguration'),
    path('sethostname/', views.sethostname, name='sethostname'),
    path('setbanner/', views.setbanner, name='setbanner'), 
    path('setInterfaceIP/', views.setInterfaceIP, name='setInterfaceIP'), 
    path('vlan/', views.vlan, name='vlan'), 
    path('staticrouting/', views.static_routing, name='staticrouting'), 
    path('ospf/', views.ospf, name='ospf'),
    path('gateway/', views.gateway, name='gateway'),
    path('vlan-brief/', views.display_VLAN_Brief, name='vlan-brief'),
    path('ospf-data/', views.OSPF_Data, name='ospf-data'),
    path('add_device/', views.add_device, name='add_device'),
    path('upload-file/', views.upload_file, name='upload-file'),
    path('paste-config/', views.paste_config, name='paste-config'),
    path('backup/', views.backup, name='backup'),

    
]