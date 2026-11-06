# Code review profesional

## 1. Objetivo

Revisar la versión refactorizada del Sistema de Gestión de Solicitudes Académicas antes de considerarla técnicamente aceptada.

El code review se enfoca en el código y en sus decisiones técnicas. No evalúa a la persona que lo desarrolló.

## 2. Alcance

La revisión incluye:

- Entidades del dominio.
- Casos de uso.
- Contratos de repositorio.
- Persistencia en memoria y JSON.
- Generadores de reportes.
- Punto de entrada.
- Pruebas automatizadas.
- Documentación técnica.
- Historial y tags de Git.

## 3. Criterios de aceptación técnica

Para aprobar la revisión, el proyecto debe cumplir estas condiciones:

- Ejecutar correctamente.
- Aprobar todas las pruebas.
- Mantener las funcionalidades existentes.
- No introducir regresiones conocidas.
- Utilizar nombres descriptivos.
- Mantener funciones pequeñas.
- Aplicar los principios SOLID cuando correspondan.
- Evitar duplicación innecesaria.
- Manejar errores mediante excepciones.
- No exponer datos personales reales.
- Mantener documentación actualizada.
- Conservar trazabilidad mediante commits y tags.

## 4. Checklist de lógica y funcionalidad

| Criterio | Evidencia | Resultado |
|---|---|---|
| El sistema registra estudiantes | `SolicitudService.registrar_estudiante()` | Aprobado |
| El sistema registra responsables | `SolicitudService.registrar_responsable()` | Aprobado |
| El sistema registra solicitudes | `SolicitudService.registrar_solicitud()` | Aprobado |
| La asignación actualiza la solicitud | `Solicitud.asignar_responsable()` | Aprobado |
| La asignación cambia PENDIENTE a EN_PROCESO | Prueba `test_asignacion_cambia_estado` | Aprobado |
| El cambio de estado funciona | `Solicitud.cambiar_estado()` | Aprobado |
| Los filtros funcionan | Prueba `test_filtra_por_prioridad` | Aprobado |
| El reporte por estado conserva el resultado | Prueba del flujo principal | Aprobado |
| El reporte por prioridad funciona | Prueba `test_reporte_por_prioridad` | Aprobado |
| La persistencia JSON recupera los datos | Prueba `test_persistencia_json` | Aprobado |
| Las solicitudes inexistentes generan un error claro | Prueba `test_informa_solicitud_inexistente` | Aprobado |

### Resultado de lógica y funcionalidad

Los casos de uso principales funcionan y el comportamiento externo del flujo principal se conserva.

No se detectaron regresiones conocidas.

## 5. Checklist de legibilidad

| Criterio | Evidencia | Resultado |
|---|---|---|
| Los nombres representan conceptos del dominio | `Estudiante`, `Responsable`, `Solicitud`, `Prioridad` y `Estado` | Aprobado |
| Las funciones tienen nombres descriptivos | `registrar_solicitud()`, `asignar_responsable()` y `cambiar_estado()` | Aprobado |
| Los métodos realizan tareas acotadas | Métodos privados extraídos en `SolicitudService` | Aprobado |
| Los errores tienen nombres específicos | `SolicitudNoEncontrada`, `ResponsableNoEncontrado` y `ErrorDominio` | Aprobado |
| Los valores permitidos son explícitos | Enumeraciones del dominio | Aprobado |
| No se utilizan variables de una sola letra | Revisión de los archivos de `src/` | Aprobado |
| La estructura de carpetas comunica las responsabilidades | `domain`, `application` e `infrastructure` | Aprobado |

### Resultado de legibilidad

El código utiliza nombres del dominio y evita valores de retorno ambiguos.

La estructura permite localizar las reglas, los casos de uso y los detalles técnicos sin revisar una única clase extensa.

## 6. Checklist de diseño y arquitectura

| Criterio | Evidencia | Resultado |
|---|---|---|
| Se aplica responsabilidad única | Separación entre dominio, aplicación, infraestructura y reportes | Aprobado |
| Los reportes pueden extenderse | `GeneradorReporte`, `ReportePorEstado` y `ReportePorPrioridad` | Aprobado |
| Las interfaces se encuentran separadas | Tres contratos de repositorio | Aprobado |
| El servicio depende de abstracciones | Constructor de `SolicitudService` | Aprobado |
| El dominio no depende de JSON | Los archivos de `src/domain` no importan infraestructura | Aprobado |
| Las reglas se encuentran junto a sus datos | Métodos de `Solicitud` y validación de `Email` | Aprobado |
| La persistencia puede reemplazarse | Repositorios en memoria y JSON | Aprobado |
| Los datos relacionados se agrupan | Objeto `NuevaSolicitud` | Aprobado |
| Se evita la clase gigante inicial | Responsabilidades distribuidas entre módulos | Aprobado |
| Los refactorings están documentados | `docs/REFACTORING.md` | Aprobado |

### Resultado de diseño y arquitectura

La versión refactorizada presenta mayor cohesión y menor acoplamiento que la versión inicial.

