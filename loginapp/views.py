from django.shortcuts import render,redirect
from.import models
from.models import User
from django.contrib import messages


def index(request):
    return render(request,'registration.html')

def register(request):
    if request.method=="POST":
        errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
                models.create_user (request)
    return redirect('/')

def login(request):
    if request.method == "POST":
        if login(request):
            id = request.session['userid'] 
            user = models.get_login(id)
            context = {
                "user" : user
            }
            return render(request,'welcom.html',context)

    return redirect('/')
