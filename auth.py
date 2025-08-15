from utils import verificar_permisos_servidor
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from modelos import Rol, Permiso
from typing import Any
security = HTTPBasic()

usuarios = [{
    "id": "1",
    "username": "admin",
    "password": "admin123",
    "rol": Rol.ADMIN,
    "permisos": [Permiso.TODO]
},
    {
        "id": "2",
        "username": "usuario",
        "password": "usuario123",
        "rol": Rol.USUARIO,
        "permisos": [Permiso.VER]
},
    {
        "id": "3",
        "username": "editor",
        "password": "editor123",
        "rol": Rol.EDITOR,
        "permisos": [Permiso.VER, Permiso.CREAR, Permiso.EDITAR]
}
]


def obtener_permisos(credenciales: HTTPBasicCredentials = Depends(security)) -> list[str]:
    usuario = buscar_usuario(credenciales.username)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    contraseña_correcta = secrets.compare_digest(
        credenciales.password, usuario['password'])

    if not contraseña_correcta:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return [perm.value for perm in usuario['permisos']]


def obtener_rol(credenciales: HTTPBasicCredentials = Depends(security)) -> str:
    usuario = buscar_usuario(credenciales.username)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    contraseña_correcta = secrets.compare_digest(
        credenciales.password, usuario['password'])

    if not contraseña_correcta:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return usuario['rol'].value


def buscar_usuario(username: str) -> dict[str, Any] | None:
    for usuario in usuarios:
        if username == usuario['username']:
            return usuario
    return None
