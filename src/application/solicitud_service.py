from src.application.repositorios import (
    EstudianteRepositorio,
    ResponsableRepositorio,
    SolicitudRepositorio,
)
from src.domain import (
    Email,
    Estado,
    Estudiante,
    NuevaSolicitud,
    Prioridad,
    Responsable,
    Solicitud,
    TipoSolicitud,
)


class EstudianteNoEncontrado(LookupError):
    pass


class ResponsableNoEncontrado(LookupError):
    pass


class SolicitudNoEncontrada(LookupError):
    pass


class SolicitudService:
    def __init__(
        self,
        estudiantes: EstudianteRepositorio,
        responsables: ResponsableRepositorio,
        solicitudes: SolicitudRepositorio,
    ) -> None:
        self._estudiantes = estudiantes
        self._responsables = responsables
        self._solicitudes = solicitudes

    def registrar_estudiante(
        self,
        nombre: str,
        email: str,
    ) -> Estudiante:
        estudiante = Estudiante(
            identificador=(
                self._estudiantes
                .siguiente_id_estudiante()
            ),
            nombre=nombre,
            email=Email(email),
        )

        self._estudiantes.guardar_estudiante(
            estudiante
        )

        return estudiante

    def registrar_responsable(
        self,
        nombre: str,
        area: str,
    ) -> Responsable:
        responsable = Responsable(
            identificador=(
                self._responsables
                .siguiente_id_responsable()
            ),
            nombre=nombre,
            area=area,
        )

        self._responsables.guardar_responsable(
            responsable
        )

        return responsable

    def registrar_solicitud(
        self,
        datos: NuevaSolicitud,
    ) -> Solicitud:
        self._validar_estudiante(
            datos.estudiante_id
        )

        solicitud = self._crear_solicitud(
            datos
        )

        self._solicitudes.guardar_solicitud(
            solicitud
        )

        return solicitud

    def asignar_responsable(
        self,
        solicitud_id: int,
        responsable_id: int,
    ) -> Solicitud:
        solicitud = (
            self._obtener_solicitud_o_fallar(
                solicitud_id
            )
        )

        responsable = (
            self._obtener_responsable_o_fallar(
                responsable_id
            )
        )

        solicitud.asignar_responsable(
            responsable.identificador
        )

        self._solicitudes.guardar_solicitud(
            solicitud
        )

        return solicitud

    def cambiar_estado(
        self,
        solicitud_id: int,
        nuevo_estado: Estado,
    ) -> Solicitud:
        solicitud = (
            self._obtener_solicitud_o_fallar(
                solicitud_id
            )
        )

        solicitud.cambiar_estado(
            nuevo_estado
        )

        self._solicitudes.guardar_solicitud(
            solicitud
        )

        return solicitud

    def buscar_solicitudes(
        self,
        estado: Estado | None = None,
        prioridad: Prioridad | None = None,
        tipo: TipoSolicitud | None = None,
    ) -> list[Solicitud]:
        solicitudes = (
            self._solicitudes
            .listar_solicitudes()
        )

        return [
            solicitud
            for solicitud in solicitudes
            if self._coincide_con_filtros(
                solicitud=solicitud,
                estado=estado,
                prioridad=prioridad,
                tipo=tipo,
            )
        ]

    def _crear_solicitud(
        self,
        datos: NuevaSolicitud,
    ) -> Solicitud:
        return Solicitud(
            identificador=(
                self._solicitudes
                .siguiente_id_solicitud()
            ),
            estudiante_id=datos.estudiante_id,
            tipo=datos.tipo,
            descripcion=datos.descripcion,
            prioridad=datos.prioridad,
        )

    def _validar_estudiante(
        self,
        estudiante_id: int,
    ) -> None:
        estudiante = (
            self._estudiantes
            .obtener_estudiante(
                estudiante_id
            )
        )

        if estudiante is None:
            raise EstudianteNoEncontrado(
                "No existe el estudiante "
                f"{estudiante_id}"
            )

    def _obtener_responsable_o_fallar(
        self,
        responsable_id: int,
    ) -> Responsable:
        responsable = (
            self._responsables
            .obtener_responsable(
                responsable_id
            )
        )

        if responsable is None:
            raise ResponsableNoEncontrado(
                "No existe el responsable "
                f"{responsable_id}"
            )

        return responsable

    def _obtener_solicitud_o_fallar(
        self,
        solicitud_id: int,
    ) -> Solicitud:
        solicitud = (
            self._solicitudes
            .obtener_solicitud(
                solicitud_id
            )
        )

        if solicitud is None:
            raise SolicitudNoEncontrada(
                "No existe la solicitud "
                f"{solicitud_id}"
            )

        return solicitud

    def _coincide_con_filtros(
        self,
        solicitud: Solicitud,
        estado: Estado | None,
        prioridad: Prioridad | None,
        tipo: TipoSolicitud | None,
    ) -> bool:
        coincide_estado = (
            estado is None
            or solicitud.estado == estado
        )

        coincide_prioridad = (
            prioridad is None
            or solicitud.prioridad == prioridad
        )

        coincide_tipo = (
            tipo is None
            or solicitud.tipo == tipo
        )

        return (
            coincide_estado
            and coincide_prioridad
            and coincide_tipo
        )