from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth

# Create your views here.
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('confirm_password')

        if not password == password_confirmation:
            messages.add_message(request, constants.ERROR, 'Passwords don\'t match.')
            return redirect('/users/register/')
        
        if len(password) < 6:
            messages.add_message(request, constants.ERROR, 'Password must be at least 6 characters.')
            return redirect('/users/register/')
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, 'Username already exists.')
            return redirect('/users/register/')
        
        User.objects.create_user(username=username, password=password)
        messages.add_message(request, constants.SUCCESS, 'User created successfully.')
        return redirect('/users/login/')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
      
        user = authenticate(request,username=username, password=password)
        if user is None:
            messages.add_message(request, constants.ERROR, 'Invalid username or password.')
            return redirect('login')
        
        auth.login(request, user)
        return redirect('/mentorship/')

def logout(request):
    auth.logout(request)
    return redirect('login')