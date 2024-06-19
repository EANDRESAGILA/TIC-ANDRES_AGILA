from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Cliente, Producto, Venta,Factura
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



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


def logout_view(request):
    logout(request)
    messages.error(request, 'Sesion Finalizada')
    return redirect('login') 


def registroUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Por favor inicia sesión.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = UserCreationForm()
    return render(request, 'nuevoUser.html', {'form': form})
    

@login_required
def base(request):
    return render(request, 'base.html')

@login_required
def nuevoC(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        # verificar si la cédula ya esta registrada
        try:
            clientes2= Cliente.objects.get(cedula=cedula)
            messages.error(request, f'La cédula {cedula} ya está registrada.')
            return render(request, "nuevoC.html")
        except ObjectDoesNotExist:
            pass
        # guardar el nuevo cliente
        clientes2 = Cliente(
            user=request.user,
            cedula=request.POST.get('cedula'),
            nombres=request.POST.get('nombres'),
            direccion=request.POST.get('direccion'),
            email=request.POST.get('email'),
            celular=request.POST.get('celular')
         )
        clientes2.save()
        messages.success(request, 'Los datos del cliente han sido guardados correctamente.')
        return redirect("clientes")
    else:
        return render(request, "nuevoC.html")
    

@login_required
def clientes(request):
    busqueda = request.GET.get('busqueda')
    cliente = Cliente.objects.all()

    if busqueda:
        if busqueda.isdigit():  
            cliente = cliente.filter(cedula__exact=busqueda)
        else:
            cliente = cliente.filter(
                nombres__icontains=busqueda
            )

    context = {'venta': cliente, 'busqueda': busqueda}

    if not cliente.exists() and busqueda:
        messages.info(request, 'No existen registros con el nombre o cedula proporcionada.')
        return redirect('clientes')

    return render(request, "clientes.html", context)
    

@login_required
def editarCliente(request, cedula):
    try:
        cliente = Cliente.objects.get(cedula=cedula)
    except Cliente.DoesNotExist:
        messages.error(request, 'El cliente que intentas editar no existe.')
        return redirect("clientes")

    if request.method == 'POST':
        # actualizar y guardar los campos del cliente 
        cliente.nombres = request.POST.get('nombres')
        cliente.direccion = request.POST.get('direccion')
        cliente.email = request.POST.get('email')
        cliente.celular = request.POST.get('celular')
        cliente.save()
        messages.success(request, 'Los datos del cliente han sido actualizados correctamente.')
        return redirect("clientes") 

    return render(request, "editarCliente.html", {'cliente': cliente})    


@login_required
def eliminarCliente(request, cedula):
   try:
         cliente = Cliente.objects.get(cedula=cedula)
   except Cliente.DoesNotExist:
        messages.error(request, 'El cliente que intentas eliminar no existe.')
        return redirect("clientes")  
   if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'El cliente ha sido eliminado correctamente.')
        return redirect("clientes")  
   else:
        return render(request, "eliminarcliente.html", {'cliente': cliente})



@login_required
def productos(request):
    if request.method == 'POST':
        # Verifica si el formulario es para actualizar las unidades
        if 'nombre_codigo' in request.POST:
            nombre_codigo = request.POST.get('nombre_codigo')
            unidades2 = request.POST.get('unidades2')

            # Busca el producto por su nombre o código
            try:
                producto = Producto.objects.get(codigo_producto=nombre_codigo)
            except Producto.DoesNotExist:
                try:
                    producto = Producto.objects.get(nombre_articulo=nombre_codigo)
                except Producto.DoesNotExist:
                    messages.error(request, 'No se encontró ningún producto con el nombre o código ingresado.')
                    return redirect('productos')

            # Actualiza las unidades del producto
            producto.unidades = unidades2
            producto.save()
            messages.success(request, f'Se han actualizado las unidades del producto "{producto.codigo_producto}" "{producto.nombre_articulo} " correctamente.')
            return redirect('productos')

        # Si no es para actualizar unidades, entonces es para agregar un nuevo producto
        codigo_producto = request.POST.get('codigo_producto')
        nombre_articulo = request.POST.get('nombre_articulo')
        unidades = request.POST.get('unidades')
        
        # Verifica si ya existe un producto con el mismo código
        if Producto.objects.filter(codigo_producto=codigo_producto).exists():
            messages.error(request, f'El producto con código {codigo_producto} ya esta registrado en el inventario.')
        else:
            # guardar producto
            inventarioN = Producto(user=request.user,codigo_producto=codigo_producto, nombre_articulo=nombre_articulo, unidades=unidades)
            inventarioN.save()
            messages.success(request, 'Los datos del producto han sido guardados correctamente.')
        
        # obtener la lista actualizada de productos
        listaI = Producto.objects.all()
        datosli = {'inv': listaI}
        return render(request, "inventario.html", datosli)
    else:
        # si no es POST solo se  muestra la lista de productos
        listaI = Producto.objects.all()
        datosli = {'inv': listaI}
        return render(request, "inventario.html", datosli)
    
    

