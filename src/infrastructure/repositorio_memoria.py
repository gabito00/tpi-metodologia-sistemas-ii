from src.domain import (
    Estudiante,
    Responsable,
    Solicitud,
)


class RepositorioMemoria:
    def __init__(self) -> None:
        self._estudiantes: dict[int, Estudiante] = {}
        self._responsables: dict[int, Responsable] = {}
        self._solicitudes: dict[int, Solicitud] = {}

    def siguiente_id_estudiante(self) -> int:
        return max(
            self._estudiantes.keys(),
            default=0,
        ) + 1

    def guardar_estudiante(
        self,
        estudiante: Estudiante,
    ) -> None:
        self._estudiantes[
            estudiante.identificador
        ] = estudiante

    def obtener_estudiante(
        self,
        identificador: int,
    ) -> Estudiante | None:
        return self._estudiantes.get(
            identificador
        )

    def siguiente_id_responsable(self) -> int:
        return max(
            self._responsables.keys(),
            default=0,
        ) + 1

    def guardar_responsable(
        self,
        responsable: Responsable,
    ) -> None:
        self._responsables[
            responsable.identificador
        ] = responsable

    def obtener_responsable(
        self,
        identificador: int,
    ) -> Responsable | None:
        return self._responsables.get(
            identificador
        )

    def siguiente_id_solicitud(self) -> int:
        return max(
            self._solicitudes.keys(),
            default=0,
        ) + 1

    def guardar_solicitud(
        self,
        solicitud: Solicitud,
    ) -> None:
        self._solicitudes[
            solicitud.identificador
        ] = solicitud

    def obtener_solicitud(
        self,
        identificador: int,
    ) -> Solicitud | None:
        return self._solicitudes.get(
            identificador
        )

    def listar_solicitudes(
        self,
    ) -> list[Solicitud]:
        return list(
            self._solicitudes.values()
        )