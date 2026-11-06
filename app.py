import json
from pathlib import Path


class GestorAcademico:
    def __init__(self, archivo):
        self.archivo = Path(archivo)

        if self.archivo.exists():
            self.datos = json.loads(
                self.archivo.read_text(encoding="utf-8")
            )
        else:
            self.datos = {
                "estudiantes": [],
                "responsables": [],
                "solicitudes": [],
            }

    def registrar_estudiante(self, nombre, email):
        if not nombre or not email or "@" not in email:
            return None

        estudiante = {
            "id": len(self.datos["estudiantes"]) + 1,
            "nombre": nombre,
            "email": email,
        }

        self.datos["estudiantes"].append(estudiante)
        self.guardar()
        return estudiante

    def registrar_responsable(self, nombre, area):
        if not nombre or not area:
            return None

        responsable = {
            "id": len(self.datos["responsables"]) + 1,
            "nombre": nombre,
            "area": area,
        }

        self.datos["responsables"].append(responsable)
        self.guardar()
        return responsable

    def registrar_solicitud(
        self,
        estudiante_id,
        tipo,
        descripcion,
        prioridad,
    ):
        estudiante = None

        for item in self.datos["estudiantes"]:
            if item["id"] == estudiante_id:
                estudiante = item
                break

        if estudiante is None:
            return None

        if tipo not in [
            "CERTIFICADO",
            "EQUIVALENCIA",
            "INSCRIPCION",
            "OTRO",
        ]:
            return None

        if prioridad not in ["BAJA", "MEDIA", "ALTA"]:
            return None

        if not descripcion:
            return None

        solicitud = {
            "id": len(self.datos["solicitudes"]) + 1,
            "estudiante_id": estudiante_id,
            "tipo": tipo,
            "descripcion": descripcion,
            "prioridad": prioridad,
            "estado": "PENDIENTE",
            "responsable_id": None,
        }

        self.datos["solicitudes"].append(solicitud)
        self.guardar()
        return solicitud

    def asignar_responsable(self, solicitud_id, responsable_id):
        solicitud = None
        responsable = None

        for item in self.datos["solicitudes"]:
            if item["id"] == solicitud_id:
                solicitud = item
                break

        for item in self.datos["responsables"]:
            if item["id"] == responsable_id:
                responsable = item
                break

        if solicitud is None or responsable is None:
            return False

        solicitud["responsable_id"] = responsable_id

        if solicitud["estado"] == "PENDIENTE":
            solicitud["estado"] = "EN_PROCESO"

        self.guardar()
        return True

    def cambiar_estado(self, solicitud_id, nuevo_estado):
        estados_validos = [
            "PENDIENTE",
            "EN_PROCESO",
            "RESUELTA",
            "CERRADA",
        ]

        if nuevo_estado not in estados_validos:
            return False

        for solicitud in self.datos["solicitudes"]:
            if solicitud["id"] == solicitud_id:
                solicitud["estado"] = nuevo_estado
                self.guardar()
                return True

        return False

    def buscar_solicitudes(
        self,
        estado=None,
        prioridad=None,
        tipo=None,
    ):
        resultado = []

        for solicitud in self.datos["solicitudes"]:
            if estado and solicitud["estado"] != estado:
                continue

            if prioridad and solicitud["prioridad"] != prioridad:
                continue

            if tipo and solicitud["tipo"] != tipo:
                continue

            resultado.append(solicitud)

        return resultado

    def generar_reporte(self):
        reporte = {
            "PENDIENTE": 0,
            "EN_PROCESO": 0,
            "RESUELTA": 0,
            "CERRADA": 0,
        }

        for solicitud in self.datos["solicitudes"]:
            estado = solicitud["estado"]

            if estado in reporte:
                reporte[estado] += 1

        return reporte

    def guardar(self):
        self.archivo.write_text(
            json.dumps(
                self.datos,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


def ejecutar_demo():
    gestor = GestorAcademico("datos_demo.json")

    estudiante = gestor.registrar_estudiante(
        "Ana Torres",
        "ana.torres@alumnos.utn.edu.ar",
    )

    responsable = gestor.registrar_responsable(
        "María López",
        "Secretaría Académica",
    )

    solicitud = gestor.registrar_solicitud(
        estudiante["id"],
        "CERTIFICADO",
        "Solicita certificado de alumno regular",
        "MEDIA",
    )

    gestor.asignar_responsable(
        solicitud["id"],
        responsable["id"],
    )

    gestor.cambiar_estado(
        solicitud["id"],
        "RESUELTA",
    )

    print(gestor.generar_reporte())


if __name__ == "__main__":
    ejecutar_demo()