import json
from pathlib import Path

from src.domain import (
    Email,
    Estado,
    Estudiante,
    Prioridad,
    Responsable,
    Solicitud,
    TipoSolicitud,
)


class RepositorioJson:
    def __init__(
        self,
        archivo: str | Path,
    ) -> None:
        self._archivo = Path(archivo)

    def siguiente_id_estudiante(self) -> int:
        estudiantes = self._leer()[
            "estudiantes"
        ]

        return max(
            (
                estudiante["id"]
                for estudiante in estudiantes
            ),
            default=0,
        ) + 1

    def guardar_estudiante(
        self,
        estudiante: Estudiante,
    ) -> None:
        datos = self._leer()

        registro = {
            "id": estudiante.identificador,
            "nombre": estudiante.nombre,
            "email": estudiante.email.valor,
        }

        datos["estudiantes"] = (
            self._reemplazar_registro(
                datos["estudiantes"],
                registro,
            )
        )

        self._escribir(datos)

    def obtener_estudiante(
        self,
        identificador: int,
    ) -> Estudiante | None:
        registros = self._leer()[
            "estudiantes"
        ]

        for registro in registros:
            if registro["id"] == identificador:
                return Estudiante(
                    identificador=registro["id"],
                    nombre=registro["nombre"],
                    email=Email(
                        registro["email"]
                    ),
                )

        return None

    def siguiente_id_responsable(self) -> int:
        responsables = self._leer()[
            "responsables"
        ]

        return max(
            (
                responsable["id"]
                for responsable in responsables
            ),
            default=0,
        ) + 1

    def guardar_responsable(
        self,
        responsable: Responsable,
    ) -> None:
        datos = self._leer()

        registro = {
            "id": responsable.identificador,
            "nombre": responsable.nombre,
            "area": responsable.area,
        }

        datos["responsables"] = (
            self._reemplazar_registro(
                datos["responsables"],
                registro,
            )
        )

        self._escribir(datos)

    def obtener_responsable(
        self,
        identificador: int,
    ) -> Responsable | None:
        registros = self._leer()[
            "responsables"
        ]

        for registro in registros:
            if registro["id"] == identificador:
                return Responsable(
                    identificador=registro["id"],
                    nombre=registro["nombre"],
                    area=registro["area"],
                )

        return None

    def siguiente_id_solicitud(self) -> int:
        solicitudes = self._leer()[
            "solicitudes"
        ]

        return max(
            (
                solicitud["id"]
                for solicitud in solicitudes
            ),
            default=0,
        ) + 1

    def guardar_solicitud(
        self,
        solicitud: Solicitud,
    ) -> None:
        datos = self._leer()

        registro = {
            "id": solicitud.identificador,
            "estudiante_id": (
                solicitud.estudiante_id
            ),
            "tipo": solicitud.tipo.value,
            "descripcion": (
                solicitud.descripcion
            ),
            "prioridad": (
                solicitud.prioridad.value
            ),
            "estado": solicitud.estado.value,
            "responsable_id": (
                solicitud.responsable_id
            ),
        }

        datos["solicitudes"] = (
            self._reemplazar_registro(
                datos["solicitudes"],
                registro,
            )
        )

        self._escribir(datos)

    def obtener_solicitud(
        self,
        identificador: int,
    ) -> Solicitud | None:
        registros = self._leer()[
            "solicitudes"
        ]

        for registro in registros:
            if registro["id"] == identificador:
                return self._crear_solicitud(
                    registro
                )

        return None

    def listar_solicitudes(
        self,
    ) -> list[Solicitud]:
        return [
            self._crear_solicitud(registro)
            for registro
            in self._leer()["solicitudes"]
        ]

    def _leer(self) -> dict:
        if not self._archivo.exists():
            return self._datos_vacios()

        datos = json.loads(
            self._archivo.read_text(
                encoding="utf-8"
            )
        )

        datos.setdefault(
            "estudiantes",
            [],
        )
        datos.setdefault(
            "responsables",
            [],
        )
        datos.setdefault(
            "solicitudes",
            [],
        )

        return datos

    def _escribir(
        self,
        datos: dict,
    ) -> None:
        self._archivo.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._archivo.write_text(
            json.dumps(
                datos,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def _datos_vacios(self) -> dict:
        return {
            "estudiantes": [],
            "responsables": [],
            "solicitudes": [],
        }

    def _reemplazar_registro(
        self,
        registros: list[dict],
        nuevo_registro: dict,
    ) -> list[dict]:
        resultado = [
            registro
            for registro in registros
            if registro["id"]
            != nuevo_registro["id"]
        ]

        resultado.append(nuevo_registro)
        return resultado

    def _crear_solicitud(
        self,
        registro: dict,
    ) -> Solicitud:
        return Solicitud(
            identificador=registro["id"],
            estudiante_id=(
                registro["estudiante_id"]
            ),
            tipo=TipoSolicitud(
                registro["tipo"]
            ),
            descripcion=(
                registro["descripcion"]
            ),
            prioridad=Prioridad(
                registro["prioridad"]
            ),
            estado=Estado(
                registro["estado"]
            ),
            responsable_id=(
                registro["responsable_id"]
            ),
        )