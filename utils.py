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
            
def verificar_permisos(permisos_usuario: list[Permiso], requeridos: list[Permiso]):
    if not any(p in permisos_usuario for p in requeridos):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene los permisos necesarios para realizar esta acción"
        )
