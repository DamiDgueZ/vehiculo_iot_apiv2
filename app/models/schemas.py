from pydantic import BaseModel
from typing import Optional

class MovimientoIndividualRequest(BaseModel):
    id_comando: int
    origen: str = "MANUAL"

class DemoEjecucionRequest(BaseModel):
    id_demo: int

class VehiculoCreateRequest(BaseModel):
    nombre: str
    modelo: str
    descripcion: str
    microcontrolador: str

class VehiculoUpdateRequest(BaseModel):
    nombre: str
    modelo: str
    descripcion: str
    microcontrolador: str
    activo: bool

class ComandoCreateRequest(BaseModel):
    nombre: str
    codigo: int
    descripcion: str

class ComandoUpdateRequest(BaseModel):
    nombre: str
    codigo: int
    descripcion: str
    activo: bool

class EstadoUpdateRequest(BaseModel):
    conectado: bool
    id_comando_actual: Optional[int] = None

class HistorialCreateRequest(BaseModel):
    id_comando: int
    origen: str = "MANUAL"

class DemoCreateRequest(BaseModel):
    nombre: str
    descripcion: str

class DemoUpdateRequest(BaseModel):
    nombre: str
    descripcion: str
    activo: bool

class MovimientoDemoRequest(BaseModel):
    id_comando: int
    orden: int
    duracion_ms: int
    pausa_ms: int = 0