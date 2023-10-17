from flask import Flask,  render_template, request, redirect, url_for, session # pip install Flask
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from os import path #pip install notify-py
from notifypy import Notify


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cardiaco'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("layout.html")    


@app.route('/login', methods= ["GET", "POST"])
def login():

    notificacion = Notify()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user)>0:
            if password == user["password"]:
                session['name'] = user['name']
                session['email'] = user['email']
            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Correo o contraseña no valida"
                notificacion.send()
                return render_template("login.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="No existe el usuario"
            notificacion.send()
            return render_template("login.html")
    else:
        
        return render_template("login.html")



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template("registro.html")
    
    nombre = request.form['nombre_completo']
    cedula = request.form['cedula']
    email = request.form['correo']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (Cedula,Nombre,Correo,Contraseña) VALUES (%s, %s, %s, %s)", (cedula,nombre,email,password))
    mysql.connection.commit()
    
   #notificacion = pb.push_note("Registro Exitoso", "Ya te encuentras registrado")

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(debug=True)