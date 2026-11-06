# Diagnóstico técnico de la versión inicial

## 1. Sistema analizado

El proyecto implementa un Sistema de Gestión de Solicitudes Académicas. Permite registrar estudiantes y responsables, crear solicitudes, asignarlas, cambiar sus estados, filtrarlas y generar un reporte.

La versión inicial cumple las funciones esperadas. El diagnóstico analiza su calidad interna antes de realizar el refactoring.

## 2. Marco teórico utilizado

La calidad externa representa lo que percibe el usuario. Incluye que el software haga lo que debe, no falle y responda adecuadamente.

La calidad interna describe cómo está construido el código. Se relaciona con:

- Legibilidad.
- Bajo acoplamiento.
- Alta cohesión.
- Testabilidad.
- Modularidad.
- Mantenibilidad.

La deuda técnica representa el costo futuro provocado por tomar atajos o mantener una base con problemas de diseño. Sus intereses aparecen como cambios más lentos, mayor cantidad de errores y mayor costo de mantenimiento.

Un code smell es una señal de un posible problema de diseño. No representa necesariamente un bug.

## 3. Calidad externa

Desde la perspectiva del usuario, el sistema permite:

- Registrar estudiantes.
- Registrar responsables académicos.
- Crear solicitudes.
- Asignar responsables.
- Cambiar estados.
- Buscar por estado, prioridad o tipo.
- Generar un reporte.
- Persistir los datos en JSON.

Las pruebas automatizadas confirman el flujo principal, los filtros, las validaciones básicas y la persistencia.

Por lo tanto, la calidad externa resulta suficiente para el alcance inicial.

## 4. Calidad interna

Aunque el sistema funciona, la estructura presenta dificultades:

- Una clase concentra varias responsabilidades.
- Los conceptos del dominio se representan mediante tipos primitivos.
- Existen valores hardcodeados.
- La lógica depende directamente de JSON y del sistema de archivos.
- Los errores se comunican mediante `None` o `False`.
- Algunos métodos realizan más de una tarea.
- La búsqueda de entidades repite estructuras similares.
- La lógica de negocio y la persistencia están acopladas.

Estos problemas no siempre son visibles para el usuario, pero aumentan el costo del cambio.

## 5. Code smells identificados

### CS-01 Clase Gigante o Large Class

**Ubicación:** clase `GestorAcademico`.

**Evidencia:** la clase registra estudiantes, registra responsables, crea solicitudes, asigna responsables, cambia estados, busca registros, genera reportes y persiste datos.

**Problema:** acumula una cantidad excesiva de responsabilidades.

**Impacto:** presenta baja cohesión y varias razones para cambiar.

**Riesgo:** un cambio en cualquier parte del sistema puede afectar la misma clase.

**Prioridad:** alta.

### CS-02 Método Largo o Long Method

**Ubicación:** método `asignar_responsable()`.

**Evidencia:** busca una solicitud, busca un responsable, valida ambos resultados, realiza la asignación, modifica el estado y guarda los datos.

**Problema:** intenta realizar varias tareas dentro del mismo método.

**Impacto:** dificulta la lectura y las pruebas aisladas.

**Riesgo:** una modificación puede alterar varias partes del flujo.

**Prioridad:** alta.

### CS-03 Obsesión por Primitivos en los estados

**Ubicación:** métodos `registrar_solicitud()`, `cambiar_estado()` y `generar_reporte()`.

**Evidencia:** estados, prioridades y tipos se representan con cadenas como `"PENDIENTE"`, `"ALTA"` y `"CERTIFICADO"`.

**Problema:** se utilizan tipos básicos para representar conceptos del dominio.

**Impacto:** el código permite valores incorrectos o errores de escritura.

**Riesgo:** las reglas pueden quedar inconsistentes entre métodos.

**Prioridad:** alta.

### CS-04 Obsesión por Primitivos en el correo electrónico

**Ubicación:** método `registrar_estudiante()`.

**Evidencia:** el correo se representa mediante un `str` y se valida buscando el carácter `@`.

**Problema:** un concepto del dominio con reglas propias se representa mediante un tipo básico.

**Impacto:** la validación queda dentro del gestor y resulta muy limitada.

**Riesgo:** pueden aceptarse correos con formatos incorrectos.

**Prioridad:** media.

### CS-05 Código Duplicado o Duplicated Code

**Ubicación:** `registrar_solicitud()`, `asignar_responsable()` y `cambiar_estado()`.

**Evidencia:** distintos métodos recorren listas manualmente para localizar estudiantes, responsables o solicitudes por identificador.

**Problema:** se repite la misma estructura de búsqueda.

**Impacto:** cualquier mejora en la búsqueda deberá aplicarse en varios lugares.

**Riesgo:** pueden aparecer implementaciones inconsistentes.

**Prioridad:** media.

## 6. Debilidades técnicas complementarias

La consigna permite registrar code smells o debilidades técnicas. Las siguientes debilidades pertenecen a los conceptos de calidad interna y Clean Code desarrollados en la materia.

### DT-06 Strings hardcodeados

**Ubicación:** listas de tipos, prioridades y estados válidos.

