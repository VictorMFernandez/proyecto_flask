from variables import conexion
from sqlalchemy import Column, types, ForeignKey

class DireccionModel(conexion.Model):
    id = Column(primary_key=True, 
                autoincrement=True, 
                type_=types.Integer)
    calle= Column(type_=types.String(100),
                nullable=False)
    numero = Column(type_=types.String(10), 
                    nullable=False)
    referencia = Column(type_=types.String(200), 
                        nullable=True)
    predeterminada = Column(type_=types.Boolean, 
                            default=False,
                            nullable=False)

# relaciones

usuarioId = Column(ForeignKey(column='usuarios.id'), 
                    nullable=False, name='usuario_id')


__tablename__ = 'direcciones'