from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/tienda.db'
db = SQLAlchemy(app)

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_barra = db.Column(db.String(250))
    nombre = db.Column(db.String(250))
    precio = db.Column(db.Integer())

@app.route("/")
def main():    
    return render_template("index.html")

@app.route("/productos")
def productos():    
    return render_template("productos.html")

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug = True)


