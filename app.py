# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Configuración de la base de datos desde .env
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip()

        if len(nombre) < 3:
            flash('El nombre debe tener al menos 3 caracteres.', 'error')
        elif not correo or '@' not in correo:
            flash('Correo electrónico inválido.', 'error')
        else:
            try:
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO contactos (nombre, correo, telefono) VALUES (%s, %s, %s)",
                        (nombre, correo, telefono if telefono else None)
                    )
                conn.commit()
                conn.close()
                flash('Contacto guardado correctamente.', 'success')
                return redirect(url_for('index'))
            except pymysql.err.IntegrityError:
                flash('El correo electrónico ya está registrado.', 'error')
            except Exception as e:
                flash(f'Error al guardar el contacto: {str(e)}', 'error')

    return render_template('index.html')

@app.route('/contacts')
def contacts():
    contactos = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT nombre, correo, telefono, fecha_registro
                FROM contactos
                WHERE eliminado_logico=0
                ORDER BY fecha_registro DESC
            """)
            contactos = cursor.fetchall()
        conn.close()
    except Exception as e:
        flash(f'Error al obtener los contactos: {str(e)}', 'error')

    return render_template('contacts.html', contactos=contactos)

@app.route('/delete/<correo>', methods=['POST'])
def delete_contact(correo):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE contactos SET eliminado_logico=1 WHERE correo=%s", (correo,))
        conn.commit()
        conn.close()
        flash('Contacto eliminado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el contacto: {str(e)}', 'error')

    return redirect(url_for('contacts'))

@app.route('/edit/<correo>', methods=['GET', 'POST'])
def edit_contact(correo):
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        telefono = request.form.get('telefono', '').strip()

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("UPDATE contactos SET nombre=%s, telefono=%s WHERE correo=%s",
                               (nombre, telefono, correo))
            conn.commit()
            conn.close()
            flash('Contacto editado correctamente.', 'success')
            return redirect(url_for('contacts'))
        except Exception as e:
            flash(f'Error al editar el contacto: {str(e)}', 'error')

    else:
        contacto = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT nombre, correo, telefono
                    FROM contactos
                    WHERE correo=%s AND eliminado_logico=0
                """, (correo,))
                contacto = cursor.fetchone()
            conn.close()
        except Exception as e:
            flash(f'Error al obtener el contacto: {str(e)}', 'error')

        if not contacto:
            flash('Contacto no encontrado.', 'error')
            return redirect(url_for('contacts'))

        return render_template('edit_contact.html', contacto=contacto)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
