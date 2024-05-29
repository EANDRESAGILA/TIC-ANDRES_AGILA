from django.db import models
from django.db.models import F
# Create your models here.

class Clientes(models.Model):
    cedula=models.CharField(primary_key=True, max_length=13, null=False)
    nombres=models.CharField(max_length=50, null=False)
    apellidos=models.CharField(max_length=50, null=False)
    direccion=models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=45)
    celular=models.CharField(max_length=10, null=False)

    class Meta:
        db_table = 'tabla_clientes'
    
class Productos(models.Model):
    codigo_producto = models.CharField(primary_key=True, max_length=20)
    nombre_articulo = models.CharField(max_length=90)
    unidades = models.IntegerField()
    class Meta:
        db_table = 'tabla_Productos'

    def restar_unidades(self, unidades_vendidas):
        self.unidades = F('unidades') - unidades_vendidas
        self.save()

class Precios(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'tabla_Precios'


class Ventas(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Productos, on_delete=models.CASCADE)
    unidades = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'tabla_Ventas'

    