from django.shortcuts import render
from django.http import HttpResponse
from .utils import AutomationMethods
# Create your views here.
def sayhello(request):
    return render(request,'hello.html',{'name':"Hagag"})
    #return HttpResponse('Hello')
    
def dowork(request):
    if request.method == 'POST':
        user_input = request.POST.get('ip')
        # You can process the input here
        return HttpResponse(f'You entered: {AutomationMethods.Ping(user_input)}')
    return  render(request,'hello.html',{'name':"Hagag"})