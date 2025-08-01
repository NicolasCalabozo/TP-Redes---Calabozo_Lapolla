from enum import Enum
from pydantic import BaseModel


class Permiso(Enum):
    VER = "ver"
    CREAR = "crear"
    EDITAR = "editar"
    ELIMINAR = "eliminar"
    TODO = "todo"


class Rol(Enum):
    USUARIO = "usuario"
    ADMIN = 'admin'
    EDITOR = 'editor'


class Pelicula(BaseModel):
    titulo: str
    año: int
    elenco: list[str]
    generos: list[str]
    sinopsis: str


class PeliculaRequest(BaseModel):
    pelicula: Pelicula
    permisos: list[str]

#OJO: Idea no implementada
class RequestGenerica(BaseModel):
    peticion: dict
    permisos: list[str]
