#-----------   I N I C I O   Cliente-Empleado -----------


from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_mysqldb import MySQL
from app import app,mysql

@app.route('/Index_Inicio')
def Index_Inicio():
    cur =  mysql.connection.cursor()
    return render_template('/index.html')

@app.route('/Index_Carrito')
def Index_Carrito():
    cur =  mysql.connection.cursor()

    return render_template('/plataformas/includes/carrito.html')

@app.route('/Index_cliente')
def Index_cliente():
    cur =  mysql.connection.cursor()

    return render_template('/plataformas/index_inicio.html')


@app.route('/Producto_Inicio/<pedido>')
def Producto_Inicio(pedido):

    cur =  mysql.connection.cursor()
    cur.execute('SELECT DISTINCT Modelo,Descripcion,Precio,Imagen  from producto')
    data =cur.fetchall()
    global Pedido
    Pedido=pedido
    print('pedido ===== ',data[1], '\n\n',data[2])
    return render_template('/plataformas/index_inicio.html', productos = data, pedido=pedido)


@app.route('/agrega_producto/<modelo>/<pedido>',methods=['POST'])
def agrega_producto(modelo,pedido):
     talla = request.form['Talla']
     cur =  mysql.connection.cursor()
     cur.execute('SELECT Id_Producto, Precio from producto where Modelo=%s and Talla=%s;',(modelo, talla))
     producto=cur.fetchone()
     cur.execute('SELECT * from carrito_cliente where Id_producto=%s and Pedido=%s',(producto[0],pedido))
     condicion_producto=cur.fetchall()
     if condicion_producto:
            cur.execute('UPDATE carrito_cliente SET Cantidad=Cantidad+1 where Pedido=%s and Id_Producto=%s',(pedido,producto[0]))
     else:
            cur.execute("""INSERT INTO carrito_cliente(Pedido,Id_Producto,Precio_Producto,Cantidad) 
                        VALUES (%s,%s,%s,%s);""",(pedido,producto[0],producto[1],1))

     mysql.connection.commit()
     return Producto_Inicio(pedido)



@app.route('/carrito/<pedido>')
def carrito(pedido):
     
     cur =  mysql.connection.cursor()
     cur.execute(""" SELECT * from producto where Id_Producto in 
     (SELECT Id_Producto from carrito_cliente where Pedido= {0} );
     """.format(pedido))

     data= cur.fetchall()
     if bool(data)==False:
            print('')
     cur.execute('SELECT Cantidad,Importe from carrito_cliente where Pedido={0}'.format(pedido))
     can_imp=cur.fetchall()
     print(data)
     datos=[a + b for a, b in zip(data, can_imp)]
     
     cur.execute('SELECT SUM(Cantidad) FROM carrito_cliente where Pedido={0};'.format(pedido))
     cantidad_total=cur.fetchone()

     cur.execute('SELECT SUM(Importe) FROM carrito_cliente where Pedido={0};'.format(pedido))
     total=cur.fetchone()

     cur.execute('SELECT * from cliente where Id_cliente=(SELECT Id_cliente from pedido_cliente where Id_PC={0});'.format(pedido))
     cliente=cur.fetchall()

     return render_template('/plataformas/includes/carrito.html', 
                            productos = datos, pedido=pedido, cantidad=can_imp, cant=cantidad_total[0], total=total[0],cliente=cliente[0])



@app.route('/delete_producto_pedido/<string:id>/<pedido>')
def delete_producto_pedido(id,pedido):
    cur =  mysql.connection.cursor()
    cur.execute("""DELETE FROM carrito_cliente 
                WHERE Id_Producto= {0} and Pedido={1}""".format(id,pedido))
    mysql.connection.commit()
    return redirect(url_for('carrito',pedido=pedido))
    
@app.route('/edit_cant/<producto>/<pedido>',methods=['POST'])
def edit_cant(producto,pedido):
    cur =  mysql.connection.cursor()
    cantidad = request.form['unidades']
    cur.execute("UPDATE carrito_cliente SET Cantidad=%s WHERE Pedido=%s and Id_Producto=%s",(cantidad, pedido,producto))
    mysql.connection.commit()
    return redirect(url_for('carrito',pedido=pedido))

@app.route('/vaciar_carrito/<pedido>')
def vaciar_carrito(pedido):
    cur =  mysql.connection.cursor()
    cur.execute("DELETE FROM carrito_cliente WHERE Pedido={0}".format(pedido))
    mysql.connection.commit()
    return redirect(url_for('carrito',pedido=pedido))

@app.route('/salir/<pedido>')
def salir(pedido):
    cur =  mysql.connection.cursor()
    cur.execute("SELECT * FROM carrito_cliente WHERE NOT Pedido != {0} ;".format(pedido))
    datos=cur.fetchall()
    if bool(datos) == False:
         cur.execute('DELETE FROM pedido_cliente WHERE Id_PC={0};'.format(pedido))
         mysql.connection.commit()
    
    return redirect(url_for('Index_Inicio'))

@app.route('/finalizar_pedido/<pedido>/<total>/<cliente>',methods=['POST'])
def finalizar_pedido(pedido,total,cliente):
    cur =  mysql.connection.cursor()
    entrega = request.form['entrega']
    fecha = request.form['fecha']
    pago = request.form['pago']
    
    cur.execute("""UPDATE pedido_cliente SET Metodo_Entrega=%s,Metodo_Pago=%s, Fecha_Entrega=%s
                   WHERE Id_PC=%s""",(entrega,pago,fecha,pedido))
    mysql.connection.commit()
    cur.execute('INSERT INTO pedido_cliente (Id_Cliente) VALUES ({0})'.format(cliente))
    mysql.connection.commit()
    cur.execute('SELECT Id_PC from pedido_cliente WHERE Id_Cliente={0} ORDER BY Id_PC DESC LIMIT 1;'.format(cliente))
    pedido=cur.fetchone()
    return redirect(url_for('Producto_Inicio',pedido=pedido[0]))

app.secret_key='mysecretkey'

if __name__=='__main__':
    app.run(port=3000,debug=True)