El servicio puede utilizar diferentes implementaciones de persistencia sin modificar sus casos de uso.

## 7. Checklist de seguridad

| Criterio | Evidencia | Resultado |
|---|---|---|
| No se incluyen datos personales reales | Datos sintéticos en demo y pruebas | Aprobado |
| El correo se valida antes de persistir | Objeto `Email` | Aprobado |
| Los datos JSON se escriben con codificación explícita | Uso de UTF-8 | Aprobado |
| Los errores no muestran información sensible | Mensajes vinculados con identificadores y validaciones | Aprobado |
| El archivo de datos no se versiona | `datos_demo.json` incluido en `.gitignore` | Aprobado |

### Observación de seguridad

El prototipo no implementa autenticación ni autorización.

Esta limitación se acepta porque el alcance del TPI corresponde a un módulo local de demostración. Una versión productiva debería identificar usuarios y controlar permisos.

## 8. Checklist de rendimiento

| Criterio | Evidencia | Resultado |
|---|---|---|
| No existen bucles anidados innecesarios en los casos de uso | Revisión de `SolicitudService` | Aprobado |
| Los reportes recorren una sola vez las solicitudes | Uso de `Counter` | Aprobado |
| El repositorio en memoria utiliza diccionarios por identificador | `RepositorioMemoria` | Aprobado |
| Las búsquedas por identificador en memoria son directas | Uso de `dict.get()` | Aprobado |
| El tamaño esperado del prototipo es acotado | Alcance definido en la consigna | Aceptado |

### Observación de rendimiento

`RepositorioJson` lee y escribe el archivo completo en cada operación.

Esta decisión resulta aceptable para el prototipo y su volumen reducido. Si el sistema creciera, debería utilizarse una base de datos con operaciones parciales y transacciones.

## 9. Checklist de pruebas

| Criterio | Evidencia | Resultado |
|---|---|---|
| Existen pruebas unitarias | `tests/test_solicitudes.py` | Aprobado |
| Todas las pruebas finalizan correctamente | Ocho pruebas en estado `OK` | Aprobado |
| Se prueba el flujo principal | `test_flujo_principal_conserva_resultado` | Aprobado |
| Se prueban casos inválidos | Correo, estado y solicitud inexistente | Aprobado |
| Se prueba la persistencia | `test_persistencia_json` | Aprobado |
| Las pruebas no dependen de archivos permanentes | Memoria y directorios temporales | Aprobado |
| Se compara el comportamiento antes y después | `docs/PRUEBAS.md` | Aprobado |

## 10. Observaciones y feedback profesional

### Observación 1

La validación del correo comprueba una estructura mínima mediante el carácter `@`.

**Feedback:** La validación resulta suficiente para el alcance académico. Una versión productiva podría incorporar reglas más completas o una biblioteca específica.

**Estado:** aceptada como mejora futura.

### Observación 2

El cambio de estado acepta cualquier valor definido en la enumeración.

**Feedback:** Se conserva este comportamiento para evitar modificar las reglas externas de la versión inicial. Si el negocio definiera un flujo obligatorio, podrían incorporarse transiciones permitidas dentro de `Solicitud`.

**Estado:** aceptada como mejora futura.

### Observación 3

El repositorio JSON reescribe el documento completo.

**Feedback:** La implementación es clara y adecuada para datos acotados. Una base de datos sería más apropiada para concurrencia o grandes volúmenes.

**Estado:** aceptada como límite del prototipo.

### Observación 4

Los tres contratos de repositorio se implementan mediante un único repositorio JSON.

**Feedback:** La separación de contratos evita que la aplicación dependa de operaciones que no necesita. La implementación compartida resulta razonable porque las tres colecciones utilizan el mismo archivo.

**Estado:** aceptada.

## 11. Correcciones verificadas

| Hallazgo inicial | Corrección |
|---|---|
| Clase Gigante | Separación por capas y entidades |
| Método Largo | Extract Method |
| Obsesión por Primitivos | Objetos de dominio y enumeraciones |
| Código Duplicado | Repositorios y métodos de búsqueda centralizados |
| Strings hardcodeados | Enumeraciones |
| Baja cohesión | Módulos con responsabilidades relacionadas |
| Alto acoplamiento | Contratos e inyección de dependencias |
| Baja testabilidad | Repositorio en memoria |
| Retornos `None` y `False` | Excepciones específicas |
| Persistencia mezclada con reglas | Capa de infraestructura |

## 12. Criterio de aceptación final

El código se considera técnicamente aceptado porque:

- Ejecuta correctamente.
- Las ocho pruebas finalizan en `OK`.
- Conserva el resultado del flujo principal.
- Aplica los refactorings obligatorios.
- Mejora cohesión, acoplamiento y testabilidad.
- Maneja errores mediante excepciones.
- Incluye documentación y trazabilidad.
- No utiliza datos personales reales.

## 13. Resultado del code review

**Estado: APROBADO**

No se identificaron observaciones bloqueantes.

Las mejoras futuras registradas no impiden cumplir el alcance del Trabajo Práctico Integrador.
