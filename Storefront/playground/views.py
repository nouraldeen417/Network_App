from django.http import HttpResponse
from .utils import AutomationMethods
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def sayhello(request):
    return render(request,'hello.html')
    #return HttpResponse('Hello')
    
def device_list(request):
    devices = AutomationMethods.Ping()  # Call the ping method to get the list of devices
    print(devices)
    serializable_devices = [
        {'host': device.host, 'task': device.task, 'status': device.status}
        for device in devices
    ]
    return JsonResponse(serializable_devices, safe=False)

def RoutersView(request):
    return render(request,'router.html')

class RouterList(APIView):
    def get(self,requset):
        return Response([{'name':"Router1" , 'ip_address':"192.167.0.1",'location':"home",'status':"Stopped"},{'name':"Router2" , 'ip_address':"192.167.0.2",'location':"home",'status':"Running"}] ,status=status.HTTP_200_OK)
    

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

def SwitchesView(request):
    return render(request,'router.html')

def FirewallView(request):
    return render(request,'router.html')

def dowork(request):
    if request.method == 'POST':
        user_input = request.POST.get('ip')
        # You can process the input here
        return HttpResponse(f'You entered: {AutomationMethods.Ping()}')
    return  render(request,'hello.html',{'name':"Hagag"})