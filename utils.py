from typing import Callable, Any
from modelos import Permiso, Rol
from fastapi import HTTPException, status
import os
import socket

def validar_opcion(input_str: str) -> bool:
    '''
    Función para validar opciones S o N, donde se necesiten inputs de tipo Sí o No (S/N).
    Retorna True si la opción es 'S' (sí), False si es 'N' (no).
    '''
    opc = cadena_mayusculas(input(input_str))
    while opc not in ("S", "N"):
        print("Error: Opción incorrecta. Reintente (S/N).")
        opc = cadena_mayusculas(input(input_str))
    return opc == "S"


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


def verificar_permisos_servidor(permisos_usuario: list[str], permisos_requeridos: list[Permiso]):
    '''
    Convierte los roles en texto plano permisos_usuario al Enum Permiso y verifica si estan en la lista de permisos requeridos
    '''
    permisos_usuario_enum = [
        Permiso(p) for p in permisos_usuario if p in Permiso._value2member_map_]
    if not any(permiso in permisos_usuario_enum for permiso in permisos_requeridos):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene los permisos necesarios para realizar esta acción"
        )


def verificar_permisos_cliente(permisos_usuario: list[Permiso], permisos_requeridos: list[Permiso]) -> bool:
    '''
    Funcion análoga para el cliente, como los permisos del servidor vienen en forma de lista de strings,
    se reconvierten al enum correspondiente Permisos para ejecutar la comparación.
    '''
    permisos_usuario_enum = [
        Permiso(p) for p in permisos_usuario if p in Permiso._value2member_map_]
    return any(p in permisos_requeridos for p in permisos_usuario_enum)


def verificar_rol_cliente(rol_usuario: str | None, roles_requeridos: list[Rol]) -> bool:
    """
    Convierte el rol de texto plano en el Enum Rol y verifica si está en la lista de roles requeridos.
    """
    try:
        rol_enum = Rol(rol_usuario)  # Convierte texto en Enum
    except ValueError:
        return False  # Si el texto no coincide con ningún valor del Enum, no pasa la verificación

    return rol_enum in roles_requeridos


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


def limpiar_consola():
    '''
    Función para lograr transiciones entre selección de opciones a la hora de navegar en el CLI
    '''
    es_windows = os.name == 'nt'
    if es_windows:
        os.system('cls')
    else:
        os.system('clear')
        

def obtener_ip_local():
    """
    Función que obtiene la IP local (IPv4) de la máquina.

    Se crea una conexión UDP ficticia a una dirección remota cualquiera.
    Al preparar esta conexión, el sistema operativo nos indica qué IP local usaría para comunicarse.
    De esta manera, podemos obtener la IP local de la máquina.
    """
    #Se prepara un socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        #Se realiza la conexión UDP ficticia
        s.connect(("8.8.8.8", 80))
        #Se obtiene la IPV4 del propio socket, que coincide con la IP de la máquina.
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
    
