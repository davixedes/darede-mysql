from django import http
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import datetime


User = get_user_model()

def register_user(request):
    form = RegisterForm(request.POST or None)
    
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")

        try:
            user = User.objects.create_user(username, email, password1)
        except:
            user = None

        if user == None:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] += 1
            # return redirect("/invalid_password")
            request.session['register_error'] = 1     # 1 == True
            return render(request, "login.html", {"form": form})

        login(request, user)
        return redirect(register_client)

    return render(request, "register_user.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user == None:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] += 1
            # return redirect("/invalid_password")
            request.session['invalid_user'] = 1     # 1 == True
            return render(request, "login.html", {"form": form})

        login(request, user)
        return redirect(home)

    return render(request, "login.html", {"form": form})
    

def login_compra(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user == None:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] += 1
            # return redirect("/invalid_password")
            request.session['invalid_user'] = 1     # 1 == True
            return render(request, "login.html", {"form": form})

        login(request, user)
        return redirect(home)

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(home)


def home(request):
    products = []
    products = Product.objects.all
    
    if request.user.is_authenticated:      
        user = request.user
        return render(request, 'home_logged_in.html', {'products': products, 'user': user})
    else:
        
        return render(request, 'home_logged_out.html', {'products': products})


def aboutus(request):
    return render(request, 'aboutus.html')


def product(request, id):
    product = get_object_or_404(Product, pk=id)
    product_name = product.get_fullName()

    if request.user.is_authenticated:
        user = request.user
        return render(request, 'product_logged_in.html', {'product': product, 'product_name': product_name, 'user': user})
    else:
        return render(request, 'product_logged_out.html', {'product': product, 'product_name': product_name})


@login_required
def register_client(request, *args, **kwargs):    
    form = ClientForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(home)

    return render(request, 'register_client.html', {'form': form})


@login_required(login_url='login_compra')
def payment(request, product_id):
    client = Client.objects.get(user_id=request.user.id)
    form_card = CardForm(request.POST or None, request.FILES or None)
    form_demand = DemandForm(request.POST or None, request.FILES or None)

    if Card.objects.filter(client_id=Client.objects.get(user_id=request.user.id)).exists():
        obj_demand = form_demand.save(commit=False)
        obj_demand.date = datetime.datetime.now()
        obj_demand.product = Product.objects.get(id=product_id)
        obj_demand.card = Card.objects.get(client_id=Client.objects.get(user_id=request.user.id))
        obj_demand.client = client
        obj_demand.save()

        return redirect(payment_confirmation, product_id, obj_demand.id)

    

    if form_card.is_valid():
        obj_card = form_card.save(commit=False)
        obj_card.client = client
        obj_card.save()

        obj_demand = form_demand.save(commit=False)
        obj_demand.date = datetime.datetime.now()
        obj_demand.product = Product.objects.get(id=product_id)
        obj_demand.card = Card.objects.get(client_id=Client.objects.get(user_id=request.user.id))
        obj_demand.client = client
        obj_demand.save()

        return redirect(payment_confirmation, product_id, obj_demand.id)

    return render(request, 'payment.html', {'form': form_card})


@login_required
def payment_confirmation(request, product_id, demand_id):
    product = get_object_or_404(Product, pk=product_id)
    product_name = product.get_fullName()

    demand = get_object_or_404(Demand, pk=demand_id)

    return render(request, 'payment_confirmation.html', {'product': product, 'demand': demand, 'demand_id': demand_id})


@login_required
def delivery(request, product_id, demand_id):
    product = get_object_or_404(Product, pk=product_id)
    product_name = product.get_fullName()

    form_delivery = DeliveryForm(request.POST or None, request.FILES or None)

    if form_delivery.is_valid():
        obj = form_delivery.save(commit=False)
        client = Client.objects.get(user_id=request.user.id)
        obj.client = client
        obj.product = product
        obj.save()

        demand = get_object_or_404(Demand, pk=demand_id)
        demand.payment_confirmed = True

        inventory = get_object_or_404(Inventory, product=product)
        inventory.amount = inventory.amount - 1
        inventory.save()

        return redirect(delivery_confirmation, product_id, demand_id, obj.id)
    return render(request, 'delivery.html', {'form_delivery': form_delivery})


@login_required
def delivery_confirmation(request, product_id, demand_id, delivery_id):
    product = get_object_or_404(Product, pk=product_id)
    product_name = product.get_fullName()

    demand = get_object_or_404(Demand, pk=demand_id)

    delivery = get_object_or_404(Delivery, pk=delivery_id)

    delivery_name = delivery.get_fullAddress()

    return render(request, 'delivery_confirmation.html', {'product': product, 'demand': demand, 'delivery': delivery, 'delivery_name': delivery_name})



@login_required
def orders(request):
    client = Client.objects.get(user_id=request.user.id)

    demands = []
    demands = Demand.objects.filter(client=client)
    
    return render(request, 'orders.html', {'client': client, 'demands': demands, 'delivery': delivery})


@login_required
def delete_order(request, demand_id):
    demand = Demand.objects.get(pk=demand_id)
    demand.delete()

    client = Client.objects.get(user_id=request.user.id)

    demands = []
    demands = Demand.objects.filter(client=client)
    
    return render(request, 'orders.html', {'client': client, 'demands': demands, 'delivery': delivery})

