from flask import Flask, render_template, request, redirect, url_for, json

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    with open('productos.json', 'r') as f:
        productos = json.load(f)
    
    categorias = sorted(set(p['categoria'] for p in productos))
    categoria_seleccionada = request.args.get('categoria')

    if categoria_seleccionada:
        productos = [p for p in productos if p['categoria'] == categoria_seleccionada]

    return render_template('index.html', productos=productos, categorias=categorias, categoria_seleccionada=categoria_seleccionada)

# Ruta para el panel de administración
@app.route('/admin')
def admin():
    with open('productos.json', 'r') as f:
        productos = json.load(f)
    return render_template('admin.html', productos=productos)

# Ruta para agregar productos
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        imagen = request.form['imagen']
        
        nuevo_producto = {
            'nombre': nombre,
            'precio': precio,
            'descripcion': descripcion,
            'categoria': categoria,
            'imagen': imagen
        }
        
        with open('productos.json', 'r') as f:
            productos = json.load(f)
        
        productos.append(nuevo_producto)
        
        with open('productos.json', 'w') as f:
            json.dump(productos, f, indent=4)
        
        return redirect(url_for('admin'))

    return render_template('agregar_producto.html')

# Ruta para editar productos
@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    with open('productos.json', 'r') as f:
        productos = json.load(f)
    
    producto = productos[id]
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['precio'] = float(request.form['precio'])
        producto['descripcion'] = request.form['descripcion']
        producto['categoria'] = request.form['categoria']
        producto['imagen'] = request.form['imagen']
        
        with open('productos.json', 'w') as f:
            json.dump(productos, f, indent=4)
        
        return redirect(url_for('admin'))

    return render_template('editar_producto.html', producto=producto, id=id)

# Ruta para eliminar productos
@app.route('/eliminar_producto/<int:id>', methods=['GET'])
def eliminar_producto(id):
    with open('productos.json', 'r') as f:
        productos = json.load(f)
    
    productos.pop(id)
    
    with open('productos.json', 'w') as f:
        json.dump(productos, f, indent=4)
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)

