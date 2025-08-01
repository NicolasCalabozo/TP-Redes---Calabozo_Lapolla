from enum import Enum


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
