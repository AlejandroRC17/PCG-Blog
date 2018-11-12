import csv
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, IntegerField
from wtforms.validators import Required

# FORMULARIOS

class BusquedaCliente(FlaskForm):
	campocliente = StringField('Ingrese proveedor', validators = [Required()])

class BusquedaProducto(FlaskForm):
	campoproducto = StringField('Ingrese producto', validators = [Required()])

class AgregarVenta(FlaskForm):
    cliente = StringField('Proveedor:', validators=[Required()])
    producto = StringField('Producto:',validators=[Required()])
    cantidad = IntegerField('Cantidad:',validators=[Required(message = 'Debe ingresar un numero')])

class Csv:
    def __init__ (self, codigo, cliente, producto, cantidad):
        self.codigo = codigo
        self.cliente = cliente
        self.producto = producto
        self.cantidad = cantidad
#        self.precio = precio
    def __str__ (self):
        return '{}, {}, {}, {}'.format(self.codigo, self.cliente, self.producto, self.cantidad)
    def __gt__ (self, otro):
        return self.cantidad > otro.cantidad

def catcsv(archivocsv):
    listaregistros = []
    with open(archivocsv) as archivo:
        archivo_csv = csv.reader(archivo)
        x = 0
        for linea in archivo_csv:
            if x == 0:
                y = 0
                for y in range(4):
                    campo = linea[y]
                    if campo == 'CODIGO':
                        campo_codigo = y
                    elif campo == 'CLIENTE':
                        campo_cliente = y
                    elif campo == 'PRODUCTO':
                        campo_producto = y
                    elif campo == 'CANTIDAD':
                        campo_cantidad = y
                x = x + 1
            else:
                listaregistros.append(Csv(codigo = linea[campo_codigo], cliente = linea[campo_cliente].upper(), producto = linea[campo_producto].upper(), cantidad = float(linea[campo_cantidad])))
    return (listaregistros)
