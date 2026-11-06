# Refactorings aplicados

## Objetivo

Mejorar la estructura interna del Sistema de Gestión de Solicitudes Académicas sin alterar negativamente su comportamiento externo.

El proceso se realizó sobre una versión inicial funcional y se verificó mediante pruebas automatizadas.

## 1. Extract Method

### Problema inicial

El método `asignar_responsable()` de `GestorAcademico` realizaba varias tareas:

- Buscaba la solicitud.
- Buscaba el responsable.
- Validaba ambos resultados.
- Modificaba la solicitud.
- Cambiaba su estado.
- Persistía todos los datos.

También existían búsquedas y validaciones mezcladas dentro de otros métodos.

### Código anterior

```python
def asignar_responsable(
    self,
    solicitud_id,
    responsable_id,
):
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
```

### Cambio aplicado

Se extrajeron métodos con nombres descriptivos en `SolicitudService`:

```python
def _crear_solicitud(
    self,
    datos: NuevaSolicitud,
) -> Solicitud:
    ...

def _validar_estudiante(
    self,
    estudiante_id: int,
) -> None:
    ...

def _obtener_responsable_o_fallar(
    self,
    responsable_id: int,
) -> Responsable:
    ...

def _obtener_solicitud_o_fallar(
    self,
    solicitud_id: int,
) -> Solicitud:
    ...

def _coincide_con_filtros(
    self,
    solicitud: Solicitud,
    estado: Estado | None,
    prioridad: Prioridad | None,
    tipo: TipoSolicitud | None,
) -> bool:
    ...
```

### Resultado

Cada función realiza una tarea concreta y mantiene un único nivel de abstracción.

La lectura del flujo principal resulta más clara y cada validación puede modificarse de manera aislada.

### Conceptos relacionados

- Funciones pequeñas.
- Nombres claros.
- Alta cohesión.
- Clean Code.

## 2. Move Method

### Problema inicial

`GestorAcademico` modificaba directamente los diccionarios que representaban solicitudes.

La asignación de responsable y el cambio de estado se encontraban fuera del objeto al que pertenecían esas reglas.

### Código anterior

```python
solicitud["responsable_id"] = responsable_id

if solicitud["estado"] == "PENDIENTE":
    solicitud["estado"] = "EN_PROCESO"
```

También se modificaba el estado de esta manera:

```python
solicitud["estado"] = nuevo_estado
```

### Cambio aplicado

Las operaciones se trasladaron a la entidad `Solicitud`:

```python
def asignar_responsable(
    self,
    responsable_id: int,
) -> None:
    if responsable_id <= 0:
        raise ErrorDominio(
            "El identificador del responsable no es válido"
        )

    self.responsable_id = responsable_id

    if self.estado == Estado.PENDIENTE:
        self.estado = Estado.EN_PROCESO
```

```python
def cambiar_estado(
    self,
    nuevo_estado: Estado,
) -> None:
    self.estado = nuevo_estado
```

El servicio ahora coordina el caso de uso:

```python
solicitud.asignar_responsable(
    responsable.identificador
)

self._solicitudes.guardar_solicitud(
    solicitud
)
```

### Resultado

Las reglas se encuentran junto a los datos que modifican.

`SolicitudService` coordina el caso de uso, mientras que `Solicitud` protege su comportamiento.

### Conceptos relacionados

- Move Method.
- Alta cohesión.
- Nombres del dominio.
- Responsabilidad única.

## 3. Introduce Parameter Object

### Problema inicial

La versión inicial recibía los datos de una solicitud como valores separados:

```python
def registrar_solicitud(
    self,
    estudiante_id,
    tipo,
    descripcion,
    prioridad,
):
    ...
```

Aunque la cantidad no alcanza el límite teórico de cinco parámetros para clasificarlo como Long Parameter List, estos datos pertenecen al mismo concepto y siempre viajan juntos.

### Cambio aplicado

Se creó el objeto `NuevaSolicitud`:

```python
@dataclass(frozen=True)
class NuevaSolicitud:
    estudiante_id: int
    tipo: TipoSolicitud
    descripcion: str
    prioridad: Prioridad

    def __post_init__(self) -> None:
        if self.estudiante_id <= 0:
            raise ErrorDominio(
                "El identificador del estudiante no es válido"
            )

        descripcion_normalizada = (
            self.descripcion.strip()
        )

        if not descripcion_normalizada:
            raise ErrorDominio(
                "La descripción de la solicitud es obligatoria"
            )

        object.__setattr__(
            self,
            "descripcion",
            descripcion_normalizada,
        )
```

