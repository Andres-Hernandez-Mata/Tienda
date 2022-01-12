from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/tienda.db'
db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_barra = db.Column(db.String(250))
    nombre = db.Column(db.String(250))
    precio = db.Column(db.Integer())

@app.route("/")
def main():    
    return render_template("index.html")

@app.route("/productos")
def listar_productos():        
    productos = db.session.execute('SELECT * FROM producto').fetchall()
    db.session.close()
    return render_template("productos.html", productos = productos)

@app.route("/crear-producto", methods=["POST"])
def crear_producto():
    agregar_produco = Producto(codigo_barra = request.form["codigo_barra"], nombre = request.form["nombre"], precio = request.form["precio"])
    db.session.add(agregar_produco)
    db.session.commit()
    return redirect(url_for("listar_productos"))

@app.route("/editar/<id>")
def editar_producto(id):
    producto = Producto.query.get(id)
    return redirect(url_for("listar_productos"))

@app.route("/eliminar/<id>")
def eliminar_producto(id):
    Producto.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("listar_productos"))

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug = True)


