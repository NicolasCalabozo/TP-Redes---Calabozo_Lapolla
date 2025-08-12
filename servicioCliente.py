import requests
from fastapi import status
from utils import validar_opcion, validar_entero, cadena_mayusculas, salir

def crear_pelicula() -> dict[str, str | int | list[str]]:
    titulo = input("Ingrese el título de la película: ").strip()
    año = validar_entero('Ingrese el año de estreno: ',
                         "Error: Ingrese un año válido")
    elenco = []
    opc = cadena_mayusculas(input('¿Desea ingresar el elenco? (S/N): '))
    if validar_opcion(opc):
        cadena_elenco = input(
            f"Ingrese el/los miembro/s del elenco, separados por coma: ")
        elenco = map(str.strip, cadena_elenco.split(sep=','))
    generos = []
    opc = cadena_mayusculas(input(
        "¿Desea ingresar los géneros de la película? (S/N): "))
    if validar_opcion(opc):
        generos_cadena = (
            input(f"Ingrese los generos de la película separados por coma: "))
        generos = map(str.strip, generos_cadena.split(','))
    sinopsis = ""
    opc = cadena_mayusculas(input("¿Desea ingresar una sinopsis? (S/N): "))
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
    if respuesta.status_code != requests.codes.ok:
        print(
            f"Error HTTP {respuesta.status_code}: {datos.get('error', 'Error desconocido')}")
        return
    print(datos.get("contenido"))

# OJO: Agregar metodo para retornar la pelicula con indice

def devolver_pelicula_con_indice() -> int:
    return 0


def seleccionar_generos(lista_generos: list[str]) -> list[str]:
    seleccionados = set()
    while True:
        print("\nSeleccione los géneros deseados (S para Salir):")
        
        for i in range(0, len(lista_generos), 5):
            fila = lista_generos[i:i+5]
            fila_marcada = []
            for j, genero in enumerate(fila, start=i+1):
                marcado = "(X)" if genero in seleccionados else "   "
                fila_marcada.append(f"{j}) {genero} {marcado}")
            print("\t".join(fila_marcada))

        opcion = input("Seleccione número: ").strip()
        
        if salir(opcion):
            break

        if not opcion.isdigit() or not (1 <= int(opcion) <= len(lista_generos)):
            print("Opción inválida, intente nuevamente.")
            continue

        id = int(opcion) - 1
        genero = lista_generos[id]

        if genero in seleccionados:
            seleccionados.remove(genero)
        else:
            seleccionados.add(genero)

    return list(seleccionados)

