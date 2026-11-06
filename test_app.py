import tempfile
import unittest
from pathlib import Path

from app import GestorAcademico


class GestorAcademicoTest(unittest.TestCase):
    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        self.archivo = Path(self.directorio.name) / "datos.json"
        self.gestor = GestorAcademico(self.archivo)

        self.estudiante = self.gestor.registrar_estudiante(
            "Ana Torres",
            "ana.torres@alumnos.utn.edu.ar",
        )

        self.responsable = self.gestor.registrar_responsable(
            "María López",
            "Secretaría Académica",
        )

    def tearDown(self):
        self.directorio.cleanup()

    def test_flujo_principal(self):
        solicitud = self.gestor.registrar_solicitud(
            self.estudiante["id"],
            "CERTIFICADO",
            "Solicita certificado de alumno regular",
            "MEDIA",
        )

        self.assertIsNotNone(solicitud)

        asignada = self.gestor.asignar_responsable(
            solicitud["id"],
            self.responsable["id"],
        )

        self.assertTrue(asignada)

        actualizada = self.gestor.cambiar_estado(
            solicitud["id"],
            "RESUELTA",
        )

        self.assertTrue(actualizada)

        self.assertEqual(
            {
                "PENDIENTE": 0,
                "EN_PROCESO": 0,
                "RESUELTA": 1,
                "CERRADA": 0,
            },
            self.gestor.generar_reporte(),
        )

    def test_filtra_por_prioridad(self):
        self.gestor.registrar_solicitud(
            self.estudiante["id"],
            "EQUIVALENCIA",
            "Solicita equivalencia de una materia",
            "ALTA",
        )

        resultado = self.gestor.buscar_solicitudes(
            prioridad="ALTA"
        )

        self.assertEqual(1, len(resultado))

    def test_rechaza_email_invalido(self):
        resultado = self.gestor.registrar_estudiante(
            "Estudiante inválido",
            "correo-invalido",
        )

        self.assertIsNone(resultado)

    def test_rechaza_estado_invalido(self):
        solicitud = self.gestor.registrar_solicitud(
            self.estudiante["id"],
            "CERTIFICADO",
            "Solicita certificado",
            "MEDIA",
        )

        resultado = self.gestor.cambiar_estado(
            solicitud["id"],
            "ELIMINADA",
        )

        self.assertFalse(resultado)

    def test_persistencia_json(self):
        self.gestor.registrar_solicitud(
            self.estudiante["id"],
            "INSCRIPCION",
            "Consulta sobre inscripción",
            "BAJA",
        )

        nuevo_gestor = GestorAcademico(self.archivo)

        self.assertEqual(
            1,
            len(nuevo_gestor.datos["solicitudes"]),
        )


if __name__ == "__main__":
    unittest.main()