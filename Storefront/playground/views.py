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
    if request.user.is_staff:  # Check if the user is an admin
        return render(request, 'admin_hello.html')  # Admin-specific homepage
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
    
def routerconfiguration(request):
    router = request.GET.get('router', None)
    print(router)
    return render(request,'router_configuration.html',{'router': router})


def sethostname(request):
    selectedrouter=None
    if request.method == "POST":
        router=request.POST.get('router')
        hostname=request.POST.get('hostname')
        print(router)
        print(hostname)
        result = AutomationMethods.Set_Hostname(router,hostname)
        selectedrouter=router
        if(result == "successful"):
            messages.success(request,"Hostname has been setten Successfully")
        else :
            messages.error(request,"Unexpected error when setting Host name, please try again error")
    return render(request,'router_configuration.html',{'router': selectedrouter})

def setbanner(request):
    selectedrouter=None
    if request.method == "POST":
        router=request.POST.get('router')
        banner=request.POST.get('banner')
        print(router)
        print(banner)
        result = AutomationMethods.Set_Banner(router,banner)
        selectedrouter=router
        if(result == "successful" ):
            messages.success(request,"Banner has been setten Successfully")
        else :
            messages.error(request,"Unexpected error when setting Banner name, please try again error")
    return render(request,'router_configuration.html',{'router': selectedrouter})


def setInterfaceConfigration(request):
    selectedrouter=None
    if request.method == "POST":
        router=request.POST.get('router')
        interfacename=request.POST.get('interface')
        ipv4=request.POST.get('ipv4')
        
        print(router)
        print(interfacename)
        print(ipv4)
        result = AutomationMethods.set_interfaceconfigration(router,interfacename,ipv4)
        selectedrouter=router
        if(result == "successful" ):
            messages.success(request,"Interface IP has been setten Successfully")
        else :
            messages.error(request,"Unexpected error when setting Interface Ip, please try again error")
    return render(request,'router_configuration.html',{'router': selectedrouter})

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
                    'status': interface.status
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
            ]
        }
        serializable_devices.append(device_data)

    # Return the serialized data as a JSON response
    return JsonResponse(serializable_devices, safe=False)

@login_required
def SwitchList(request):
        devices=AutomationMethods.Switch_list()
        serializable_devices = [
        {'name':device.name , 'ip_address':device.ip_address,'location':device.location,'status':device.status}
        for device in devices
        ]
        return JsonResponse(serializable_devices, safe=False)
        return Response([{'name':"Switch1" , 'ip_address':"192.167.0.1",'location':"home",'status':"Stopped"},{'name':"switch2" , 'ip_address':"192.167.0.2",'location':"home",'status':"Running"}] ,status=status.HTTP_200_OK)

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