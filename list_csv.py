import csv
import sys
import random

# BUSQUEDA PROVEEDOR
# Busca en lista registros, un proveedor que contenga los caracteres ingresados
# del formulario BusquedaProveedor y devuelve una lista con las coincidencias

def buscar_cliente(registros, nombre):
    cliente = []
    for i in range(len(registros)):
        if nombre in registros[i].cliente:
            if registros[i].cliente in cliente:
                pass
            else:
                cliente.append(registros[i].cliente)
        else:
            pass
    return cliente

# Devuelve en una lista todos los productos que suministra el proveedor

def productos_cliente(registros, cliente):
    nombre_cliente = cliente.upper()
    n_productos = []
    for i in range(len(registros)):
        if nombre_cliente in registros[i].cliente:
            n_productos.append(registros[i])
            with open('consulta.csv','w', newline='') as archivo:
                archivo.write("Productos por cliente" + '\n')
                writer = csv.writer(archivo)
                archivo.write('\n')
                writer.writerow(n_productos)
    return n_productos


# BUSQUEDAPRODUCTO
# Busca en lista registros, un producto con los mismos caracteres ingresados en el
# BusquedaProductos y devuelve las coincidencias en una lista

def buscar_productos(registros, nombre):
    producto = []
    for i in range(len(registros)):
        if nombre in registros[i].producto:
            if registros[i].producto in producto:
                pass
            else:
                producto.append(registros[i].producto)
        else:
            pass
    return producto

# Devuelve en una lista el producto y los datos de importancia

def lista_producto(registros, producto):
    nombre_producto = producto.upper()
    cliente = []
    for i in range(len(registros)):
        if nombre_producto in registros[i].producto:
            cliente.append(registros[i])
        with open('consulta.csv','w') as archivo:
            archivo.write("Lista de productos" + '\n')
            writer = csv.writer(archivo)
            writer.writerow(cliente)
    return cliente

# AGREGAR REGISTRO
# Agrega un nuevo registro a la lista medianto los campos de proveedor
# producto y cantidad, le asigna un codigo a cada registro agregado

def agregar_reg(cliente,producto,cantidad): 
	lista = ('615644','178965','212354','367351','434689','571649','664989','764314','886631','964142')
	codigo = random.choice(lista)
	cantidad = str(cantidad) + ".00"
	with open("listado.csv","a+") as archivo:
		archivo.writelines(codigo + ',' + cliente + ','+ producto + ',' + cantidad +'\n')				
		return "Se agrego correctamente"