from dataclasses import dataclass

from .errores import ErrorDominio


@dataclass(frozen=True)
class Email:
    valor: str

    def __post_init__(self) -> None:
        email_normalizado = self.valor.strip().lower()

        if not self._es_valido(email_normalizado):
            raise ErrorDominio(
                "El correo electrónico no es válido"
            )

        object.__setattr__(
            self,
            "valor",
            email_normalizado,
        )

    def _es_valido(self, email: str) -> bool:
        return (
            "@" in email
            and not email.startswith("@")
            and not email.endswith("@")
        )

    def __str__(self) -> str:
        return self.valor