from dataclasses import dataclass

from .errores import ErrorDominio


@dataclass(frozen=True)
class Responsable:
    identificador: int
    nombre: str
    area: str

    def __post_init__(self) -> None:
        if self.identificador <= 0:
            raise ErrorDominio(
                "El identificador del responsable no es válido"
            )

        nombre_normalizado = self.nombre.strip()
        area_normalizada = self.area.strip()

        if not nombre_normalizado:
            raise ErrorDominio(
                "El nombre del responsable es obligatorio"
            )

        if not area_normalizada:
            raise ErrorDominio(
                "El área del responsable es obligatoria"
            )

        object.__setattr__(
            self,
            "nombre",
            nombre_normalizado,
        )

        object.__setattr__(
            self,
            "area",
            area_normalizada,
        )