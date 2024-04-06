
from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_mysqldb import MySQL



app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='AldoAdmin'
app.config['MYSQL_PASSWORD']='habitacion11'
app.config['MYSQL_DB']='zapateria'
mysql= MySQL(app)

app.secret_key='mysecretkey'
@app.route('/Index')
def Index():
    cur =  mysql.connection.cursor()
    #cur.execute('SELECT * from producto')
    #data =cur.fetchall()
    return render_template('index.html')


@app.route('/ingresa_cliente', methods=['POST'])
def ingresa_cliente():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        cur =  mysql.connection.cursor()
        cur.execute('SELECT Id_Cliente from cliente where Correo= %s and Contrasenia=%s',(correo, contrasena))
        data =cur.fetchall()
        global pedido
        mysql.connection.commit()
        if data!=0:
              cur.execute("INSERT INTO pedido_cliente (Id_Cliente) VALUES (%s);",( data))
              mysql.connection.commit()
              cur.execute('SELECT Id_PC from pedido_cliente WHERE Id_Cliente=%s ORDER BY Id_PC DESC LIMIT 1;',(data))
              pedido=cur.fetchone()
              return redirect(url_for('Producto_Inicio', pedido=pedido[0], cliente=data))
        flash("  Error: Usuario Incorrecto  ")
        return redirect(url_for('Index'))
    

@app.route('/ingresa_empleado', methods=['POST'])
def ingresa_empleado():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        cur =  mysql.connection.cursor()
        cur.execute('SELECT Puesto,Id_empleado from empleado where Correo= %s and Contrasenia=%s',(correo, contrasena))
        ad=['13','14','15','16','41','42']
        al=['21','22', '23','24','31','32', '33']
        ec=['11','12','51','52', '53','54']
        pv=['15','61','62', '63','64','65','66']
        data = cur.fetchone()
        print(data)
        mysql.connection.commit()
        if data[0] in al:
             return redirect(url_for('Index_Producto'))
        elif data[0] in ad:
             return redirect(url_for('Index_Administracion'))
        elif data[0] in ec:
             return redirect(url_for('Index_Ecommerce'))
        elif data[0] in pv:
             return redirect(url_for('Producto_Inicio'))
    
        else:
            flash("  Error: Empleado Incorrecto  ")
            return redirect(url_for('Index'))

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoP']
        apellidoM = request.form['apellidoM']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        cur =  mysql.connection.cursor()
        cur.execute("""INSERT INTO cliente (Nombre, ApellidoP, ApellidoM, Correo, Contrasenia) 
                    VALUES (%s, %s, %s, %s,%s)""",
                    (nombre, apellidoP, apellidoM, correo, contrasena))
        mysql.connection.commit()
        cur.execute("SELECT * from cliente ORDER BY Id_Cliente DESC")
        clientes=cur.fetchall()
        return render_template('/plataformas/includes/perfil.html',clientes=clientes[0])
    
@app.route('/save_cliente/<id>', methods=['POST'])
def save_cliente(id):
     cur =  mysql.connection.cursor()
     if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoP']
        apellidoM = request.form['apellidoM']
        domicilio = request.form['domicilio']
        ciudad = request.form['ciudad']
        estado = request.form['estado']
        telefono=request.form['telefono']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        cur.execute("""UPDATE cliente SET 
        Nombre=%s,
        ApellidoP=%s,
        ApellidoM=%s,
        Domicilio=%s,
        Ciudad=%s,
        Estado=%s,
        Telefono=%s,
        Correo=%s,
        Contrasenia=%s
        where Id_cliente=%s
        """  ,(nombre, apellidoP,apellidoM,domicilio,ciudad,estado,telefono,correo,contrasena,id))
        mysql.connection.commit()
        flash('Cliente Actualizado')
        cur.execute('SELECT Id_Cliente from cliente where Correo= %s and Contrasenia=%s',(correo, contrasena))
        data =cur.fetchall()
        global pedido
        mysql.connection.commit()
        if data!=0:
              cur.execute("INSERT INTO pedido_cliente (Id_Cliente) VALUES (%s);",( data))
              mysql.connection.commit()
              cur.execute('SELECT Id_PC from pedido_cliente WHERE Id_Cliente=%s ORDER BY Id_PC DESC LIMIT 1;',(data))
              pedido=cur.fetchone()
              return redirect(url_for('Producto_Inicio', pedido=pedido[0], cliente=data))
            
@app.route('/perfil/<cliente>')
def perfil(cliente):
        cur =  mysql.connection.cursor()
        cur.execute("SELECT * from cliente WHERE Id_cliente=(SELECT Id_cliente from pedido_cliente where Id_PC={0})".format(cliente))
        clientes=cur.fetchall()
        return render_template('/plataformas/includes/perfil.html',clientes=clientes[0], pedido=cliente)

from archivosPY.inventario import*
from archivosPY.inicio import*
from archivosPY.ecomerce import*
from archivosPY.admin import*

if __name__=='__main__':
    app.run(port=3000,debug=True)


