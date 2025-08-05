from typing import Callable, Any
from modelos import Permiso
from fastapi import HTTPException, status

def validar_opcion(opc: str) -> bool:
    while True:
        if (opc != "N" and opc != "S"):
            print("Error: Opción incorrecta. Reintente (S/N).")
        else:
            break
    return True if opc == 'S' else False


def validar_entero(mensaje_input: str, mensaje_error: str) -> int:
    while True:
        valor = input(mensaje_input)
        try:
            return int(valor)
        except ValueError:
            print(mensaje_error)

def validar_dato_input(mensaje_input: str, mensaje_error: str, tipo_dato: Callable) -> Any:
    while True:
        valor = input(mensaje_input)
        try:
            return tipo_dato(valor)
        except (ValueError, TypeError):
            print(mensaje_error)
            
def verificar_permisos(permisos_usuario: list[Permiso], permisos_requeridos: list[Permiso]):
    if not any(permiso in permisos_usuario for permiso in permisos_requeridos):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene los permisos necesarios para realizar esta acción"
        )

def cadena_mayusculas(cadena: str) -> str:
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