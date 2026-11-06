import tempfile
import unittest
from pathlib import Path

from src.application import (
    ReportePorEstado,
    ReportePorPrioridad,
    SolicitudNoEncontrada,
    SolicitudService,
)
from src.domain import (
    ErrorDominio,
    Estado,
    NuevaSolicitud,
    Prioridad,
    TipoSolicitud,
)
from src.infrastructure import (
    RepositorioJson,
    RepositorioMemoria,
)


class SolicitudServiceTest(
    unittest.TestCase
):
    def setUp(self) -> None:
        self.repositorio = (
            RepositorioMemoria()
        )

        self.servicio = SolicitudService(
            estudiantes=self.repositorio,
            responsables=self.repositorio,
            solicitudes=self.repositorio,
        )

        self.estudiante = (
            self.servicio
            .registrar_estudiante(
                nombre="Ana Torres",
                email=(
                    "ana.torres"
                    "@alumnos.utn.edu.ar"
                ),
            )
        )

        self.responsable = (
            self.servicio
            .registrar_responsable(
                nombre="María López",
                area="Secretaría Académica",
            )
        )

    def crear_solicitud(
        self,
        prioridad: Prioridad = (
            Prioridad.MEDIA
        ),
    ):
        return (
            self.servicio
            .registrar_solicitud(
                NuevaSolicitud(
                    estudiante_id=(
                        self.estudiante
                        .identificador
                    ),
                    tipo=(
                        TipoSolicitud
                        .CERTIFICADO
                    ),
                    descripcion=(
                        "Solicita certificado "
                        "de alumno regular"
                    ),
                    prioridad=prioridad,
                )
            )
        )

    def test_flujo_principal_conserva_resultado(
        self,
    ) -> None:
        solicitud = self.crear_solicitud()

        self.servicio.asignar_responsable(
            solicitud_id=(
                solicitud.identificador
            ),
            responsable_id=(
                self.responsable
                .identificador
            ),
        )

        self.servicio.cambiar_estado(
            solicitud_id=(
                solicitud.identificador
            ),
            nuevo_estado=Estado.RESUELTA,
        )

        reporte = ReportePorEstado()

        resultado = reporte.generar(
            self.repositorio
            .listar_solicitudes()
        )

        self.assertEqual(
            {
                "PENDIENTE": 0,
                "EN_PROCESO": 0,
                "RESUELTA": 1,
                "CERRADA": 0,
            },
            resultado,
        )

    def test_filtra_por_prioridad(
        self,
    ) -> None:
        self.crear_solicitud(
            Prioridad.MEDIA
        )
        self.crear_solicitud(
            Prioridad.ALTA
        )

        resultado = (
            self.servicio
            .buscar_solicitudes(
                prioridad=Prioridad.ALTA
            )
        )

        self.assertEqual(
            1,
            len(resultado),
        )

        self.assertEqual(
            Prioridad.ALTA,
            resultado[0].prioridad,
        )

    def test_rechaza_email_invalido(
        self,
    ) -> None:
        with self.assertRaisesRegex(
            ErrorDominio,
            "correo electrónico",
        ):
            self.servicio.registrar_estudiante(
                nombre="Estudiante inválido",
                email="correo-invalido",
            )

    def test_rechaza_estado_inexistente(
        self,
    ) -> None:
        with self.assertRaises(
            ValueError
        ):
            Estado("ELIMINADA")

    def test_persistencia_json(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directorio:
            archivo = (
                Path(directorio)
                / "datos.json"
            )

            repositorio = (
                RepositorioJson(archivo)
            )

            servicio = SolicitudService(
                estudiantes=repositorio,
                responsables=repositorio,
                solicitudes=repositorio,
            )

            estudiante = (
                servicio
                .registrar_estudiante(
                    nombre="Luis Pérez",
                    email=(
                        "luis.perez"
                        "@alumnos.utn.edu.ar"
                    ),
                )
            )

            solicitud = (
                servicio
                .registrar_solicitud(
                    NuevaSolicitud(
                        estudiante_id=(
                            estudiante
                            .identificador
                        ),
                        tipo=(
                            TipoSolicitud
                            .INSCRIPCION
                        ),
                        descripcion=(
                            "Consulta sobre "
                            "inscripción"
                        ),
                        prioridad=(
                            Prioridad.BAJA
                        ),
                    )
                )
            )

            nuevo_repositorio = (
                RepositorioJson(
                    archivo
                )
            )

            recuperada = (
                nuevo_repositorio
                .obtener_solicitud(
                    solicitud.identificador
                )
            )

            self.assertEqual(
                solicitud,
                recuperada,
            )
    def test_asignacion_cambia_estado(
        self,
    ) -> None:
        solicitud = self.crear_solicitud()

        actualizada = (
            self.servicio
            .asignar_responsable(
                solicitud_id=(
                    solicitud.identificador
                ),
                responsable_id=(
                    self.responsable
                    .identificador
                ),
            )
        )

        self.assertEqual(
            Estado.EN_PROCESO,
            actualizada.estado,
        )

        self.assertEqual(
            self.responsable.identificador,
            actualizada.responsable_id,
        )

    def test_informa_solicitud_inexistente(
        self,
    ) -> None:
        with self.assertRaisesRegex(
            SolicitudNoEncontrada,
            "No existe la solicitud 99",
        ):
            self.servicio.cambiar_estado(
                solicitud_id=99,
                nuevo_estado=Estado.RESUELTA,
            )

    def test_reporte_por_prioridad(
        self,
    ) -> None:
        self.crear_solicitud(
            Prioridad.MEDIA
        )
        self.crear_solicitud(
            Prioridad.ALTA
        )

        reporte = ReportePorPrioridad()

        resultado = reporte.generar(
            self.repositorio
            .listar_solicitudes()
        )

        self.assertEqual(
            {
                "BAJA": 0,
                "MEDIA": 1,
                "ALTA": 1,
            },
            resultado,
        )

if __name__ == "__main__":
    unittest.main()