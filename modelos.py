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
    title: str
    year: int
    cast: list[str]
    genres: list[str]
    extract: str