@login_required
def eliminarProducto(request, codigo_producto):
    producto = Producto.objects.get(codigo_producto=codigo_producto)
    producto.delete()
    messages.error(request, f'EL Producto {codigo_producto} eliminado correctamente.')
    return redirect('productos')


@login_required
def editarInventario(request, codigo_producto):
    try:
        producto = Producto.objects.get(codigo_producto=codigo_producto)
    except Producto.DoesNotExist:
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


@login_required
def listaPrecios(request):
    if request.method == 'POST':
        nombre_codigo = request.POST.get('nombre_codigo')   
        precio = request.POST.get('precio')
        if not precio:
            messages.error(request, 'Debe proporcionar el precio del producto.')
            return redirect('listaPrecios')
        producto = None
        try:
            # intentamos encontrar el producto por su código
            producto = Producto.objects.get(codigo_producto=nombre_codigo)
        except Producto.DoesNotExist:
            try:
                # si no se encuentra por código, intentamos encontrarlo por nombre
                producto = Producto.objects.get(nombre_articulo=nombre_codigo)
            except Producto.DoesNotExist:
                # si no se encuentra por nombre ni por código, mostramos un mensaje de error
                messages.error(request, 'No se encontró ningún producto con el nombre o código ingresado')
                return redirect('listaPrecios')
        # si se encontró el producto, actualizamos su precio
        producto.precio = precio
        producto.save()
        messages.success(request, 'El precio del producto se ha actualizado correctamente.')
        return redirect('listaPrecios')
    else:
        listaI = Producto.objects.all()
        datosli = {'inv': listaI}
        return render(request, "listaPrecios.html", datosli)


@login_required   
def eliminarPrecio(request, codigo_producto):
    try:
        producto = Producto.objects.get(codigo_producto=codigo_producto)
    except Producto.DoesNotExist:
        messages.success(request, 'El producto no existe.')
        return redirect('listaPrecios')
    # si exsiste actualiza el precio del producto a 0
    producto.precio = 0
    producto.save()
    messages.success(request, 'El precio se borro ($0).')
    return redirect('listaPrecios')  



@login_required
def nuevaVenta(request):  
    if request.method == 'POST':
        # Recuperar los datos del formulario
        fecha = request.POST.get('fecha')
        cedula_cliente = request.POST.get('cedula')

        # Verificar si el cliente existe en la base de datos
        try:
            cliente = Cliente.objects.get(cedula=cedula_cliente)
        except Cliente.DoesNotExist:
            messages.error(request, f'El cliente con cédula {cedula_cliente} no existe.')
            return redirect('nuevaVenta')

        forma_pago = request.POST.get('forma_pago')
        observaciones = request.POST.get('observaciones')

        # Verificar si todos los productos tienen suficiente stock antes de crear la factura y las ventas
        productos_con_stock_insuficiente = []
        for i in range(len(request.POST.getlist('codigo_producto[]'))):
            codigo_producto = request.POST.getlist('codigo_producto[]')[i]
            producto = get_object_or_404(Producto, codigo_producto=codigo_producto)
            unidades = int(request.POST.getlist('unidades[]')[i])

            if unidades > producto.unidades or unidades <= 0:
                productos_con_stock_insuficiente.append(codigo_producto)

        if productos_con_stock_insuficiente:
            messages.error(request, f'No hay suficiente stock para el producto: {", ".join(productos_con_stock_insuficiente)}.')
            return redirect('nuevaVenta')

        # Crear una nueva instancia de Factura y guardarla en la base de datos
        factura = Factura.objects.create(user=request.user,fecha=fecha, cliente=cliente, formaPago=forma_pago,
                                         observaciones=observaciones, subtotal=0, iva=0, total=0)

        subtotal_general = 0  # Variable para calcular el subtotal general de la factura

        for i in range(len(request.POST.getlist('codigo_producto[]'))):
            codigo_producto = request.POST.getlist('codigo_producto[]')[i]
            producto = get_object_or_404(Producto, codigo_producto=codigo_producto)
            unidades = int(request.POST.getlist('unidades[]')[i])
            precio = float(request.POST.getlist('precio[]')[i])

            subtotal_producto = unidades * precio
            subtotal_general += subtotal_producto

            #crear instancia de venta y guardar en la base de datos
            Venta.objects.create(user=request.user,factura=factura, producto=producto, unidades=unidades,
                                 precio=precio, subtotal=subtotal_producto)

            #actualizar el stock del producto
            producto.unidades -= unidades
            producto.save()

        #actualizar el subtotal, iva y total de la factura
        iva = subtotal_general * 0.15  
        total = subtotal_general + iva
        factura.subtotal = subtotal_general
        factura.iva = iva
        factura.total = total
        factura.save()

        messages.success(request, f'La factura {factura.numeroF} se ha registrado correctamente.')

        return redirect('nuevaVenta')  
    else:
        return render(request, 'nuevaVenta.html')  
    
    

 
