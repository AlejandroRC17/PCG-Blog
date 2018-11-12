#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_bootstrap import Bootstrap
from flask_script import Manager
from classyforms import BusquedaCliente, BusquedaProducto, AgregarVenta
import csv
import vldr_csv
import classyforms
import list_csv
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

# PAGINA INICIAL

@app.route("/")
def index():
	return render_template("index.html")

# PAGINAS CONSULTAS(ULTIMAS VENTAS, BUSQUEDAS CLIENTES PRODUCTOS, MAS VENDIDOS, CLIENTES QUE MAS GASTARON)

abrir_archivo = 'listado.csv'
vldr_csv.validarcampos(abrir_archivo)
registros = classyforms.catcsv(abrir_archivo)


@app.route("/busquedaproveedores", methods = ['GET', 'POST'])
def busquedaproveedores():
	formcliente = BusquedaCliente()
	if formcliente.validate_on_submit():
		cliente = formcliente.campocliente.data.upper()
		if len(cliente) < 3:
			flash('La busqueda debe tener al menos 3 caracteres')
			return render_template('busquedaproveedores.html', form = formcliente)
		else:
			buscarclientes = list_csv.buscar_cliente(registros, cliente)
			if len(buscarclientes) == 0:
				flash('No hay resultados')
			elif len(buscarclientes) == 1:
				listar = list_csv.productos_cliente(registros, cliente)
				return render_template('busquedaproveedores.html', form = formcliente, listar = listar, cliente = formcliente.campocliente.data.upper())
			else:
				return render_template('busquedaproveedores.html', form = formcliente, clientes = buscarclientes)
	return render_template('busquedaproveedores.html', form = formcliente)


@app.route("/busquedaproveedores/<clientes>", methods = ['GET', 'POST'])
def busquedaproveedores1(clientes):
	formcliente = BusquedaCliente()
	if formcliente.validate_on_submit():
		cliente = formcliente.campocliente.data.upper()
		if len(cliente) < 3:
			flash('La busqueda debe al menos 3 caracteres')
			return render_template('busquedaproveedores.html', form = formcliente)
		else:
			buscarclientes = list_csv.buscar_cliente(registros, cliente)
			if len(buscarclientes) == 0:
				flash('No hay resultados')
				return redirect(url_for('busquedaproveedores'))
			elif len(buscarclientes) == 1:
				listar = list_csv.productos_cliente(registros, cliente)
				return render_template('busquedaproveedores.html', form = formcliente, listar = listar, cliente = formcliente.campocliente.data.upper())
			else:
				return render_template('busquedaproveedores.html', form = formcliente, clientes = buscarclientes)
	else:
		cliente = clientes
		clientenc = list_csv.buscar_cliente(registros, cliente)
		listar = list_csv.productos_cliente(registros, cliente)
		return render_template('busquedaproveedores.html', form = formcliente, listar = listar, cliente = clientenc)


@app.route("/busquedaproductos", methods = ['GET', 'POST'])
def buscarproductos():
	formproducto = BusquedaProducto()
	if formproducto.validate_on_submit():
		producto = formproducto.campoproducto.data.upper()
		if len(producto) < 3:
			flash('Debe Ingresar por lo menos tres caracteres a buscar')
			return render_template('busquedaproductos.html', form = formproducto)
		else:
			res_pr = list_csv.buscar_productos(registros, producto)
			if len(res_pr) == 0:
				flash('No se encontraron productos')
			elif len(res_pr) == 1:
				listar = list_csv.lista_producto(registros, producto)
				return render_template('busquedaproductos.html', form = formproducto, listar = listar, producto = formproducto.campoproducto.data.upper())
			else:
				return render_template('busquedaproductos.html', form = formproducto, productos = res_pr)
	return render_template('busquedaproductos.html', form = formproducto)


@app.route("/busquedaproductos/<productos>", methods = ['GET', 'POST'])
def buscarproductos1(productos):
	formproducto = BusquedaProducto()
	if formproducto.validate_on_submit():
		producto = formproducto.campoproducto.data.upper()
		if len(producto) < 3:
			flash('Debe Ingresar por lo menos tres caracteres a buscar')
			return redirect(url_for('busquedaproductos'))
		else:
			res_pr = list_csv.buscar_productos(registros, producto)
			if len(res_pr) == 0:
				flash('No se encontraron productos')
				return redirect(url_for('busquedaproductos'))
			elif len(res_pr) == 1:
				listar = list_csv.lista_producto(registros, producto)
				return render_template('busquedaproductos.html', form = formproducto, listar = listar, producto = formproducto.campoproducto.data.upper())
			else:
				return render_template('busquedaproductos.html', form = formproducto, productos = res_pr)
	else:
		res_pr = []
		listar = []
		producto = productos
		res_pr = list_csv.buscar_productos(registros, producto)
		listar = list_csv.lista_producto(registros, producto)
		return render_template('busquedaproductos.html', form = formproducto, listar = listar, producto = producto)

# ERRORES

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500



@app.route('/agregar_registro', methods=['GET','POST'])   # AGREGO UN NUEVO REGISTRO
def agregar_registro():
	agregar_registro = AgregarVenta()
	if agregar_registro.validate_on_submit():
		cliente = agregar_registro.cliente.data
		producto = agregar_registro.producto.data
		cantidad = agregar_registro.cantidad.data
		agregar = list_csv.agregar_reg(cliente,producto,cantidad)
		flash("Se agrego correctamente")
		return redirect (url_for("listastock"))
	else:
		return render_template("agregar_nuevo.html", form = agregar_registro)


@app.route("/stock", methods = ['GET', 'POST'])
def listastock():
	with open("listado.csv", "r") as archivo:
		data = csv.reader(archivo)
		headers = next(data)
		return render_template('listadostock.html', body = data)

# DESCARGA CONSULTA (NO DISPONIBLE)

@app.route("/descargaconsulta/")
def descarga():
		flash("Descarga de consulta no disponible")
		return redirect(url_for("busquedaproveedores"))

if __name__ == "__main__":
	manager.run()