El servicio recibe ahora un único objeto:

```python
def registrar_solicitud(
    self,
    datos: NuevaSolicitud,
) -> Solicitud:
    ...
```

### Resultado

La firma expresa que todos los valores forman una solicitud nueva.

El objeto también concentra la normalización y validación de sus propios datos.

### Conceptos relacionados

- Introduce Parameter Object.
- Legibilidad.
- Nombres del dominio.
- Alta cohesión.

## 4. Corrección de Obsesión por Primitivos

### Problema inicial

La versión inicial representaba conceptos del dominio mediante cadenas:

```python
"estado": "PENDIENTE"
"prioridad": "MEDIA"
"tipo": "CERTIFICADO"
```

El correo electrónico también era un `str` validado dentro de `GestorAcademico`:

```python
if not nombre or not email or "@" not in email:
    return None
```

### Cambio aplicado

Se introdujeron enumeraciones para los valores permitidos:

```python
class Estado(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    CERRADA = "CERRADA"
```

```python
class Prioridad(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
```

```python
class TipoSolicitud(str, Enum):
    CERTIFICADO = "CERTIFICADO"
    EQUIVALENCIA = "EQUIVALENCIA"
    INSCRIPCION = "INSCRIPCION"
    OTRO = "OTRO"
```

También se creó el objeto de valor `Email`:

```python
@dataclass(frozen=True)
class Email:
    valor: str

    def __post_init__(self) -> None:
        email_normalizado = (
            self.valor
            .strip()
            .lower()
        )

        if not self._es_valido(
            email_normalizado
        ):
            raise ErrorDominio(
                "El correo electrónico no es válido"
            )
```

### Resultado

Los conceptos del dominio dejan de depender de cadenas libres.

Los valores inválidos se rechazan antes de llegar a la persistencia y las reglas se encuentran en componentes con nombres del negocio.

### Conceptos relacionados

- Obsesión por Primitivos.
- Nombres del dominio.
- Manejo de errores mediante excepciones.
- Clean Code.

## 5. Separación de responsabilidades

Además de los cuatro refactorings documentados, se reorganizó la clase inicial.

### Antes

`GestorAcademico` concentraba:

- Entidades.
- Validaciones.
- Casos de uso.
- Búsquedas.
- Persistencia.
- Reportes.

### Después

La solución se divide en:

- `src/domain`: entidades y reglas.
- `src/application`: casos de uso y contratos.
- `src/infrastructure`: persistencia.
- `tests`: pruebas automatizadas.
- `docs`: evidencia técnica.
- `app.py`: composición y demostración.

### Principios aplicados

- SRP: responsabilidades separadas.
- OCP: nuevos reportes sin modificar el servicio.
- ISP: contratos separados por entidad.
- DIP: el servicio depende de contratos.
- Alta cohesión dentro de cada módulo.
- Bajo acoplamiento entre capas.

## 6. Manejo de errores

### Antes

La versión inicial devolvía valores genéricos:

```python
return None
```

```python
return False
```

### Después

La versión final utiliza excepciones con significado:

```python
raise ErrorDominio(
    "El correo electrónico no es válido"
)
```

```python
raise SolicitudNoEncontrada(
    f"No existe la solicitud {solicitud_id}"
)
```

Esto evita que el flujo principal dependa de códigos de error ambiguos.

## 7. Verificación del comportamiento

El flujo principal produjo el mismo resultado antes y después:

```text
{'PENDIENTE': 0, 'EN_PROCESO': 0, 'RESUELTA': 1, 'CERRADA': 0}
```

La versión final cuenta con ocho pruebas automatizadas:

```bash
python -m unittest discover -s tests -v
```

Resultado:

```text
Ran 8 tests

OK
```

## 8. Trazabilidad en Git

| Hito | Tag |
|---|---|
| Versión inicial | `estado-inicial` |
| Diagnóstico técnico | `etapa-diagnostico` |
| Aplicación de refactorings | `etapa-refactoring` |
| Pruebas ampliadas | `etapa-pruebas` |
| Versión final del código | `estado-refactorizado` |

Los tags permiten recuperar y comparar cada etapa sin depender únicamente de fragmentos incluidos en la documentación.

## Conclusión

Los refactorings conservaron las funcionalidades visibles y mejoraron la calidad interna.

La versión final presenta responsabilidades más claras, mayor cohesión, menor acoplamiento, errores explícitos y pruebas independientes de la persistencia principal.