@login_required  
def autoCliente(request):
    cedula = request.GET.get('cedula', None)
    if cedula and Cliente.objects.filter(cedula=cedula).exists():
        cliente = Cliente.objects.get(cedula=cedula)
        data = {
            'cliente': cliente.nombres,
            'contacto': cliente.celular,
            'email': cliente.email,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    

    
@login_required 
def autoProducto(request):
    codigo_producto = request.GET.get('codigo_producto', None)
    if codigo_producto and Producto.objects.filter(codigo_producto=codigo_producto).exists():
        producto = Producto.objects.get(codigo_producto=codigo_producto)
        data = {
            'nombre_articulo': producto.nombre_articulo,
            'precio': producto.precio,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    

@login_required     
def factura(request):
    busqueda = request.GET.get('busqueda')
    user = request.user
    facturas = Factura.objects.filter(user=user)

    if busqueda:
        if busqueda.isdigit():  
            facturas = facturas.filter(numeroF__exact=busqueda).union(
                facturas.filter(
                    cliente__cedula__exact=busqueda
                )
            )
        else:
            facturas = facturas.filter(
                cliente__nombres__icontains=busqueda
            )

    context = {'fact': facturas, 'busqueda': busqueda}

    if not facturas.exists() and busqueda:
        messages.info(request, 'No existen registros con el número, cédula o nombre proporcionado.')
        return redirect('factura')

    return render(request, "factura.html", context)

@login_required 
def visualizarVenta(request, numeroF):
    factura = get_object_or_404(Factura, numeroF=numeroF)
    ventas = Venta.objects.filter(factura=factura)
    
    context = {
        'factura': factura,
        'ventas': ventas,
    }
    return render(request, 'visualizarVenta.html', context)

@login_required 
def editarF(request, numeroF):
    factura = get_object_or_404(Factura, numeroF=numeroF)
    ventas = Venta.objects.filter(factura=factura)

    if request.method == 'POST':
        # actualizo los datos de la factura
        factura.formaPago = request.POST.get('forma_pago')
        factura.observaciones = request.POST.get('observaciones')
        factura.subtotal = float(request.POST.get('subtotal'))
        factura.iva = float(request.POST.get('iva'))
        factura.total = float(request.POST.get('total'))
        factura.save()

        # listar ventas existentes y crear nuevas
        ventas.delete()
        for i in range(len(request.POST.getlist('codigo_producto[]'))):
            codigo_producto = request.POST.getlist('codigo_producto[]')[i]
            unidades = int(request.POST.getlist('unidades[]')[i])
            precio = float(request.POST.getlist('precio[]')[i])
            subtotal_producto = float(request.POST.getlist('subtotal_producto[]')[i])
            
            Venta.objects.create(
                user=request.user,
                factura=factura,
                producto=Producto.objects.get(codigo_producto=codigo_producto),
                unidades=unidades,
                precio=precio,
                subtotal=subtotal_producto
            )
        messages.success(request, 'Factura actualizada correctamente.')
        return redirect('factura')

    context = {
        'factura': factura,
        'ventas': ventas,
    }
    return render(request, 'editarFactura.html', context)


@login_required 
def eliminarFactura(request, numeroF):
    factura= Factura.objects.get(numeroF=numeroF)
    factura.delete()
    messages.error(request, f'La Factura #{numeroF} eliminada correctamente.')
    return redirect('factura')

@login_required 
def dashboard(request):
    return render(request,"dashboard.html")
