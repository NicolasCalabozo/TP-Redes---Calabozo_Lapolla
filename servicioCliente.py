import requests
from fastapi import status
from utils import validar_opcion, validar_entero, cadena_mayusculas, salir
from modelos import Pelicula

def crear_pelicula() -> Pelicula | None:
    titulo = input("Ingrese el título de la película: ").strip()
    año = validar_entero('Ingrese el año de estreno: ',
                         "Error: Ingrese un año válido")
    elenco = []
    
    if validar_opcion("¿Desea ingresar el elenco? (S/N): "):
        cadena_elenco = input(
            f"Ingrese el/los miembro/s del elenco, separados por coma: ")
        elenco = list(map(str.strip, cadena_elenco.split(',')))
    generos = []
    if validar_opcion("¿Desea ingresar los generos? (S/N): "):
        generos_cadena = (
            input(f"Ingrese los generos de la película separados por coma: "))
        generos = list(map(str.strip, generos_cadena.split(',')))
    sinopsis = ""
    if validar_opcion("¿Desea ingresar la sinopsis? (S/N): "):
        sinopsis = input("Ingrese la sinopsis: ")
        
    print("\n-- Resumen de la película --\n")
    print(f"Título: {titulo}\n")
    print(f"Año: {año}\n")
    print(f"Elenco: {', '.join(elenco) if elenco else 'No ingresado'}\n")
    print(f"Géneros: {', '.join(generos) if generos else 'No ingresado'}\n")
    print(f"Sinopsis: {sinopsis if sinopsis else 'No ingresada'}\n")
    print("----------------------------\n")
        
    if not validar_opcion("¿Desea guardar la película? (S/N): "):
           return 
        
    pelicula = Pelicula(
        title=titulo,
        year=año,
        cast=elenco,
        genres=generos,
        extract=sinopsis
    )
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

