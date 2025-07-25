def suma(a, b):
    return a + b

resultado = suma(num1=10, num2=20)
print(resultado)

data = {
    'num1': 10,
    'num2': 20
}

resultado = suma(num1=data.get('num1'), num2=data.get('num2'))
print(resultado)
# decorador para crear un endpoint que recibe un usuario y lo devuelve en formato JSON

# cuando el nombre de la llave del diccionario es el mismo que el nombre del parametro de la funcion, podemos usar el operador ** para desempaquetar el diccionario
# al usar el ** se desempaquetan las llaves del diccionario y se pasan como parametros a la funcion
# esto solo funciona en diccionarios, no en listas ni en tuplas
