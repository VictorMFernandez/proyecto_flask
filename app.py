from flask import Flask, request
from variables import conexion
from models.usuario import UsuarioModel # apesar que no estemos usando el UsuarioModel, es necesario importarlo para que se cree la tabla en la base de datos
from models.direcciones import DireccionModel # apesar que no estemos usando el DireccionModel, es necesario importarlo para que se cree la tabla en la base de datos

app = Flask(__name__)
#print(app.config)
# el app.config almacenara todas las variables de configuracion de la aplicacion
# aca inicializamos la conexion a la base de datos
# al moneto de pasar la aplicacion de flask en esta se encontraras la cadena de coneccion a la BD

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ROOT@localhost:3306/alumnos_bd'

# esta es la cadena de coneccion a la base de datos
conexion.init_app(app)


#  before_request se ejecuta antes de cada peticion
# en este caso se ejecutara antes de cada peticion para inicializar la base de datos
@app.before_request
def inicializacion():
    conexion.create_all()
    # create_all crea todas la stablas que no se an creado en la base de datos

@app.route('/')
def inicical():
    return{
        'message': 'Bienvenido a la API de Usuarios'
    }



if __name__ == '__main__':
    app.run(debug=True)

