from django.shortcuts import render, redirect
from .models import Clientes, Productos, Precios, Ventas
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.contrib.auth import authenticate, login
from datetime import date

# Create your views here.

TEMPLATES_DIRS =(
    'os.path.join(BASE_DIR, "templates")'

)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'Login.html')
    

def base(request):
    return render(request, 'base.html')


def nuevoC(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        
        # verificar si la cédula ya esta registrada
        try:
            cliente_existente = Clientes.objects.get(cedula=cedula)
            messages.error(request, f'La cédula {cedula} ya está registrada.')
            return render(request, "nuevoC.html")
        except ObjectDoesNotExist:
            pass

        # guardar el nuevo cliente
        clientes2 = Clientes(
            cedula=request.POST.get('cedula'),
            nombres=request.POST.get('nombres'),
            apellidos=request.POST.get('apellidos'),
            direccion=request.POST.get('direccion'),
            email=request.POST.get('email'),
            celular=request.POST.get('celular')
        )
        clientes2.save()
        messages.success(request, 'Los datos del cliente han sido guardados correctamente.')
        return redirect("clientes")
    else:
        return render(request, "nuevoC.html")
    


def ventas(request):
    venta = Ventas.objects.all()
    datos ={'venta' : venta}
    return render(request,"ventas.html", datos)

def clientes(request):
    clientes1 = Clientes.objects.all()
    datos = {'venta' : clientes1}
    return render(request,"clientes.html", datos)

def editarCliente(request, cedula):
    try:
        cliente = Clientes.objects.get(cedula=cedula)
    except Clientes.DoesNotExist:
        messages.error(request, 'El cliente que intentas editar no existe.')
        return HttpResponseRedirect('/clientes/')  

    if request.method == 'POST':
        # actualizar y guardar los campos del cliente 
        cliente.nombres = request.POST.get('nombres')
        cliente.apellidos = request.POST.get('apellidos')
        cliente.direccion = request.POST.get('direccion')
        cliente.email = request.POST.get('email')
        cliente.celular = request.POST.get('celular')
        cliente.save()
        messages.success(request, 'Los datos del cliente han sido actualizados correctamente.')
        return HttpResponseRedirect('/clientes/')  

    return render(request, "editarCliente.html", {'cliente': cliente})    

def eliminarCliente(request, cedula):
   try:
         cliente = Clientes.objects.get(cedula=cedula)
   except Clientes.DoesNotExist:
        messages.error(request, 'El cliente que intentas eliminar no existe.')
        return redirect("clientes")  
   if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'El cliente ha sido eliminado correctamente.')
        return redirect("clientes")  
   else:
        return render(request, "eliminarcliente.html", {'cliente': cliente})
   
def productos(request):
    if request.method == 'POST':
        codigo_producto = request.POST.get('codigo_producto')
        nombre_arituclo = request.POST.get('nombre_articulo')
        unidades = request.POST.get('unidades')
        
        # verifica si ya existe un producto con el mismo codigo
        if Productos.objects.filter(codigo_producto=codigo_producto).exists():
            messages.error(request, f'El producto con código {codigo_producto} ya tiene inventario.')
        else:
            # guardar producto
            inventarioN = Productos(codigo_producto=codigo_producto, nombre_articulo=nombre_arituclo, unidades=unidades)
            inventarioN.save()
            messages.success(request, 'Los datos del producto han sido guardados correctamente.')
        
        # obtener la lista actualizada de productos
        listaI = Productos.objects.all()
        datosli = {'inv': listaI}
        return render(request, "inventario.html", datosli)
    else:
        # si no es POST solo se  muestra la lista de productos
        listaI = Productos.objects.all()
        datosli = {'inv': listaI}
        return render(request, "inventario.html", datosli)


def eliminarProducto(request, codigo_producto):
    producto = Productos.objects.get(codigo_producto=codigo_producto)
    producto.delete()
    return redirect('productos')

def editarInventario(request, codigo_producto):
    try:
        producto = Productos.objects.get(codigo_producto=codigo_producto)
    except Productos.DoesNotExist:
        messages.error(request, 'El producto seleccionado no existe.')
        return redirect('productos')

    if request.method == 'POST':
        # actualizar las unidades
        unidades = request.POST.get('unidades')
        producto.unidades = unidades
        producto.save()
        messages.success(request, 'Las unidades del producto han sido actualizadas correctamente.')
        return redirect('productos')
    else:
        return render(request, 'inventario.html', {'producto': producto})

def listaPrecios(request):
    if request.method == 'POST':
        producto = request.POST.get('producto')
        precio = request.POST.get('precio')

        try:
            producto = Productos.objects.get(codigo_producto=producto)
        except Productos.DoesNotExist:
            messages.error(request, 'El producto especificado no existe.')
            return redirect('listaPrecios')

        if Precios.objects.filter(producto=producto).exists():
            messages.error(request, 'El producto ya esta registrado en la lista de precios.')
            return redirect('listaPrecios')
        else:
            precio = Precios(producto=producto, precio=precio)
            precio.save()
            messages.success(request, 'El precio del producto ha sido asignado correctamente.')

        return redirect('listaPrecios')     
    else:
        # si no es POST muestra la lista de productos
        listaP = Precios.objects.all()
        datosP = {'preci': listaP}
        return render(request, "listaPrecios.html", datosP)