**Evidencia:** los valores aparecen escritos directamente dentro de métodos y estructuras de reporte.

**Problema:** para agregar o cambiar un valor es necesario modificar distintos sectores del código.

**Impacto:** reduce la extensibilidad y la legibilidad.

**Riesgo:** pueden quedar valores desactualizados o contradictorios.

**Prioridad:** alta.

### DT-07 Baja cohesión

**Ubicación:** clase `GestorAcademico`.

**Evidencia:** la clase contiene operaciones sobre estudiantes, responsables, solicitudes, archivos y reportes.

**Problema:** sus elementos no se relacionan con una única responsabilidad.

**Impacto:** la clase resulta difícil de comprender y mantener.

**Riesgo:** continuará creciendo cada vez que se agregue una funcionalidad.

**Prioridad:** alta.

### DT-08 Alto acoplamiento

**Ubicación:** constructor y método `guardar()`.

**Evidencia:** `GestorAcademico` depende directamente de `Path`, JSON y un archivo concreto.

**Problema:** la lógica de negocio conoce los detalles de persistencia.

**Impacto:** reemplazar JSON por una base de datos obligaría a modificar la clase principal.

**Riesgo:** puede producirse un efecto dominó ante cambios tecnológicos.

**Prioridad:** alta.

### DT-09 Baja testabilidad

**Ubicación:** funcionamiento general de `GestorAcademico`.

**Evidencia:** incluso las pruebas de reglas de negocio necesitan crear archivos temporales.

**Problema:** no es posible probar completamente los casos de uso sin involucrar la persistencia.

**Impacto:** las pruebas tienen más preparación y mezclan distintos niveles.

**Riesgo:** a medida que crezca el sistema, las pruebas serán más lentas y difíciles de aislar.

**Prioridad:** media.

### DT-10 Manejo de errores mediante valores de retorno

**Ubicación:** métodos de registro, asignación y cambio de estado.

**Evidencia:** los errores se comunican mediante `None` o `False`.

**Problema:** Clean Code recomienda utilizar excepciones en lugar de códigos o valores de error.

**Impacto:** el llamador no puede conocer con precisión qué validación falló.

**Riesgo:** pueden ignorarse errores o mostrarse mensajes poco claros.

**Prioridad:** alta.

## 7. Code smell de Demasiados Parámetros

El material define Demasiados Parámetros o Long Parameter List como métodos que generalmente reciben cinco o más argumentos.

`registrar_solicitud()` recibe cuatro argumentos además de `self`:

- `estudiante_id`
- `tipo`
- `descripcion`
- `prioridad`

Por lo tanto, no se registra como code smell en esta versión inicial.

Sin embargo, estos datos se relacionan entre sí y viajan juntos. Más adelante se podrá justificar Introduce Parameter Object como una mejora de claridad y evolución, sin afirmar incorrectamente que el método ya supera el límite indicado por la teoría.

## 8. Relación con la deuda técnica

La deuda técnica de la versión inicial no se debe a falta de funcionamiento ni a ausencia de pruebas.

Surge principalmente de decisiones de diseño utilizadas para construir rápidamente el prototipo:

- Centralizar las responsabilidades en una clase.
- Representar conceptos del dominio con cadenas.
- Acoplar la lógica al archivo JSON.
- Repetir búsquedas manuales.
- Comunicar errores con `None` y `False`.

Los intereses de esta deuda aparecerían al agregar nuevos tipos, estados, reportes o mecanismos de persistencia. Cada cambio requeriría modificar más sectores del sistema y aumentaría el riesgo de errores.

## 9. Síntomas de rigidez, fragilidad e inmovilidad

### Rigidez

Cambiar el mecanismo de persistencia requiere modificar `GestorAcademico`, que también contiene los casos de uso.

### Fragilidad

Modificar las cadenas que representan estados puede afectar el registro, el cambio de estado, los filtros y el reporte.

### Inmovilidad

Las reglas de solicitudes no pueden reutilizarse fácilmente sin llevar también la dependencia de archivos y JSON.

## 10. Criterios para el refactoring

La versión refactorizada deberá:

- Mantener el comportamiento externo.
- Separar las responsabilidades.
- Aumentar la cohesión.
- Reducir el acoplamiento.
- Mejorar la testabilidad.
- Reemplazar valores hardcodeados por conceptos del dominio.
- Utilizar excepciones con mensajes claros.
- Aplicar Extract Method.
- Aplicar Move Method.
- Aplicar Introduce Parameter Object.
- Evitar código duplicado.
- Conservar las pruebas existentes y agregar nuevos casos.

## 11. Conclusión

La versión inicial tiene una calidad externa adecuada porque cumple las funciones principales. Sin embargo, su calidad interna presenta una Clase Gigante, un Método Largo, Obsesión por Primitivos y Código Duplicado.

También se observan strings hardcodeados, baja cohesión, alto acoplamiento, baja testabilidad y manejo de errores mediante valores de retorno.

Estas señales justifican un refactoring seguro respaldado por pruebas. El objetivo será mejorar la estructura interna sin alterar negativamente el comportamiento que percibe el usuario.