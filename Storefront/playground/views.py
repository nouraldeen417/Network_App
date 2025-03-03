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
def FirewallView(request):
    return render(request,'firewall.html')
@login_required
def routerconfiguration(request):
    return render(request,'router_configuration.html')

@login_required
def switchconfiguration(request):
    return render(request,'switch_configuration.html')


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
        print(routers)
        print(cidr)
        print(ospf_id)
        print(area_id)
        print(interfaces)
        print(hello_timer)
        print(dead_timer)
        print(tag)
        result=AutomationMethods.Ospf_routing(
            routers,interfaces,cidr,
            ospf_id,routers,area_id,
            hello_timer,dead_timer,tag
        )
        print(result)
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
        
        AutomationMethods.Vlans_configs(switches,interfaces,vlan_cidr,vlanid,vlanname,tag)
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
            return redirect('/playground/routerconfiguration');# render(request,'router_configuration.html')
        else :
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
            return redirect('/playground/routerconfiguration');# render(request,'router_configuration.html')
        else :
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
            return redirect('/playground/routerconfiguration');# render(request,'router_configuration.html')
        else :
            return redirect('/playground/switchconfiguration');# render(request,'switch_configuration.html')
        
# API 
@login_required
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

@login_required
def FirewallList(request):
        devices=AutomationMethods.Firewall_list()
        serializable_devices = [
        {'name':device.name , 'ip_address':device.ip_address,'location':device.location,'status':device.status}
        for device in devices
        ]
        return JsonResponse(serializable_devices, safe=False)
        return Response([{'name':"Firewall1" , 'ip_address':"192.167.0.1",'location':"home",'status':"Stopped"},{'name':"firewall2" , 'ip_address':"192.167.0.2",'location':"home",'status':"Running"}] ,status=status.HTTP_200_OK)

@login_required
def RouterDoWork(request):
    # Data I will Take from nour (Routers and thier status[stop, active]) 
    if request.method == 'POST':
        selected_router_ids = request.POST.getlist('selectedRouterIPs[]')
        print(selected_router_ids)
        if selected_router_ids:
            messages.success(request, "Routers selected successfully!")
        else:
            messages.error(request, "No routers selected. Please try again.")
            
    # Redirect to the main view
    return redirect('RoutersView')

@login_required
def SwitchDoWork(request):
    # Data I will Take from nour (Routers and thier status[stop, active]) 
    if request.method == 'POST':
        selected_router_ids = request.POST.getlist('selectedRouterIPs[]')
        print(selected_router_ids)
        if selected_router_ids:
            messages.success(request, "Routers selected successfully!")
        else:
            messages.error(request, "No routers selected. Please try again.")
            
    # Redirect to the main view
    return redirect('RoutersView')

@login_required
def FirewallDoWork(request):
    # Data I will Take from nour (Routers and thier status[stop, active]) 
    if request.method == 'POST':
        selected_router_ids = request.POST.getlist('selectedRouterIPs[]')
        print(selected_router_ids)
        if selected_router_ids:
            messages.success(request, "Routers selected successfully!")
        else:
            messages.error(request, "No routers selected. Please try again.")
            
    # Redirect to the main view
    return redirect('RoutersView')

@login_required
def dowork(request):
    if request.method == 'POST':
        user_input = request.POST.get('ip')
        # You can process the input here
        return HttpResponse(f'You entered: {AutomationMethods.Ping()}')
    return  render(request,'hello.html',{'name':"Hagag"})