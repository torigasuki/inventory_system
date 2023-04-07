from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('erp/' , views.erp_view, name='erp'),
    path('products/', views.products_view, name='products'),
    path('inbound/', views.inbound_view, name='inbound'),
    path('unbound/', views.unbound_view, name='unbound'),
]