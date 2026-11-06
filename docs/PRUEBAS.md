# Pruebas y verificación del comportamiento

## Objetivo

Verificar que el refactoring no haya alterado negativamente el comportamiento externo del sistema.

La versión inicial y la versión refactorizada deben conservar las operaciones principales:

- Registrar estudiantes.
- Registrar responsables.
- Registrar solicitudes.
- Asignar responsables.
- Cambiar estados.
- Buscar solicitudes.
- Generar reportes.
- Persistir datos en JSON.

## Estrategia

Las reglas y los casos de uso se prueban mediante `RepositorioMemoria`. Esto permite ejecutar pruebas unitarias sin depender de archivos permanentes.

La persistencia se verifica por separado mediante `RepositorioJson` y un directorio temporal.

## Casos automatizados

| Caso | Resultado esperado | Resultado |
|---|---|---|
| Flujo principal | Una solicitud termina en estado RESUELTA | Aprobado |
| Filtro por prioridad | Solo devuelve solicitudes con prioridad ALTA | Aprobado |
| Correo inválido | Lanza `ErrorDominio` con un mensaje claro | Aprobado |
| Estado inexistente | El valor es rechazado por `Estado` | Aprobado |
| Persistencia JSON | La solicitud puede guardarse y recuperarse | Aprobado |
| Asignación de responsable | La solicitud pasa a EN_PROCESO | Aprobado |
| Solicitud inexistente | Lanza `SolicitudNoEncontrada` | Aprobado |
| Reporte por prioridad | Devuelve los conteos BAJA, MEDIA y ALTA | Aprobado |

## Comparación antes y después

En ambas versiones se ejecutó el mismo flujo:

1. Registrar un estudiante.
2. Registrar un responsable.
3. Registrar una solicitud.
4. Asignar el responsable.
5. Cambiar el estado a RESUELTA.
6. Generar el reporte por estado.

El resultado observable en ambas versiones fue:

```text
{'PENDIENTE': 0, 'EN_PROCESO': 0, 'RESUELTA': 1, 'CERRADA': 0}