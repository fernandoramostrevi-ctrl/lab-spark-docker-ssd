from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime
from models import Ingrediente, Sandwich, Compra, SistemaCompras

# Autor: Juan Gutierrez Miranda
# Fecha de creación: 2024-01-27

# Instalar dependencias
import install_dependencies

app = Flask(__name__)

# Instancia del sistema de compras
sistema_compras = SistemaCompras()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hacer_sandwich', methods=['GET', 'POST'])
def hacer_sandwich():
    if request.method == 'POST':
        # Obtener los ingredientes seleccionados por el usuario
        ingredientes_seleccionados = request.form.getlist('ingredientes')

        # Crear el sándwich
        sandwich = Sandwich()
        for ingrediente_nombre in ingredientes_seleccionados:
            sandwich.agregar_ingrediente(sistema_compras.ingredientes[ingrediente_nombre])

        # Guardar la compra
        compra = Compra(sandwich)
        sistema_compras.compras.append(compra)
        compra.guardar_compra()

        return redirect(url_for('ver_sandwich'))

    # Mostrar la página para hacer el sándwich
    return render_template('hacer_sandwich.html', ingredientes=sistema_compras.ingredientes)

@app.route('/ver_sandwich')
def ver_sandwich():
    if sistema_compras.compras:
        ultima_compra = sistema_compras.compras[-1]
        sandwich = ultima_compra.get_sandwich()
        ingredientes = [ingrediente.get_nombre().capitalize() for ingrediente in sandwich.get_ingredientes()]
        total = sandwich.get_total()
        return render_template('ver_sandwich.html', ingredientes=ingredientes, total=total)
    else:
        return render_template('ver_sandwich.html', ingredientes=[], total=0)

@app.route('/historial_compras')
def historial_compras():
    return render_template('historial_compras.html', compras=sistema_compras.compras)

@app.route('/pagar', methods=['GET', 'POST'])
def pagar():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        tarjeta = request.form['tarjeta']
        cvv = request.form['cvv']

        # Procesar el pago y guardar la compra
        ultima_compra = sistema_compras.compras[-1]
        ultima_compra.guardar_compra()
        sistema_compras.compras.clear()

        # Obtener los detalles de la compra
        ingredientes = [ingrediente.get_nombre().capitalize() for ingrediente in ultima_compra.get_sandwich().get_ingredientes()]
        total = ultima_compra.get_sandwich().get_total()

        return render_template('resumen_compra.html', nombre=nombre, ingredientes=ingredientes, total=total)

    # Mostrar la página de pago
    return render_template('pagar.html', total=sistema_compras.compras[-1].get_sandwich().get_total())

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    app.run(debug=True)