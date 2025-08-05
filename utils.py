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
            
def verificar_permisos(permisos_usuario: list[Permiso], permisos_requeridos: list[Permiso]):
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

def cadena_mayusculas(cadena: str) -> str:
    '''Devuelve una cadena formateada en mayúsculas y sin espacios en blanco al comienzo o al final,
    para su interacción contra la base de datos'''
    
    return cadena.upper().strip()


def paginar_lista(lista: list, pagina: int = 1, limite: int = 10) -> dict:
    """
    Devuelve una porción paginada de una lista con metadatos.
    
    Parámetros:
    - lista: Lista de elementos a paginar
    - pagina: Número de página (1-indexado)
    - limite: Cantidad de elementos por página
    
    Retorna:
    - Un diccionario con los resultados paginados y metadatos
    """
    total = len(lista)
    if limite <= 0:
        limite = 10
    if pagina <= 0:
        pagina = 1

    inicio = (pagina - 1) * limite
    fin = inicio + limite
    datos = lista[inicio:fin]

    return {
        "datos": datos,
        "pagina": pagina,
        "limite": limite,
        "total": total,
        "paginas_totales": (total + limite - 1) // limite  # Redondeo hacia arriba
    }