from flask import Flask, request
from variables import conexion

app = Flask(__name__)
print(app.config)
# el app.config almacenara todas las variables de configuracion de la aplicacion
# aca inicializamos la conexion a la base de datos
# al moneto de pasar la aplicacion de flask en esta se encontraras la cadena de coneccion a la BD

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root:ROOT@localhost:3306/alumnos_db'


conexion.init_app(app)



if __name__ == '__main__':
    app.run(debug=True)

