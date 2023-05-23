from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.contrib import auth

def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, 'Passwords do not match')
            return redirect(reverse('signup'))

        #to-do: validar força da senha

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'User already exists')
            return redirect(reverse('signup'))

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.add_message(request, constants.SUCCESS, 'User succesfully registred')

        return redirect(reverse('login'))

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, constants.ERROR, 'Invalid username or password')
            return redirect(reverse('login'))

        auth.login(request, user)
        return redirect('/events/new_marathon/')