def editarPrecio(request, producto):
    try:
        productObj = Productos.objects.get(codigo_producto=producto)
    except Productos.DoesNotExist:
        messages.error(request, 'El producto seleccionado no existe en el inventario.')
        return redirect('listaPrecios')
    try:
        precios = Precios.objects.get(producto=productObj)
    except Precios.DoesNotExist:
        messages.error(request, 'No se encontró el producto en la lista de precios')
        return redirect('listaPrecios')

    if request.method == 'POST':
        # actualizar precios
        nuevoPrecio = request.POST.get('precio')
        precios.precio = nuevoPrecio
        precios.save()
        messages.success(request, 'El precio del producto ha sido actualizado correctamente.')
        return redirect('listaPrecios')
    else:
        return render(request, 'editarPrecio.html', {'precios': precios})
    

def eliminarPrecio(request, producto):
    try:
        precio = Precios.objects.get(producto=producto)
        if request.method == 'POST':
            precio.delete()
            messages.success(request, 'El precio ha sido eliminado correctamente.')
            return redirect('listaPrecios')  
        else:
            return render(request, 'listaPrecios.html')  
    except Precios.DoesNotExist:
        messages.error(request, 'El precio que intentas eliminar no existe.')
        return redirect('listaPrecios') 
    

def nuevaVenta(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente', '')
        unidades_list = request.POST.getlist('unidades[]')
        articulo_list = request.POST.getlist('articulo[]')
        valor_total_list = request.POST.getlist('valor_total[]')

        # verifica si el cliente existe en la base
        cliente_existe = Clientes.objects.filter(cedula=cliente_id).exists()

        if cliente_existe:
            cliente = Clientes.objects.get(cedula=cliente_id)
            productos_validos = True
            ventas = []

            for articulo_id, unidades, valor_total in zip(articulo_list, unidades_list, valor_total_list):
                if Productos.objects.filter(codigo_producto=articulo_id).exists():
                    producto = Productos.objects.get(codigo_producto=articulo_id)
                    
                    # verifica si el producto tiene un precio asignado
                    if not Precios.objects.filter(producto=producto).exists():
                        productos_validos = False
                        messages.error(request, f'El producto con código {articulo_id} no tiene precio asignado.')
                        break

                    # verificar si hay suficiente stock
                    if producto.unidades < int(unidades):
                        productos_validos = False
                        messages.error(request, f'No hay suficientes unidades disponibles del producto con código {articulo_id}.')
                        break
                    
                    venta = Ventas(cliente=cliente, articulo=producto, unidades=int(unidades), valor_total=valor_total)
                    ventas.append(venta)
                else:
                    productos_validos = False
                    messages.error(request, f'El producto con código {articulo_id} no existe.')
                    break

            if productos_validos:
                for venta in ventas:
                    venta.save()

                    # Restar unidades vendidas del inventario
                    producto = venta.articulo
                    producto.unidades -= int(venta.unidades)
                    producto.save()

                messages.success(request, 'La venta ha sido registrada correctamente.')
                return redirect('nuevaVenta')
        else:
            messages.error(request, 'El cliente no existe.')

    return render(request, 'nuevaVenta.html')
    
def obtener_cliente(request):
    cedula = request.GET.get('cedula', None)
    if cedula and Clientes.objects.filter(cedula=cedula).exists():
        cliente = Clientes.objects.get(cedula=cedula)
        data = {
            'nombres': cliente.nombres,
            'apellidos': cliente.apellidos,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

def obtener_producto(request):
    codigo_producto = request.GET.get('codigo_producto', None)
    if codigo_producto and Productos.objects.filter(codigo_producto=codigo_producto).exists():
        producto = Productos.objects.get(codigo_producto=codigo_producto)
        precio = Precios.objects.filter(producto=producto).first().precio if Precios.objects.filter(producto=producto).exists() else None
        data = {
            'nombre_articulo': producto.nombre_articulo,
            'precio': precio,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Producto no encontrado'}, status=404)


def editarVenta(request, venta_id):
    try:
        venta = Ventas.objects.get(id=venta_id)
    except Ventas.DoesNotExist:
        messages.error(request, 'La venta que intentas editar no existe.')
        return redirect('/ventas/')  

    cliente = venta.cliente
    producto = venta.articulo

    if request.method == 'POST':
        venta.unidades = request.POST.get('unidades')
        venta.valor_total = request.POST.get('valor_total')
        venta.fecha = date.today()
        venta.save()
        messages.success(request, 'Los datos de la venta han sido actualizados correctamente.')
        return redirect('/ventas/') 
    contexto = {
        'cliente': cliente,
        'venta': venta,
        'producto': producto,
    }
    return render(request, "editarVenta.html", contexto)

def eliminarVenta(request, venta_id):
    try:
        venta = Ventas.objects.get(pk=venta_id)
        if request.method == 'POST':
            venta.delete()
            messages.success(request, 'La venta ha sido eliminada correctamente.')
            return redirect('ventas')
        else:
            return render(request, 'ventas.html')  
    except Ventas.DoesNotExist:
        messages.error(request, 'La venta que intentas eliminar no existe.')
        return redirect('ventas')

def dashboard(request):
    return render(request,"dashboard.html")
