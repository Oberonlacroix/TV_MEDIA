from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse

def index(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

 
def home_view(request):
    return render(request, 'base.html')