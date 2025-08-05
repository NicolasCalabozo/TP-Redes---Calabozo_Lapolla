import requests
from fastapi import status
from typing import Callable, Any
from utils import validar_opcion, validar_entero

def crear_pelicula() -> dict[str, str | int | list[str]]:
    titulo = input("Ingrese el título de la película: ").strip()
    año = validar_entero('Ingrese el año de estreno: ',
                         "Error: Ingrese un año válido")
    elenco = []
    opc = input('¿Desea ingresar el elenco? (S/N): ').upper().strip()
    if validar_opcion(opc):
        cadena_elenco = input(
            f"Ingrese el/los miembro/s del elenco, separados por coma: ")
        elenco = map(str.strip, cadena_elenco.split(sep=','))
    generos = []
    opc = input(
        "¿Desea ingresar los géneros de la película? (S/N): ").strip().upper()
    if validar_opcion(opc):
        generos_cadena = (
            input(f"Ingrese los generos de la película separados por coma: "))
        generos = map(str.strip, generos_cadena.split(','))
    sinopsis = ""
    opc = input("¿Desea ingresar una sinopsis? (S/N): ").strip().upper()
    if validar_opcion(opc):
        sinopsis = input("Ingrese la sinopsis: ")
    pelicula = {
        "title": titulo,
        "year": año,
        "cast": elenco,
        "genres": generos,
        "extract": sinopsis
    }
    return pelicula

# OJO: Completar método de modificar

def modificar_pelicula():
    # pelicula['title'] = nuevo nombre
    pass

def procesar_respuesta(respuesta: requests.Response) -> None:
    datos = respuesta.json()
    if respuesta.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
        print(
            f"Error HTTP {respuesta.status_code}: {datos.get('error', 'Error desconocido')}")
        return
    print(datos.get("contenido"))

# OJO: Agregar metodo para retornar la pelicula con indice

def devolver_pelicula_con_indice() -> int:
    return 0


