from collections import Counter
from typing import Protocol

from src.domain import (
    Estado,
    Prioridad,
    Solicitud,
)


class GeneradorReporte(Protocol):
    def generar(
        self,
        solicitudes: list[Solicitud],
    ) -> dict[str, int]:
        ...


class ReportePorEstado:
    def generar(
        self,
        solicitudes: list[Solicitud],
    ) -> dict[str, int]:
        conteo = Counter(
            solicitud.estado.value
            for solicitud in solicitudes
        )

        return {
            estado.value: conteo.get(
                estado.value,
                0,
            )
            for estado in Estado
        }


class ReportePorPrioridad:
    def generar(
        self,
        solicitudes: list[Solicitud],
    ) -> dict[str, int]:
        conteo = Counter(
            solicitud.prioridad.value
            for solicitud in solicitudes
        )

        return {
            prioridad.value: conteo.get(
                prioridad.value,
                0,
            )
            for prioridad in Prioridad
        }