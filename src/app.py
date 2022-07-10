from flask import Flask, render_template, request, url_for, redirect, json
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_barra = db.Column(db.String(250))
    nombre = db.Column(db.String(250))
    precio = db.Column(db.Integer())

class ProductoForm(FlaskForm):
    codigo_barra = StringField('codigo_barra', validators=[DataRequired()])
    nombre       = StringField('nombre', validators=[DataRequired()])
    precio       = IntegerField('precio', validators=[DataRequired()])    

@app.route("/")
def main():    
    return render_template("index.html")

@app.route("/productos")
def listar_productos():        
    productos = db.session.execute("SELECT * FROM producto").fetchall()
    db.session.close()
    return render_template("productos.html", productos = productos)

@app.route("/crear_producto", methods=["POST"])
def crear_producto():
    agregar_produco = Producto(codigo_barra = request.form["codigo_barra"], nombre = request.form["nombre"], precio = request.form["precio"])
    db.session.add(agregar_produco)
    db.session.commit()
    db.session.close()
    return redirect(url_for("listar_productos"))

@app.route("/editar/<int:id>")
def editar(id):
    producto = Producto.query.get_or_404(id)
    return render_template("editar_producto.html", producto = producto)

@app.route("/editar_producto/<int:id>", methods=["POST"])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if producto:
        form = request.form        
        producto.codigo_barra = form.get("codigo_barra")
        producto.nombre = form.get("nombre")
        producto.precio = form.get("precio")
        db.session.commit()
        db.session.close()
    return redirect(url_for("listar_productos"))

@app.route("/eliminar_producto/<int:id>")
def eliminar_producto(id):
    Producto.query.filter_by(id = id).delete()
    db.session.commit()
    db.session.close()
    return redirect(url_for("listar_productos"))

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug = True)


