from flask import Flask, request
from variables import conexion
from models.usuario import UsuarioModel # apesar que no estemos usando el UsuarioModel, es necesario importarlo para que se cree la tabla en la base de datos
from models.direcciones import DireccionModel # apesar que no estemos usando el DireccionModel, es necesario importarlo para que se cree la tabla en la base de datos
from flask_migrate import Migrate
from datetime import datetime


app = Flask(__name__)
#print(app.config)
# el app.config almacenara todas las variables de configuracion de la aplicacion
# aca inicializamos la conexion a la base de datos
# al moneto de pasar la aplicacion de flask en esta se encontraras la cadena de coneccion a la BD

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ROOT@localhost:3306/alumnos_bd'

# esta es la cadena de coneccion a la base de datos
conexion.init_app(app)


#Migrate sirve para cokear la base de datos con la aplicacion
Migrate(app=app, db=conexion)

#  before_request se ejecuta antes de cada peticion
# en este caso se ejecutara antes de cada peticion para inicializar la base de datos
#@app.before_request
#def inicializacion():
    #conexion.create_all()
    # create_all crea todas la stablas que no se an creado en la base de datos

@app.route('/usuarios', methods=['GET'])
def destionarUsuarios():
    # creamos una sesion con Conexion 
    resultado = conexion.session.query(UsuarioModel).all()
    # con el metodo all() obtenemos todos los usuarios de la base de datos  
    usuarios = []
    # recorremos los usuarios y los agregamos a la lista de usuarios
    # cada usuario es un diccionario con los campos id, nombre, apellido, correo, sexo y fechaNacimiento
    # el id es el id del usuario, el nombre es el nombre del usuario, el apellido es el apellido del usuario, el correo es el correo del usuario, el sexo es el sexo del usuario y la fechaNacimiento es la fecha de nacimiento del usuario
    # el resultado es una lista de objetos UsuarioModel, por lo que debemos recorrerla y convertirla a diccionarios
    for usuario in resultado:
        usuarios.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'correo': usuario.correo,
            'sexo': usuario.sexo,
            'fechaNacimiento': datetime.strftime(usuario.fechaNacimiento, '%Y-%m-%d') # convertimos la fecha de nacimiento a un string con el formato YYYY-MM-DD
            # si quisieramos la hora tambien, podriamos usar '%H:%M:%S'
        })
    #print(usuarios)

    return {
        'content': usuarios
    }, 200

# decorador para crear un endpoint que recibe un usuario y lo crea en la base de datos
@app.route('/usuario', methods=['POST'])
def crearUsuario():
    # primero capturamos la informacion con el metodo request.get_json()
    data = request.get_json()
    nuevoUsuario = UsuarioModel(nombre = data.get('nombre'),
                                apellido = data.get('apellido'),
                                correo = data.get('correo'),
                                sexo = data.get('sexo'),
                                fechaNacimiento = data.get('fechaNacimiento'))
    # creamos un nuevo usuario con los datos que nos llegan del cliente
    conexion.session.add(nuevoUsuario)
    print('Antes del commit',nuevoUsuario.id)
    # agregamos el nuevo usuario a la sesion de la base de datos
    # esto no lo guarda en la base de datos, solo lo agrega a la sesion
    conexion.session.commit()
    print('despues del commit',nuevoUsuario.id)

    return{
        'message': 'Usuario creado correctamente',
    }, 201

#########################  1:38 #########################


@app.route('/')
def inicical():
    return{
        'message': 'Bienvenido a la API de Usuarios'
    }



if __name__ == '__main__':
    app.run(debug=True)
