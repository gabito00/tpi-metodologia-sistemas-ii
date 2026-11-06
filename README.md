# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de Metodología de Sistemas II.

El proyecto demuestra la evolución de una versión inicial funcional hacia una estructura con mayor cohesión, menor acoplamiento y mejor capacidad de prueba.

## Funcionalidades

- Registrar estudiantes.
- Registrar responsables académicos.
- Registrar solicitudes.
- Asignar responsables.
- Cambiar estados.
- Buscar por estado, prioridad o tipo.
- Generar reportes.
- Persistir los datos en JSON.
- Ejecutar pruebas sin depender de archivos permanentes.

## Tecnologías

- Python 3.11 o superior.
- Biblioteca estándar.
- unittest.
- Persistencia JSON.
- Git y GitHub.

El proyecto no requiere dependencias externas.

## Estructura

```text
.
├── app.py
├── README.md
├── src
│   ├── application
│   │   ├── reportes.py
│   │   ├── repositorios.py
│   │   └── solicitud_service.py
│   ├── domain
│   │   ├── email.py
│   │   ├── errores.py
│   │   ├── estudiante.py
│   │   ├── responsable.py
│   │   └── solicitud.py
│   └── infrastructure
│       ├── repositorio_json.py
│       └── repositorio_memoria.py
├── tests
│   └── test_solicitudes.py
└── docs
    ├── CODE_REVIEW.md
    ├── DIAGNOSTICO.md
    ├── PRUEBAS.md
    ├── REFACTORING.md
    └── USO_IA.md
```

## Capas

### Dominio

Contiene las entidades y las reglas del negocio. No conoce archivos, JSON ni otros detalles de infraestructura.

### Aplicación

Coordina los casos de uso y define los contratos de persistencia. Depende del dominio y de abstracciones.

### Infraestructura

Implementa los contratos de persistencia. Incluye una implementación JSON para la ejecución y otra en memoria para las pruebas.

### Pruebas

Verifican el comportamiento mediante un repositorio en memoria y archivos temporales.

## Ejecución

```bash
python app.py
```

La primera ejecución sobre un archivo vacío produce:

```text
{'PENDIENTE': 0, 'EN_PROCESO': 0, 'RESUELTA': 1, 'CERRADA': 0}
```

El archivo `datos_demo.json` conserva los datos entre ejecuciones.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

## Refactorings aplicados

### Extract Method

Se extrajeron métodos privados para crear solicitudes, validar estudiantes, buscar responsables, buscar solicitudes y evaluar filtros.

### Move Method

La asignación de responsables y el cambio de estado pasaron de la clase gestora a la entidad `Solicitud`.

### Introduce Parameter Object

Los datos necesarios para registrar una solicitud se agruparon en `NuevaSolicitud`.

### Separación de responsabilidades

La clase inicial se dividió en dominio, aplicación, infraestructura y reportes.

## Principios aplicados

- SRP: cada módulo tiene una responsabilidad concreta.
- OCP: se pueden agregar reportes sin modificar el servicio.
- ISP: los contratos de repositorio se encuentran separados por entidad.
- DIP: el servicio depende de contratos y no de JSON.
- Clean Code: nombres del dominio, funciones pequeñas y excepciones específicas.

## Versiones y tags

- `estado-inicial`: versión funcional anterior al diagnóstico.
- `etapa-diagnostico`: diagnóstico de calidad y deuda técnica.
- `etapa-refactoring`: versión reorganizada mediante refactoring seguro.
- `etapa-pruebas`: ampliación y documentación de las pruebas.
- `estado-refactorizado`: versión final del código verificada.
- `etapa-docs`: documentación técnica completa.

## Datos

Todos los nombres y correos utilizados son sintéticos. El proyecto no contiene datos personales reales.
