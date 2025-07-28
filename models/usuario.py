from sqlalchemy import Column, types
from variables import conexion


#Para indicar que esta clase sera una tabla en la base de datos utilizamos la conexion a la base de datos
class UsuarioModel(conexion.Model):
    id = Column(name='id', 
                type_=types.Integer, 
                autoincrement=True, 
                primary_key=True)
    nombre = Column(type_=types.String(100), nullable=False)
# si no colocamos el parametro name tonces el nombre de la columna sera el mismo que el nombre del atributo
    apellido = Column(type_=types.String(100), nullable=False)
    fechaNacimiento = Column(name='fecha_nacimiento', type_=types.Date,)
    correo = Column(type_=types.String(100), unique=True , nullable=False)
    sexo = Column(type_=types.String(10), server_default='NINGUNO')
    # server_default='1' indica que cuando se agregue un nuevo registro a la tabla, el valor por defecto sera 1 (True)
    # esto es util para indicar que el usuario esta activo por defecto
    #mientras que default=True indica que el valor por defecto sera True
    # si no colocamos el parametro server_default, entonces el valor por defecto sera None
    activo = Column(type_=types.Boolean, server_default='1') # cuando agregamos una nueva columna y la tabla ya existe al utilizar un valor por defecto lo que hara sera colorcar a todos los registros ese valor 
    # para indicar que esta clase es una tabla en la base de datos

# para indicar como queremos que se llame esta tabla en la base de datos
    __tablename__ = 'usuarios'

