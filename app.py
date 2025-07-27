from flask import Flask, request
from variables import conexion
from models.usuario import UsuarioModel # apesar que no estemos usando el UsuarioModel, es necesario importarlo para que se cree la tabla en la base de datos
from models.direcciones import DireccionModel # apesar que no estemos usando el DireccionModel, es necesario importarlo para que se cree la tabla en la base de datos
from flask_migrate import Migrate
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


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


class UsuarioDTO(Schema):
    nombre = fields.Str(required=True)  # hace la validacion que cumpla con el patron que corresponde al nombre
    apellido = fields.Str()
    correo = fields.Email(required=True)  # hace la validacion que cumpla con el patron que corresponde al correo 
    fechaNacimiento = fields.Date() # hace la validacion que cumpla con el patron que corresponde a la fecha
    sexo = fields.Str()

class UsuarioModelDto(SQLAlchemyAutoSchema):
    class Meta:
        # este model sirve para indicar desde que modelo se va a jalar toda la configuracion de nuestro DTO
        # en base a las columnas seteara las configuraciones de los Modelos y toda la configuracion de las tablas
        model = UsuarioModel
        



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
    validador = UsuarioModelDto(many=True)  # inicializamos el validador con el modelo de datos que queremos validar
    # con el metodo all() obtenemos todos los usuarios de la base de datos  
    usuarios = validador.dump(resultado)  # usamos el metodo dump del validador para convertir la lista de objetos UsuarioModel a una lista de diccionarios
    # usuarios = []
    # # recorremos los usuarios y los agregamos a la lista de usuarios
    # # cada usuario es un diccionario con los campos id, nombre, apellido, correo, sexo y fechaNacimiento
    # # el id es el id del usuario, el nombre es el nombre del usuario, el apellido es el apellido del usuario, el correo es el correo del usuario, el sexo es el sexo del usuario y la fechaNacimiento es la fecha de nacimiento del usuario
    # # el resultado es una lista de objetos UsuarioModel, por lo que debemos recorrerla y convertirla a diccionarios
    # for usuario in resultado:
    #     usuarios.append({
    #         'id': usuario.id,
    #         'nombre': usuario.nombre,
    #         'apellido': usuario.apellido,
    #         'correo': usuario.correo,
    #         'sexo': usuario.sexo,
    #         'fechaNacimiento': datetime.strftime(usuario.fechaNacimiento, '%Y-%m-%d') # convertimos la fecha de nacimiento a un string con el formato YYYY-MM-DD
    #         # si quisieramos la hora tambien, podriamos usar '%H:%M:%S'
    #     })
    # #print(usuarios)

    return {
        'content': usuarios  # usamos el metodo dump del validador para convertir la lista de objetos UsuarioModel a una lista de diccionarios
    }, 200

# decorador para crear un endpoint que recibe un usuario y lo crea en la base de datos
@app.route('/usuario', methods=['POST'])
def crearUsuario():
    try:
        # primero capturamos la informacion con el metodo request.get_json()
        data = request.get_json()
        # si la informaicon es incorecta nos envia un error 400
        #validador = UsuarioDTO()
        validador = UsuarioModelDto()  # inicializamos el validador con el modelo de datos que queremos validar
        # usamos el validador para validar los datos que nos llegan del cliente
        # validamos los datos que nos llegan del cliente
        dataValidada = validador. load(data) # si los datos no son validos, lanzara una excepcion load sirve para validar los datos que nos llegan del cliente
        # si los datos no son validos, lanzara una excepcion



        nuevoUsuario = UsuarioModel(**dataValidada)  # usamos el operador ** para desempaquetar el diccionario data y pasarlo como argumentos al constructor de UsuarioModel
        # de esta forma podemos crear un nuevo usuario con los datos que nos llegan del cliente

# de esta forma podemos crear un nuevo usuario con los datos que nos llegan del cliente en datos fijos 
# nuevoUsuario = UsuarioModel(nombre = data.get('nombre'),
#                            apellido = data.get('apellido'),
#                           correo = data.get('correo'),
#                          sexo = data.get('sexo'),
#                         fechaNacimiento = data.get('fechaNacimiento'))
        # creamos un nuevo usuario con los datos que nos llegan del cliente
        conexion.session.add(nuevoUsuario)
        print('Antes del commit',nuevoUsuario.id)
        # agregamos el nuevo usuario a la sesion de la base de datos
        # esto no lo guarda en la base de datos, solo lo agrega a la sesion
        conexion.session.commit()
        print('despues del commit',nuevoUsuario.id)

        # usuarioCreado es un diccionario que contiene los datos del usuario creado
        # usamos datetime.strftime para convertir la fecha de nacimiento a un string con el formato YYYY-MM-DD
        # esto es necesario porque la fecha de nacimiento es un objeto datetime y queremos enviarla como un string
        # si no lo hacemos, Flask no sabe como serializar el objeto datetime a JSON

        usuarioCreado = validador.dump(nuevoUsuario)  # usamos el metodo dump del validador para convertir el objeto UsuarioModel a un diccionario
        #usuarioCreado = UsuarioModelDto().dump(nuevoUsuario)  # usamos el metodo dump del validador para convertir el objeto UsuarioModel a un diccionario
        # el metodo dump convierte el objeto UsuarioModel a un diccionario con los campos id, nombre, apellido, correo, sexo y fechaNacimiento
        # el id es el id del usuario, el nombre es el nombre del usuario, el apellido es el apellido del usuario, el correo es el correo del usuario, el sexo es el sexo del usuario y la fecha de nacimiento es la fecha de nacimiento del usuario

        # usuarioCreado= {
        #     'id': nuevoUsuario.id,
        #     'nombre': nuevoUsuario.nombre,
        #     'apellido': nuevoUsuario.apellido,   
        #     'correo': nuevoUsuario.correo,
        #     'sexo': nuevoUsuario.sexo,
        #     'fechaNacimiento': datetime.strftime(nuevoUsuario.fechaNacimiento, '%Y-%m-%d')
        # }
    
        return{
            'message': 'Usuario creado correctamente',
            'content':usuarioCreado
        }, 201
    except Exception as error:
        # si ocurre un error, hacemos un rollback para deshacer los cambios
        return{
            'message': 'Error al crear el usuario',
            'content': error.args
        }, 500


@app.route('/usuario/<int:id>', methods=['GET', 'UPDATE'])
def destionarUsuario(id):
    if request.method == 'GET':     

        usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(id = id).first()# el metodo filter_by nos permite filtrar los resultados de la consulta
        # usamos el metodo first() para obtener el primer resultado de la consulta
        if usuarioEncontrado is None:
            return{
                'message': 'Usuario no existente',
            }, 404

        serializador = UsuarioModelDto()
        resultado = serializador.dump(usuarioEncontrado)
        return{
            'content': resultado
        }, 200
    elif request.method == 'PUT':
        usuarioEncontrado =  conexion.session.query(UsuarioModel).with_entities(UsuarioModel.id).filter_by(id = id).first() # con este metodo verificamos si el usuario existe
        if usuarioEncontrado is None:
            return{
                'message': 'Usuario no existente',
            }, 404


@app.route('/')
def inicical():
    return{
        'message': 'Bienvenido a la API de Usuarios'
    }



if __name__ == '__main__':
    app.run(debug=True)
