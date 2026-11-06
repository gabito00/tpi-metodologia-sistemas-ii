from dataclasses import dataclass
from enum import Enum

from .errores import ErrorDominio


class Estado(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    CERRADA = "CERRADA"


class Prioridad(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"


class TipoSolicitud(str, Enum):
    CERTIFICADO = "CERTIFICADO"
    EQUIVALENCIA = "EQUIVALENCIA"
    INSCRIPCION = "INSCRIPCION"
    OTRO = "OTRO"


@dataclass(frozen=True)
class NuevaSolicitud:
    estudiante_id: int
    tipo: TipoSolicitud
    descripcion: str
    prioridad: Prioridad

    def __post_init__(self) -> None:
        if self.estudiante_id <= 0:
            raise ErrorDominio(
                "El identificador del estudiante no es válido"
            )

        descripcion_normalizada = (
            self.descripcion.strip()
        )

        if not descripcion_normalizada:
            raise ErrorDominio(
                "La descripción de la solicitud es obligatoria"
            )

        object.__setattr__(
            self,
            "descripcion",
            descripcion_normalizada,
        )


@dataclass
class Solicitud:
    identificador: int
    estudiante_id: int
    tipo: TipoSolicitud
    descripcion: str
    prioridad: Prioridad
    estado: Estado = Estado.PENDIENTE
    responsable_id: int | None = None

    def __post_init__(self) -> None:
        if self.identificador <= 0:
            raise ErrorDominio(
                "El identificador de la solicitud no es válido"
            )

        if self.estudiante_id <= 0:
            raise ErrorDominio(
                "El identificador del estudiante no es válido"
            )

        descripcion_normalizada = (
            self.descripcion.strip()
        )

        if not descripcion_normalizada:
            raise ErrorDominio(
                "La descripción de la solicitud es obligatoria"
            )

        self.descripcion = descripcion_normalizada

    def asignar_responsable(
        self,
        responsable_id: int,
    ) -> None:
        if responsable_id <= 0:
            raise ErrorDominio(
                "El identificador del responsable no es válido"
            )

        self.responsable_id = responsable_id

        if self.estado == Estado.PENDIENTE:
            self.estado = Estado.EN_PROCESO

    def cambiar_estado(
        self,
        nuevo_estado: Estado,
    ) -> None:
        self.estado = nuevo_estado