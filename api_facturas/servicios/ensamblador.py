"""
Ensamblador — el ÚNICO lugar del sistema que conoce clases concretas.

Tres líneas, sin diccionarios ni DB_PROVIDER: la v1 tiene UN motor y el
código lo dice (YAGNI con dirección). Cuando la v3 agregue MariaDB, SOLO este
archivo se convertirá en la fábrica real — controllers y servicios no se
tocarán: ese será el examen del principio abierto/cerrado.
"""

import os

from repositorios.repositorio_producto_postgresql import (
    RepositorioProductoPostgreSQL,
)
from servicios.abstracciones.i_servicio_producto import IServicioProducto
from servicios.servicio_producto import ServicioProducto


def crear_servicio_producto() -> IServicioProducto:
    """Arma el servicio con su repositorio (la cadena viene del entorno)."""
    repositorio = RepositorioProductoPostgreSQL(os.environ["DB_POSTGRES"])
    return ServicioProducto(repositorio)
