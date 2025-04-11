from django.http import HttpResponse
from .utils import AutomationMethods
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .form import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.cache import cache
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Mark the user as inactive until approved
            user.save()
            return render(request, 'pending_approval.html')  # Inform the user
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def approve_users(request):
    from django.contrib.auth.models import User

    pending_users = User.objects.filter(is_active=False)  # Get inactive users
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(User, id=user_id)

        if action == 'approve':
            user.is_active = True
            user.save()
        elif action == 'approveAsAdmin':
            user.is_active = True
            user.is_staff=True
            user.save()
        elif action == 'reject':
            user.delete()  # Delete user if rejected
        return redirect('approve_users')

    return render(request, 'approve_users.html', {'pending_users': pending_users})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('sayhello')
                else:
                    messages.error(request, "Your account is pending approval by an admin.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Create your views here.
@login_required
def sayhello(request):
    return render(request, 'hello.html')  # User-specific homepage
    #return HttpResponse('Hello')

@login_required
def RoutersView(request):
    return render(request,'router.html')

@login_required
def SwitchesView(request):
    return render(request,'switch.html')

@login_required
def AdvancedConfigView(request):
    return render(request,'advanced_config.html')

@login_required
def routerconfiguration(request):
    return render(request,'router_configuration.html')

@login_required
def switchconfiguration(request):
    return render(request,'switch_configuration.html')


@login_required
def add_device(request):
    
    if request.method=='POST':
        cidr=request.POST.get('ip')
        devicename=request.POST.get('name')
        type=request.POST.get('type')
        username=request.POST.get('ssh-username')
        password=request.POST.get('ssh-pass')
        print(cidr)
        print(devicename)
        print(type)
        print(username)
        print(password)
        result=AutomationMethods.new_device(cidr,devicename,type,username,password)
        return JsonResponse({'response':result})  
    return render(request,'advanced_config.html')
    

@login_required
def upload_file(request):
    if request.method=='POST':
        file=request.FILES.get('file')
        device=request.POST.getlist('device')
        print(file)
        print(device)
        result =AutomationMethods.send_configration_file(device,file)
        return JsonResponse({'response':result})
    return render(request,'advanced_config.html')

@login_required
def paste_config(request):
    if request.method=='POST':
        paste_config=request.POST.get('paste-config')
        device=request.POST.getlist('device')
        print(paste_config)
        print(device)
        result =AutomationMethods.send_commands_string(device,paste_config)
        return JsonResponse({'response':result})
    return render(request,'advanced_config.html')


@login_required
def backup(request):
    if request.method=='POST':
        devices=request.POST.getlist('device')
        print(devices)
        result =AutomationMethods.take_backup(devices)
        return JsonResponse({'response':result})
    return render(request,'advanced_config.html')


@login_required
def gateway(request):
    if request.method=='POST':
        switch=request.POST.get('switch')
        gateway=request.POST.get('gateway')
        print(switch)
        print(gateway)
        result = AutomationMethods.set_switchgateway(switch,gateway)
        if(result == "ok"):# i change here
            messages.success(request,"Switch Gateway has been Done Successfully")
        else :
            messages.error(request,f"Error while Switch Gateway Configuration: {result}")# i change here
        
        return render(request,'result.html',{'page':'switchconfiguration'})

@login_required
def static_routing(request):
    if request.method=="POST":
        router=request.POST.get('router')
        cidr=request.POST.get('cidr')
        next_hop=request.POST.get('next-hop')
        admin_dist=request.POST.get('admin-dist')
        tag=request.POST.get('tag')
        print(router)
        print(cidr)
        print(next_hop)
        print(admin_dist)
        print(tag)
        result=AutomationMethods.Static_routing(router,cidr,next_hop,admin_dist,tag)
        if(result == "ok"):# i change here
            messages.success(request,"Static Routing has been Done Successfully")
        else :
            messages.error(request,f"Error while doing Static Routing Configuration: {result}")# i change here
        
        return render(request,'result.html',{'page':'routerconfiguration'})
        return redirect('/playground/routerconfiguration')


@login_required
def ospf(request):
    if request.method=="POST":
        routers=request.POST.getlist('routers')
        cidr=request.POST.get('cidr')
        ospf_id=request.POST.get('ospf-id')
        area_id=request.POST.get('area-id')
        interfaces=request.POST.getlist('interfaces')
        hello_timer=request.POST.get('hello-timer')
        dead_timer=request.POST.get('dead-timer')
        tag=request.POST.get('tag')
        router_id=request.POST.get('router-id')
        print(routers)
        print(cidr)
        print(ospf_id)
        print(area_id)
        print(interfaces)
        print(hello_timer)
        print(dead_timer)
        print(tag)
        print(router_id)
        result=AutomationMethods.Ospf_routing(
            routers,interfaces,cidr,
            ospf_id,router_id,area_id,
            hello_timer,dead_timer,tag
        )#router_id required --->"1.1.1.1"
        if(result == "ok"):# i change here
            messages.success(request,"OSPF has been Done Successfully")
        else :
            messages.error(request,f"Error while doing OSPF Configuration: {result}")# i change here
        
    return render(request,'result.html',{'page':'routerconfiguration'})
    return redirect('/playground/routerconfiguration')


@login_required
def vlan(request):
    if request.method=="POST":
        vlanid=request.POST.get('vlan-id')
        vlanname=request.POST.get('vlan-name')
        switches=request.POST.getlist('switches')
        interfaces=request.POST.getlist('interfaces')
        vlan_cidr=request.POST.get('vlan-cidr')
        tag=request.POST.get('tag')
        print(switches)
        print(interfaces)
        print(tag)
        print(vlan_cidr)
        print(vlanid)
        print(vlanname)
        
        result=AutomationMethods.Vlans_configs(switches,interfaces,vlan_cidr,vlanid,vlanname,tag)
        if(result == "ok"):# i change here
            messages.success(request,"VLAN has been Done Successfully")
        else :
            messages.error(request,f"Error while doing VLAN Configuration: {result}")# i change here
        
    return render(request,'result.html',{'page':'switchconfiguration'})
    return redirect('/playground/switchconfiguration')


@login_required
def sethostname(request):
    if request.method == "POST":
        router=request.POST.get('router')
        switch=request.POST.get('switch')
        hostname=request.POST.get('hostname')
        print(router)
        print(switch)
        print(hostname)
        result=""
        if(router):
            print("set Router")
            result = AutomationMethods.Set_Hostname(router,hostname)
        elif(switch):
            print("set switch")
            result = AutomationMethods.Set_Hostname(switch,hostname)
        if(result == "ok"):# i change here
            messages.success(request,"Hostname has been set Successfully")
        else :
            messages.error(request,f"Error while setting setting Host name: {result}")# i change here
        
        if(router):    
            return render(request,'result.html',{'page':'routerconfiguration'})
            return redirect('/playground/routerconfiguration');# render(request,'router_configuration.html')
        else :
            return render(request,'result.html',{'page':'switchconfiguration'})
            return redirect('/playground/switchconfiguration');# render(request,'switch_configuration.html')
@login_required
def setbanner(request):
    if request.method == "POST":
        router=request.POST.get('router')
        switch=request.POST.get('switch')
        banner=request.POST.get('banner')
        print("hello banner")
        print(router)
        print(switch)
        print(banner)
        result=""
        if(router):
            print("set Router")
            result = AutomationMethods.Set_Banner(router,banner)
        elif(switch):
            print("set switch")
            result = AutomationMethods.Set_Banner(switch,banner)
        
        if(result == "ok" ):# i change here
            messages.success(request,"Banner has been set Successfully")
        else :
            messages.error(request,f"Error while setting setting Banner name: {result}")
        
        if(router):    
            return render(request,'result.html',{'page':'routerconfiguration'})
            return redirect('/playground/routerconfiguration');# render(request,'router_configuration.html')
        else :
            return render(request,'result.html',{'page':'switchconfiguration'})
            return redirect('/playground/switchconfiguration');# render(request,'switch_configuration.html')

@login_required
def setInterfaceIP(request):
    if request.method == "POST":
        router=request.POST.get('router')
        switch=request.POST.get('switch')
        interfacename=request.POST.get('interfaces')
        ipv4=request.POST.get('ipv4')
        print(router)
        print(switch)
        print(interfacename)
        print(ipv4)
        result=""
        if(router):
            print("set Router")
            result = AutomationMethods.set_interfaceconfigration(router,interfacename,ipv4)
        elif(switch):
            print("set switch")
            result = AutomationMethods.set_interfaceconfigration(router,interfacename,ipv4)
        
        if(result == "ok" ): # i change here
            messages.success(request,"Interface IP has been set successfully.")
        else :
            messages.error(request,f"Error while setting the Interface Ip: {result}")# i change here
        
        if(router):    
            return render(request,'result.html',{'page':'routerconfiguration'})
            return redirect('/playground/routerconfiguration');# render(request,'router_configuration.html')
        else :
            return render(request,'result.html',{'page':'switchconfiguration'})
            return redirect('/playground/switchconfiguration');# render(request,'switch_configuration.html')



# API 

@login_required
def display_VLAN_Brief(request):
    data={
        'vlan':AutomationMethods.display_VLAN_Brief()
    }
    return JsonResponse(data,safe=False)

@login_required
def OSPF_Data(request):
    data={
        'neighborInfo':AutomationMethods.display_OSPF_Neighbor_Information(),
        'databaseInfo':AutomationMethods.display_OSPF_Database_Summary(),
    }
    return JsonResponse(data,safe=False)

def devices_list(request):
    devices = AutomationMethods.Ping()  # Call the ping method to get the list of devices
    print(devices)
    serializable_devices = [
        {'host': device.host, 'task': device.task, 'status': device.status}
        for device in devices
    ]
    return JsonResponse(serializable_devices, safe=False)



@login_required
def RouterList(request):
    # Fetch the list of devices (Facts objects)
    devices = AutomationMethods.Router_list()
    print("routerlist")
    # Serialize the devices into a JSON-compatible format
    serializable_devices = []
    for device in devices:
        # Serialize the device
        device_data = {
            'id' : device.id,
            'device': device.device,
            'interfaces': [
                {
                    'name': interface.name,
                    'address_subnet': interface.address_subnet,
                    'status': interface.status,
                    'description':interface.description
                }
                for interface in device.interfaces
            ],
            'neighbors': [
                {
                    'name': neighbor.name,
                    'address_subnet': neighbor.address_subnet,
                    'port': neighbor.port
                }
                for neighbor in device.neighbors
            ],
            'routes': [
                {
                    'protocol' : routing.protocol,
                    'network' : routing.network,
                    'interface' : routing.interface,
                    'next_hop' : routing.next_hop,
                    'admin_distance' : routing.admin_distance
                } 
                for routing in device.routing
            ]
        }
        serializable_devices.append(device_data)

    # Return the serialized data as a JSON response
    return JsonResponse(serializable_devices, safe=False)

@login_required
def SwitchList(request):
        # Fetch the list of devices (Facts objects)
    devices = AutomationMethods.Switch_list()
    print("Swithces_List")
    print(devices)
    # Serialize the devices into a JSON-compatible format
    serializable_devices = []
    for device in devices:
        # Serialize the device
        device_data = {
            'id' : device.id,
            'device': device.device,
            'interfaces': [
                {
                    'name': interface.name,
                    'address_subnet': interface.address_subnet,
                    'status': interface.status,
                    'description':interface.description
                }
                for interface in device.interfaces
            ],
            'neighbors': [
                {
                    'name': neighbor.name,
                    'address_subnet': neighbor.address_subnet,
                    'port': neighbor.port
                }
                for neighbor in device.neighbors
            ],
            'vlan': [
                {
                    'id' : vlan.id,
                    'name' : vlan.name,
                    'status' : vlan.status,
                    'port' : vlan.port,
                } 
                for vlan in device.vlans
            ]
        }
        serializable_devices.append(device_data)

    # Return the serialized data as a JSON response
    return JsonResponse(serializable_devices, safe=False)

