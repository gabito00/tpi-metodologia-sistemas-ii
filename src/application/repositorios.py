from typing import Protocol

from src.domain import (
    Estudiante,
    Responsable,
    Solicitud,
)


class EstudianteRepositorio(Protocol):
    def siguiente_id_estudiante(self) -> int:
        """Devuelve el identificador del próximo estudiante."""
        ...

    def guardar_estudiante(
        self,
        estudiante: Estudiante,
    ) -> None:
        """Guarda o actualiza un estudiante."""
        ...

    def obtener_estudiante(
        self,
        identificador: int,
    ) -> Estudiante | None:
        """Busca un estudiante por su identificador."""
        ...


class ResponsableRepositorio(Protocol):
    def siguiente_id_responsable(self) -> int:
        """Devuelve el identificador del próximo responsable."""
        ...

    def guardar_responsable(
        self,
        responsable: Responsable,
    ) -> None:
        """Guarda o actualiza un responsable."""
        ...

    def obtener_responsable(
        self,
        identificador: int,
    ) -> Responsable | None:
        """Busca un responsable por su identificador."""
        ...


class SolicitudRepositorio(Protocol):
    def siguiente_id_solicitud(self) -> int:
        """Devuelve el identificador de la próxima solicitud."""
        ...

    def guardar_solicitud(
        self,
        solicitud: Solicitud,
    ) -> None:
        """Guarda o actualiza una solicitud."""
        ...

    def obtener_solicitud(
        self,
        identificador: int,
    ) -> Solicitud | None:
        """Busca una solicitud por su identificador."""
        ...

    def listar_solicitudes(
        self,
    ) -> list[Solicitud]:
        """Devuelve todas las solicitudes."""
        ...