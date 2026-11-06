from pathlib import Path

from src.application import (
    ReportePorEstado,
    SolicitudService,
)
from src.domain import (
    Estado,
    ErrorDominio,
    NuevaSolicitud,
    Prioridad,
    TipoSolicitud,
)
from src.infrastructure import (
    RepositorioJson,
)


def crear_servicio(
    archivo: str | Path,
) -> tuple[
    SolicitudService,
    RepositorioJson,
]:
    repositorio = RepositorioJson(
        archivo
    )

    servicio = SolicitudService(
        estudiantes=repositorio,
        responsables=repositorio,
        solicitudes=repositorio,
    )

    return servicio, repositorio


def ejecutar_demo(
    archivo: str | Path = "datos_demo.json",
) -> dict[str, int]:
    servicio, repositorio = crear_servicio(
        archivo
    )

    estudiante = (
        servicio.registrar_estudiante(
            nombre="Ana Torres",
            email=(
                "ana.torres"
                "@alumnos.utn.edu.ar"
            ),
        )
    )

    responsable = (
        servicio.registrar_responsable(
            nombre="María López",
            area="Secretaría Académica",
        )
    )

    solicitud = (
        servicio.registrar_solicitud(
            NuevaSolicitud(
                estudiante_id=(
                    estudiante.identificador
                ),
                tipo=(
                    TipoSolicitud.CERTIFICADO
                ),
                descripcion=(
                    "Solicita certificado "
                    "de alumno regular"
                ),
                prioridad=Prioridad.MEDIA,
            )
        )
    )

    servicio.asignar_responsable(
        solicitud_id=solicitud.identificador,
        responsable_id=(
            responsable.identificador
        ),
    )

    servicio.cambiar_estado(
        solicitud_id=solicitud.identificador,
        nuevo_estado=Estado.RESUELTA,
    )

    reporte = ReportePorEstado()

    return reporte.generar(
        repositorio.listar_solicitudes()
    )


def main() -> None:
    try:
        resultado = ejecutar_demo()
        print(resultado)
    except ErrorDominio as error:
        print(
            f"Error de validación: {error}"
        )
    except LookupError as error:
        print(
            f"Registro inexistente: {error}"
        )


if __name__ == "__main__":
    main()