# app_-modelo-vista-controlador-_python_oracle .

<img width="203" height="193" alt="image" src="https://github.com/user-attachments/assets/acd0ce8a-579d-497b-a76e-797430d0bb13" />

# Aplicación MVC en Python conectada a Oracle .

<img width="2553" height="1079" alt="image" src="https://github.com/user-attachments/assets/70c1a452-c2d5-4c96-ae83-b97cf43540bb" />
<img width="2554" height="1079" alt="image" src="https://github.com/user-attachments/assets/164d15c0-444d-4b5f-98b8-ce431eb5943d" />
<img width="2550" height="1079" alt="image" src="https://github.com/user-attachments/assets/25d86245-6c6a-4724-8bb2-72d8d6170be3" />

Este repositorio de ejemplo muestra una aplicación **Modelo-Vista-Controlador (MVC)** en **Python** usando **Flask** como framework web y **oracledb** 
( la librería oficial que reemplaza a `cx_Oracle`) para conectarse a una base de datos **Oracle** .

---

## 📂 Estructura del proyecto

- mvc_python_oracle/
  - **app.py** → Controller (rutas Flask)
  - **models.py** → Modelo (acceso a Oracle)
  - **config.py** → Configuración (DSN, credenciales)
  - **requirements.txt**
  - **templates/**
    - base.html
    - index.html
    - create.html
    - edit.html
  - **static/** → (opcional: css/js)


---

## ✅ Requisitos
- Python 3.8+
- Paquetes (vea `requirements.txt`)

### requirements.txt .
Flask>=2.0
oracledb>=1.0
python-dotenv

---

## 🗄️ script SQL ( tabla de ejemplo )

```sql
-- Tabla de ejemplo: PACIENTES
CREATE TABLE PACIENTES (
    ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    NOMBRE VARCHAR2(100),
    APELLIDO VARCHAR2(100),
    EDAD NUMBER,
    TELEFONO VARCHAR2(50),
    CORREO VARCHAR2(150)
);

-- Opcionalmente agregar INSERTs de ejemplo según necesite .

⚙️ configuración ( config.py )
python

import os
from dotenv import load_dotenv
load_dotenv()

ORACLE_USER = os.getenv('ORACLE_USER', 'your_user')
ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', 'your_password')

# DSN formato: host:port/service_name -> ejemplo: 127.0.0.1:1521/XEPDB1
ORACLE_DSN = os.getenv('ORACLE_DSN', 'host:1521/servicename')

# opciones de pool
POOL_MIN = int(os.getenv('POOL_MIN', '1'))
POOL_MAX = int(os.getenv('POOL_MAX', '4'))
POOL_INC = int(os.getenv('POOL_INC', '1'))

🛠️ modelo ( models.py )
python

import oracledb
from config import ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN, POOL_MIN, POOL_MAX, POOL_INC

# crear un pool de conexiones
_pool = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN,
            min=POOL_MIN,
            max=POOL_MAX,
            increment=POOL_INC,
            encoding='UTF-8'
        )
    return _pool

# Crud basico para la tabla PACIENTES .

def list_pacientes():
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ID, NOMBRE, APELLIDO, EDAD, TELEFONO, CORREO FROM PACIENTES ORDER BY ID")
            cols = [d[0].lower() for d in cur.description]
            rows = [dict(zip(cols, r)) for r in cur.fetchall()]
            return rows

def get_paciente(p_id):
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ID, NOMBRE, APELLIDO, EDAD, TELEFONO, CORREO FROM PACIENTES WHERE ID = :id", [p_id])
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0].lower() for d in cur.description]
            return dict(zip(cols, row))

def create_paciente(data):
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO PACIENTES (NOMBRE, APELLIDO, EDAD, TELEFONO, CORREO) VALUES (:1, :2, :3, :4, :5)",
                (data.get('nombre'), data.get('apellido'), data.get('edad'),
                 data.get('telefono'), data.get('correo'))
            )
        conn.commit()

def update_paciente(p_id, data):
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE PACIENTES SET NOMBRE=:1, APELLIDO=:2, EDAD=:3, TELEFONO=:4, CORREO=:5 WHERE ID=:6",
                (data.get('nombre'), data.get('apellido'), data.get('edad'),
                 data.get('telefono'), data.get('correo'), p_id)
            )
        conn.commit()

def delete_paciente(p_id):
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM PACIENTES WHERE ID = :id", [p_id])
        conn.commit()

🎮 controlador (app.py)
python

from flask import Flask, render_template, request, redirect, url_for, flash
import models

app = Flask(__name__)
app.secret_key = 'cambiar_por_una_clave_segura'

@app.route('/')
def index():
    pacientes = models.list_pacientes()
    return render_template('index.html', pacientes=pacientes)

@app.route('/paciente/nuevo', methods=['GET','POST'])
def nuevo_paciente():
    if request.method == 'POST':
        data = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'edad': request.form.get('edad'),
            'telefono': request.form.get('telefono'),
            'correo': request.form.get('correo')
        }
        models.create_paciente(data)
        flash('Paciente creado correctamente')
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/paciente/editar/<int:p_id>', methods=['GET','POST'])
def editar_paciente(p_id):
    paciente = models.get_paciente(p_id)
    if not paciente:
        flash('Paciente no encontrado')
        return redirect(url_for('index'))
    if request.method == 'POST':
        data = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'edad': request.form.get('edad'),
            'telefono': request.form.get('telefono'),
            'correo': request.form.get('correo')
        }
        models.update_paciente(p_id, data)
        flash('Paciente actualizado')
        return redirect(url_for('index'))
    return render_template('edit.html', paciente=paciente)

@app.route('/paciente/eliminar/<int:p_id>', methods=['POST'])
def eliminar_paciente(p_id):
    models.delete_paciente(p_id)
    flash('Paciente eliminado')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

🎨 vistas ( templates con Jinja2 )

templates/base.html
html

<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Gestión Pacientes</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="p-4">
<div class="container">
  <h1 class="mb-4">Gestión Pacientes</h1>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <div class="alert alert-info">{{ messages[0] }}</div>
    {% endif %}
  {% endwith %}
  {% block content %}{% endblock %}
</div>
</body>
</html>

templates/index.html

{% extends 'base.html' %}
{% block content %}
<a class="btn btn-primary mb-3" href="{{ url_for('nuevo_paciente') }}">Nuevo Paciente</a>
<table class="table table-striped">
  <thead>
    <tr><th>ID</th><th>Nombre</th><th>Apellido</th><th>Edad</th><th>Teléfono</th><th>Correo</th><th>Acciones</th></tr>
  </thead>
  <tbody>
    {% for p in pacientes %}
    <tr>
      <td>{{ p.id }}</td>
      <td>{{ p.nombre }}</td>
      <td>{{ p.apellido }}</td>
      <td>{{ p.edad }}</td>
      <td>{{ p.telefono }}</td>
      <td>{{ p.correo }}</td>
      <td>
        <a class="btn btn-sm btn-secondary" href="{{ url_for('editar_paciente', p_id=p.id) }}">Editar</a>
        <form method="post" action="{{ url_for('eliminar_paciente', p_id=p.id) }}" style="display:inline" onsubmit="return confirm('Eliminar?')">
          <button class="btn btn-sm btn-danger">Eliminar</button>
        </form>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}

templates/create.html

{% extends 'base.html' %}
{% block content %}
<form method="post">
  <div class="mb-3">
    <label class="form-label">Nombre</label>
    <input class="form-control" name="nombre" required>
  </div>
  <div class="mb-3">
    <label class="form-label">Apellido</label>
    <input class="form-control" name="apellido">
  </div>
  <div class="mb-3">
    <label class="form-label">Edad</label>
    <input type="number" class="form-control" name="edad">
  </div>
  <div class="mb-3">
    <label class="form-label">Teléfono</label>
    <input class="form-control" name="telefono">
  </div>
  <div class="mb-3">
    <label class="form-label">Correo</label>
    <input type="email" class="form-control" name="correo">
  </div>
  <button class="btn btn-primary">Crear</button>
  <a class="btn btn-secondary" href="{{ url_for('index') }}">Cancelar</a>
</form>
{% endblock %}

templates/edit.html

{% extends 'base.html' %}
{% block content %}
<form method="post">
  <div class="mb-3">
    <label class="form-label">Nombre</label>
    <input class="form-control" name="nombre" value="{{ paciente.nombre }}" required>
  </div>
  <div class="mb-3">
    <label class="form-label">Apellido</label>
    <input class="form-control" name="apellido" value="{{ paciente.apellido }}">
  </div>
  <div class="mb-3">
    <label class="form-label">Edad</label>
    <input type="number" class="form-control" name="edad" value="{{ paciente.edad }}">
  </div>
  <div class="mb-3">
    <label class="form-label">Teléfono</label>
    <input class="form-control" name="telefono" value="{{ paciente.telefono }}">
  </div>
  <div class="mb-3">
    <label class="form-label">Correo</label>
    <input type="email" class="form-control" name="correo" value="{{ paciente.correo }}">
  </div>
  <button class="btn btn-primary">Guardar</button>
  <a class="btn btn-secondary" href="{{ url_for('index') }}">Cancelar</a>
</form>
{% endblock %}

🚀 Pasos para ejecutar
crear un entorno virtual e instalar dependencias :

bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt

Configurar variables de entorno (usar .env o exportar) :
ORACLE_USER=tu_usuario
ORACLE_PASSWORD=tu_password
ORACLE_DSN=host:1521/servicename
crear la tabla PACIENTES en Oracle con el script proporcionado .

Ejecutar la app:

bash
python app.py

Abrir en el navegador:
http://127.0.0.1:5000
