from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

def home(request:HttpRequest):

    return render(request, "inventory/home.html")

def inventory(request:HttpRequest):


    return render(request, "inventory/inventory.html")

