#-----------   E M P L E A D O   E - C o m m e r c e     -----------

from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_mysqldb import MySQL
from app import app,mysql




@app.route('/Index_Ecommerce')
def Index_Ecommerce():
    cur =  mysql.connection.cursor()
    cur.execute("SELECT * from cliente_pedido")
    pedidos=cur.fetchall()
    cur.execute("SELECT * from pedido_producto")
    productos=cur.fetchall();
    return render_template('/plataformas/index_ecomerce.html', pedidos=pedidos, productos=productos)

@app.route('/Index_Ecommerce_Nombre')
def Index_Ecommerce_Nombre():
    cur =  mysql.connection.cursor()
    cur.execute("SELECT * from cliente_pedido ORDER BY Nombre ASC")
    pedidos=cur.fetchall()
    cur.execute("SELECT * from pedido_producto ")
    productos=cur.fetchall();
    return render_template('/plataformas/index_ecomerce.html', pedidos=pedidos, productos=productos)

@app.route('/Index_Ecommerce_Fecha')
def Index_Ecommerce_Fecha():
    cur =  mysql.connection.cursor()
    cur.execute("SELECT * from cliente_pedido ORDER BY Fecha_Pedido DESC")
    pedidos=cur.fetchall()
    cur.execute("SELECT * from pedido_producto ")
    productos=cur.fetchall();
    return render_template('/plataformas/index_ecomerce.html', pedidos=pedidos, productos=productos)


@app.route('/mostrar_pedido')
def mostrar_pedido():
    cur =  mysql.connection.cursor()
    cur.execute("SELECT * from cliente_pedido")
    pedidos=cur.fetchall()
    cur.execute("SELECT * from pedido_producto")
    productos=cur.fetchall();
    return render_template('/plataformas/index_ecomerce.html', pedidos=pedidos, productos=productos)

@app.route('/terminar/<pedido>', methods=['POST'])
def terminar_pedido(pedido):
    cur =  mysql.connection.cursor()
    empleado = request.form['empleado']
    envio = request.form['fecha_envio']
    estatus = request.form['estatus']
    cur.execute("SELECT Id_Empleado from empleado where Id_empleado={0}".format(empleado))
    print(pedido,envio,estatus)
    verf_empleado=cur.fetchone()
    if bool(verf_empleado)==False:
        print('FALSE')
        flash('Empleado Incorrecto')
        return redirect(url_for('Index_Ecommerce'))
    else:
        cur.execute("""UPDATE pedido_cliente 
                    SET Fecha_entrega=%s, Atendio=%s, Estatus=%s where Id_PC = %s;""",
                    (envio,empleado[0],estatus,pedido))
        mysql.connection.commit()
        return redirect(url_for('Index_Ecommerce'))




@app.route('/elimina_pedido/<pedido>')
def eliminar_pedido(pedido):
    cur =  mysql.connection.cursor()
    cur.execute("DELETE FROM pedido_cliente WHERE Id_PC={0}".format(pedido))
    mysql.connection.commit()
    return redirect(url_for('Index_Ecommerce'))

@app.route('/busca_pedido',methods=['POST'])
def busca_pedido():
    cur =  mysql.connection.cursor()
    Nombre = request.form['Nombre']
    Fecha = request.form['Fecha']
    Pedido = request.form['Pedido']
    if Nombre!=False:
        cur.execute("SELECT * FROM pedido_cliente WHERE Id_PC =(SELECT Id_PC from cliente_pedido Where Nombre =%s); ")
        pedidos=cur.fetchall()
    return redirect(url_for('Index_Ecommerce'))

@app.route('/completados')
def completado():
    cur =  mysql.connection.cursor()
    cur.execute("SELECT * from pedido_com")
    pedidos=cur.fetchall()
    cur.execute("SELECT * from pedido_producto")
    productos=cur.fetchall();
    return render_template('/plataformas/includes/pedido_completado.html', pedidos=pedidos, productos=productos)



app.secret_key='mysecretkey'


if __name__=='__main__':
    app.run(port=3000,debug=True)