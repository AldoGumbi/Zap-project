#-----------   A D M I N I S T R A C I O N     -----------



from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_mysqldb import MySQL
from app import app,mysql




@app.route('/Index_Administracion')
def Index_Administracion():
    cur =  mysql.connection.cursor()
    cur.execute("""SELECT 
    empleado.Id_Empleado,empleado.Nombre,empleado.ApellidoP,empleado.ApellidoM,
    empleado.Domicilio,empleado.Ciudad,empleado.Estado,empleado.Telefono,
    empleado.Numero_Seguro, empleado.RFC,puesto_departamento.Nombre_Puesto,empleado.Correo
    from empleado inner join puesto_departamento on empleado.Puesto=puesto_departamento.Id_PD;""")
    datos_E =cur.fetchall()
    cur.execute("""SELECT * from cliente ORDER BY Id_Cliente DESC """)
    datos_C =cur.fetchall()
    dep=cur.execute("SELECT Id_PD,Nombre_Puesto from puesto_departamento ORDER BY Id_PD ASC")
    dep=cur.fetchall()
    cur.execute("SELECT count(Id_Empleado) from empleado ")
    total_E=cur.fetchall()
    cur.execute("SELECT count(Id_Cliente) from cliente")
    total_C=cur.fetchall()
    
    return render_template('/plataformas/index_administracion.html', 
                           empleados = datos_E, clientes=datos_C,deps=dep, total_E=total_E[0],total_C=total_C[0])



@app.route('/add_empleado', methods=['POST'])
def add_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoP']
        apellidoM = request.form['apellidoM']
        domicilio = request.form['domicilio']
        ciudad = request.form['ciudad']
        estado = request.form['estado']
        telefono=request.form['telefono']
        nss = request.form['nss']
        rfc = request.form['rfc']
        puesto = request.form['puesto']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        cur =  mysql.connection.cursor()

        cur.execute("""INSERT INTO empleado (Nombre,ApellidoP,ApellidoM,Domicilio,Ciudad,Estado, Telefono,Numero_Seguro,RFC,Puesto,Correo,Contrasenia)
                    VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s)""",
                    (nombre, apellidoP,apellidoM,domicilio,ciudad,estado,telefono,nss,rfc,puesto,correo,contrasena))
        mysql.connection.commit()
        flash('Empleado Guardado')
        return redirect(url_for('Index_Administracion'))
    
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
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
        cur =  mysql.connection.cursor()

        cur.execute("""INSERT INTO cliente (Nombre,ApellidoP,ApellidoM,Domicilio,Ciudad,Estado, Telefono,Correo,Contrasenia)
                    VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)""",
                    (nombre, apellidoP,apellidoM,domicilio,ciudad,estado,telefono,correo,contrasena))
        mysql.connection.commit()
        flash('Cliente Guardado')
        return redirect(url_for('Index_Administracion'))
        
 

@app.route('/edit_empleado/<id>')
def get_empleado(id):
    cur =  mysql.connection.cursor()
    cur.execute('SELECT * FROM empleado WHERE Id_empleado= %s and Id_empleado !=1'% (id))
    data= cur.fetchall()
    print(data)
    return render_template('/plataformas/includes/edit_empleado.html', empleado=data[0])


@app.route('/edit_cliente/<id>')
def edit_cliente(id):
    cur =  mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE Id_Cliente=%s'% (id))
    data= cur.fetchall()
    print(data)
    return render_template('/plataformas/includes/edit_cliente.html', clientes=data[0])



@app.route('/update_empleado/<id>', methods=['POST'])
def update_empleado(id):
     cur =  mysql.connection.cursor()
     if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoP']
        apellidoM = request.form['apellidoM']
        domicilio = request.form['domicilio']
        ciudad = request.form['ciudad']
        estado = request.form['estado']
        telefono=request.form['telefono']
        nss = request.form['nss']
        rfc = request.form['rfc']
        puesto = request.form['puesto']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        cur.execute("""UPDATE empleado SET 
        Nombre=%s,
        ApellidoP=%s,
        ApellidoM=%s,
        Domicilio=%s,
        Ciudad=%s,
        Estado=%s,
        Telefono=%s,
        Numero_Seguro=%s,
        RFC=%s,
        Puesto=%s,
        Correo=%s,
        Contrasenia=%s
        where Id_empleado=%s
        """  ,(nombre, apellidoP,apellidoM,domicilio,ciudad,estado,telefono,nss,rfc,puesto,correo,contrasena,id))
        mysql.connection.commit()
        flash('Empleado Actualizado')
        return redirect(url_for('Index_Administracion'))
     

@app.route('/update_cliente/<id>', methods=['POST'])
def update_cliente(id):
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
        return redirect(url_for('Index_Administracion'))
     



@app.route('/delete_empleado/<string:id>')
def delete_empleado(id):
    cur =  mysql.connection.cursor()
    cur.execute('DELETE FROM empleado WHERE Id_empleado= {0}'.format(id))
    mysql.connection.commit()
    flash('Empleado Eliminado')
    return redirect(url_for('Index_Administracion'))


@app.route('/delete_cliente/<string:id>')
def delete_cliente(id):
    cur =  mysql.connection.cursor()
    cur.execute('DELETE FROM cliente WHERE Id_cliente= {0}'.format(id))
    mysql.connection.commit()
    flash('Cliente Eliminado')
    return redirect(url_for('Index_Administracion'))
    


    





app.secret_key='mysecretkey'





if __name__=='__main__':
    app.run(port=3000,debug=True)