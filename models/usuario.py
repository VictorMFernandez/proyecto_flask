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
    correo = Column(type_=types.String(100), unique=True)
    sexo = Column(type_=types.String(10), nullable=False)

# para indicar como queremos que se llame esta tabla en la base de datos
    __tablename__ = 'usuarios'

