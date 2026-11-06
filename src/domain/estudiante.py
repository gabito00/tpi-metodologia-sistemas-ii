from dataclasses import dataclass

from .email import Email
from .errores import ErrorDominio


@dataclass(frozen=True)
class Estudiante:
    identificador: int
    nombre: str
    email: Email

    def __post_init__(self) -> None:
        if self.identificador <= 0:
            raise ErrorDominio(
                "El identificador del estudiante no es válido"
            )

        nombre_normalizado = self.nombre.strip()

        if not nombre_normalizado:
            raise ErrorDominio(
                "El nombre del estudiante es obligatorio"
            )

        object.__setattr__(
            self,
            "nombre",
            nombre_normalizado,
        )