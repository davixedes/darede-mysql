"""clients URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import Pattern
from django.contrib import admin
from django.urls import path
from core.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', home, name='home'),
    path('abouus/', aboutus, name='aboutus'),
    path('login/', login_view, name='login'),
    path('login_compra/', login_compra, name='login_compra'),
    path('logout/', logout_view, name='logout'),
    path('register_user/', register_user, name='register_user'),
    path('product/<int:id>/', product, name='product'),
    path('register_client/', register_client, name='register_client'),
    path('payment/<int:product_id>/', payment, name='payment'),
    path('delivery/<int:product_id>/<int:demand_id>/', delivery, name='delivery'),
    path('delivery_confirmation/<int:product_id>/<int:demand_id>/<int:delivery_id>/', delivery_confirmation, name='delivery_confirmation'),
    path('payment_confirmation/<int:product_id>/<int:demand_id>/', payment_confirmation, name='confirmation'),
    path('orders/', orders, name='orders'),
    path('delete_order/<int:demand_id>/', delete_order, name='delete_order')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)