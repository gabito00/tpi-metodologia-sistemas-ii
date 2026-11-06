# Declaración de uso de inteligencia artificial

## Herramienta utilizada

Durante el trabajo se utilizó ChatGPT Codex como herramienta de apoyo.

## Participación del alumno

Desarrolló el trabajo de manera incremental. Creó y administró el repositorio, incorporó y adaptó el código, tomó las decisiones de organización, realizó los commits y tags, ejecutó las pruebas y verificó el comportamiento de las distintas versiones.

También revisó las propuestas con el material teórico de la materia y solicitó correcciones cuando una sugerencia no coincidía con los conceptos desarrollados por la cátedra.

## Apoyo brindado por la herramienta

La inteligencia artificial se utilizó como asistente para:

- Preparar un borrador del código inicial.
- Revisar las modificaciones realizadas durante el refactoring.
- Analizar alternativas de separación de responsabilidades.
- Comprobar la relación de los cambios con SOLID y Clean Code.
- Proponer casos de prueba para verificar el comportamiento.
- Ayudar a organizar y redactar el informe final.

## Modalidad de trabajo

El código se trabajó por etapas. El alumno incorporó los cambios en su repositorio y ejecutó el sistema después de cada modificación. Las observaciones de la herramienta se utilizaron como recomendaciones y fueron aceptadas, modificadas o rechazadas según el resultado de las pruebas y la teoría de la asignatura.

Durante el proceso, el alumno propuso separar las entidades y organizar el proyecto en capas de dominio, aplicación e infraestructura. También detectó problemas de importación, corrigió la ubicación de archivos y comprobó la trazabilidad del trabajo mediante Git.

## Verificación

El alumno verificó el sistema mediante:

```bash
python app.py
python -m unittest discover -s tests -v
```

También comprobó el historial y el estado del repositorio mediante:

```bash
git log --oneline --decorate
git status
```

La versión inicial y la versión refactorizada produjeron el mismo resultado para el flujo principal. La versión final completó ocho pruebas automatizadas correctamente.

## Declaración final

La inteligencia artificial funcionó como herramienta de consulta, revisión y apoyo en la redacción. Las decisiones, la integración del proyecto, la construcción del historial, la ejecución de las pruebas y la verificación final fueron realizadas por el alumno.
