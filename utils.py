from typing import Callable, Any
from modelos import Permiso
from fastapi import HTTPException, status


def validar_opcion(opc: str) -> bool:
    '''
    Función para validar opciones S o N, donde se necesiten inputs de tipo Si o No (S/N) equivalente a (Y/N)
    '''
    while True:
        if (opc != "N" and opc != "S"):
            print("Error: Opción incorrecta. Reintente (S/N).")
        else:
            break
    return True if opc == 'S' else False


def salir(opc: str) -> bool:
    opcion = cadena_mayusculas(opc)
    return opcion == 'S'


def validar_entero(mensaje_input: str, mensaje_error: str) -> int:
    '''
    Funcion de validación de input entero
    '''
    while True:
        valor = input(mensaje_input)
        try:
            return int(valor)
        except ValueError:
            print(mensaje_error)


def validar_dato_input(mensaje_input: str, mensaje_error: str, tipo_dato: Callable) -> Any:
    '''
    OJO: No utilizada
    Funcion genérica de input que verifica el tipo de dato ingresado
    Parámetros:
        - mensaje_input: Mensaje que le mostraremos al usuario, indicando qué esperamos que ingrese 
        - mensaje_error: Mensaje de error en caso que se ingrese un dato incorrecto
        - tipo_dato: Una función que le aplicaremos al input para verificar que sea del tipo correcto
    Funcionamiento:
        - Hasta que no se ingrese un dato válido, se vuelve a pedir al cliente que reingrese datos.
        - La función tipo Callable serán solamente las de casteo - Ej: int(...), str(...), bool(...)
    '''
    while True:
        valor = input(mensaje_input)
        try:
            return tipo_dato(valor)
        except (ValueError, TypeError):
            print(mensaje_error)


def verificar_permisos_servidor(permisos_usuario: list[Permiso], permisos_requeridos: list[Permiso]):
    '''
    Función que verifica los permisos de usuario necesarios para la posterior ejecución de otros métodos del servidor
    Parámetros:
        - Una lista de permisos de usuario
        - Una lista de permisos requeridos
    Funcionamiento:
        - Levanta un error http en caso de que el usuario no tenga al menos uno de los permisos requeridos

    '''
    if not any(permiso in permisos_usuario for permiso in permisos_requeridos):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene los permisos necesarios para realizar esta acción"
        )

def verificar_permisos_cliente(permisos_usuario: list[str], permisos_requeridos: list[Permiso]) -> bool:
    permisos_usuario_enum = [Permiso(p) for p in permisos_usuario if p in Permiso._value2member_map_]
    return any(p in permisos_requeridos for p in permisos_usuario_enum)

def cadena_mayusculas(cadena: str) -> str:
    '''Devuelve una cadena formateada en mayúsculas y sin espacios en blanco al comienzo o al final,
    para su interacción contra la base de datos'''
    return cadena.upper().strip()


def formatear_generos(generos: list[str], por_linea: int = 5) -> str:
    '''Devuelve la cantidad de generos según el valor de la variable por_linea'''
    resultado = ""
    for i, genero in enumerate(generos, start=1):
        resultado += genero
        if i % por_linea == 0:
            resultado += "\n"
        else:
            resultado += "\t"
    return resultado.strip()
