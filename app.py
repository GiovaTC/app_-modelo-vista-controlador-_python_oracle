from flask import Flask, render_template, request, redirect, url_for, flash
import models

app = Flask(__name__)
app.secret_key = 'cambiar_por_una_clave_segura'

@app.route('/')
def index():
    pacientes = models.list_pacientes()
    return render_template('index.html', pacientes = pacientes)

@app.route('/paciente/nuevo', methods=['GET', 'POST'])
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
        flash('paciente creado correctamente')
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/paciente/editar/<int:p_id>', methods=['GET, POST'])
def editar_paciente(p_id):
    paciente = models.get_paciente(p_id)
    if not paciente:
        flash('paciente no encontrado')
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
        flash('paciente actualizado')
        return redirect(url_for('index'))
    return render_template('edit.html', paciente= paciente)

@app.route('/paciente/eliminar/<int:p_id>', methods=['POST'])
def eliminar_paciente(p_id):
    models.delete_paciente(p_id)
    flash('paciente eliminado')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)