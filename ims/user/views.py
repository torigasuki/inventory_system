from django.shortcuts import render,redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/sign_up.html')
        
    elif request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2','')
        email = request.POST.get('email')


        if password != password2:
            return render(request, 'user/sign_up.html', {'error': 'Password does not match'})
        else:
           if username == '' and password == '' and email == '':
                return render(request, 'user/sign_up.html', {'error': 'Please fill all the fields'})
           else:
                exist_user = get_user_model().objects.filter(username=username)
                if exist_user:
                    return render(request, 'user/sign_up.html', {'error': 'Username already exists'})
                else:
                    UserModel.objects.create_user(username=username, password=password, email=email)
                    return redirect('/login/')
                
def login_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/erp/')
        else:
            return render(request, 'user/login.html')
        
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)

        if me is not None:
            auth.login(request, me)
            return redirect('/erp/')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid username or password'})
@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('/login/')