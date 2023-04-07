from django.shortcuts import render,redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Product
# Create your views here.
def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/erp/')
    else:
        return redirect('/login/')

def erp_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            product_list = Product.objects.all()
            return render(request, 'erp/erp.html',{'product_list': product_list})
        else:
            return redirect('/login/')
    elif request.method == 'POST':
        return render(request, 'erp/erp.html')
    
@login_required
def products_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/products.html')
        else:
            return redirect('/login/')
        
    elif request.method == 'POST':
        user = request.user
        code = request.POST.get('code', '')
        name = request.POST.get('name', '')
        price = request.POST.get('price', '')
        sizes = request.POST.get('size', '')
        if code == '' or name == '' or price == '' or sizes == '':
            return render(request, 'erp/products.html', {'error': 'Please fill all the fields'})
        else:
            product = Product.objects.create(author = user, code=code, name=name, price=price, size=sizes)
            product.save()
            return redirect('/erp/')


def inbound_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/inbound.html')
        else:
            return redirect('/login/')
    elif request.method == 'POST':
        code = request.POST.get('code', '')
        inbound = request.POST.get('inbound', '')
        if code == '' or inbound == '':
            return render(request, 'erp/inbound.html', {'error': 'Please fill all the fields'})
        else:
            product = Product.objects.get(code=code)
            product.inbound_count += int(inbound)
            product.stock += int(inbound)
            product.save()
            return redirect('/erp/')
        

def unbound_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/unbound.html')
        else:
            return redirect('/login/')
    elif request.method == 'POST':
        code = request.POST.get('code', '')
        unbound = request.POST.get('unbound', '')
        if code == '' or unbound == '':
            return render(request, 'erp/inbound.html', {'error': 'Please fill all the fields'})
        else:
            product = Product.objects.get(code=code)
            if product.stock < int(unbound):
                return render(request, 'erp/unbound.html', {'error': 'Unbound count is more than stock'})
            else:
                product.unbound_count += int(unbound)
                product.stock -= int(unbound)
                product.save()
                return redirect('/erp/')