from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cedula=models.CharField(primary_key=True, max_length=13 ,null=False)
    nombres=models.CharField(max_length=150, null=False)
    direccion=models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=45)
    celular=models.CharField(max_length=10, null=False)

    class Meta:
        db_table = 'tabla_Cliente'
    
class Producto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo_producto = models.CharField(primary_key=True, max_length=9)
    nombre_articulo = models.CharField(max_length=90)
    unidades = models.IntegerField()
    precio= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        db_table = 'tabla_Producto'


class Factura(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    numeroF= models.AutoField(primary_key=True)
    fecha = models.DateField() 
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    formaPago = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
       
    class Meta:
        db_table = 'tabla_Factura'  


class Venta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    unidades = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
           
    class Meta:
        db_table = 'tabla_Venta'
