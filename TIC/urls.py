"""
URL configuration for TIC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login_view, name="login"),
    path('base/', views.base),
    path('clientes/', views.clientes, name="clientes"),
    path('nuevoC/', views.nuevoC, name="nuevoC"),
    path('ventas/', views.ventas,name="ventas"),
    path('editarCliente/<cedula>', views.editarCliente,name="editarCliente"),
    path('clientes/eliminarCliente/<cedula>', views.eliminarCliente,name="eliminarCliente"),
    path('productos/', views.productos, name="productos"),
    path('eliminarProducto/<codigo_producto>/', views.eliminarProducto, name='eliminarProducto'),
    path('editarInventario/<codigo_producto>/', views.editarInventario, name="editarInventario"),
    path('listaPrecios/', views.listaPrecios, name="listaPrecios"),
    path('editarPrecio/<producto>/', views.editarPrecio, name="editarPrecio"),
    path('nuevaVenta/', views.nuevaVenta, name="nuevaVenta"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('obtener_cliente/', views.obtener_cliente, name='obtener_cliente'),
    path('obtener_producto/', views.obtener_producto, name='obtener_producto'),


]
