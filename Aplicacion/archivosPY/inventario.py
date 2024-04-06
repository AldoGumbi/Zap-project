#-----------   I N V E N T A R I O S    -----------

from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_mysqldb import MySQL
from app import app,mysql




@app.route('/Index_Producto')
def Index_Producto():
    cur =  mysql.connection.cursor()
    cur.execute('SELECT * from producto ORDER BY Id_Producto ASC')
    data =cur.fetchall()
    return render_template('/plataformas/index_producto.html', productos = data)

app.secret_key='mysecretkey'

@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        descripcion = request.form['descripcion']
        talla = request.form['talla']
        color = request.form['color']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        categoria = request.form['categoria']
        cur =  mysql.connection.cursor()

        cur.execute("""INSERT INTO producto (Modelo, Marca, Descripcion, Talla, Color, Precio, Cantidad_P, Categoria) 
                    VALUES (%s, %s, %s, %s,%s, %s, %s, %s)""",
                    (modelo, marca, descripcion, talla, color, precio,cantidad, categoria))
        mysql.connection.commit()
        flash('Producto Guardado')
        return redirect(url_for('Index_Producto'))
        
 

@app.route('/edit_producto/<id>')
def get_producto(id):
    cur =  mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE Id_Producto= %s' % (id))
    data= cur.fetchall()
    return render_template('/plataformas/includes/edit_producto.html', producto=data[0])

@app.route('/update_producto/<id>', methods=['POST'])
def update_producto(id):
     cur =  mysql.connection.cursor()
     if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        descripcion = request.form['descripcion']
        talla = request.form['talla']
        color = request.form['color']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        categoria = request.form['categoria']
        imagen = request.form['imagen']
        cur.execute("""UPDATE producto SET 
        Modelo=%s, 
        Marca=%s, 
        Descripcion=%s, 
        Talla=%s, 
        Color=%s, 
        Precio=%s, 
        Cantidad_P=%s, 
        Categoria=%s,
        Imagen=%s where Id_Producto=%s
        """  ,(modelo, marca, descripcion, talla, color, precio,cantidad, categoria,imagen,id))
        mysql.connection.commit()
        flash('Producto Actualizado')
        return redirect(url_for('Index_Producto'))

@app.route('/delete_producto/<string:id>')
def delete_producto(id):
    cur =  mysql.connection.cursor()
    cur.execute('DELETE FROM producto WHERE Id_Producto= {0}'.format(id))
    mysql.connection.commit()
    flash('Producto Eliminado')
    return redirect(url_for('Index_Producto'))
    



@app.route('/update_cant', methods=['POST'])
def update_cant():
    if request.method == 'POST':
        codigo = request.form['codigo']
        cantidad = request.form['cantidad']
        cur =  mysql.connection.cursor()
        cur.execute("""UPDATE producto SET Cantidad_P=%s WHERE Id_Producto= %s;""",
                    (cantidad,codigo ))
        mysql.connection.commit()
        flash('Producto Guardado')
        return redirect(url_for('Index_Producto'))
    



if __name__=='__main__':
    app.run(port=3000,debug=True)