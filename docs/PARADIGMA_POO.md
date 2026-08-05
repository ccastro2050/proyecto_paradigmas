# El paradigma de Programación Orientada a Objetos (P.O.O.)

> Documento conceptual del curso. Qué es un paradigma, qué propone la P.O.O.,
> por qué este proyecto la usa, y dónde verla funcionando en la versión 1.

---

## 1. ¿Qué es un paradigma de programación?

Un paradigma es una **forma de pensar y organizar los programas**: qué es la
unidad básica de construcción y cómo se combinan. Los grandes paradigmas:

| Paradigma | Unidad básica | Idea central | Ejemplo |
|---|---|---|---|
| **Imperativo/estructurado** | la instrucción y el procedimiento | Secuencia, decisión, ciclo | C, Pascal |
| **Orientado a objetos** | el **objeto** (datos + comportamiento) | Objetos que colaboran enviándose mensajes | Java, C#, Python |
| **Funcional** | la función pura | Transformar datos sin estado mutable | Haskell, Elixir |
| **Declarativo** | la descripción del resultado | Decir QUÉ, no CÓMO | SQL, HTML |

Python es **multiparadigma**: en este proyecto se escribe código estructurado
(dentro de los métodos), orientado a objetos (la arquitectura), declarativo
(el SQL y los modelos Pydantic) y ocasionalmente funcional (comprehensions).
Saber elegir el paradigma para cada problema ES la competencia del curso.

## 2. Los cuatro pilares de la P.O.O.

### 2.1 Abstracción
Quedarse con lo esencial y esconder el detalle. `IRepositorioProducto` es una
abstracción: define QUÉ se puede hacer con productos (obtener, crear,
actualizar, eliminar) sin decir CÓMO ni DÓNDE se guardan.

### 2.2 Encapsulamiento
Cada objeto guarda su estado y expone solo operaciones. En la v1,
`RepositorioProductoPostgreSQL` encapsula el engine de conexión y el SQL: nadie
más en el sistema sabe que existe una cadena de conexión.

### 2.3 Herencia (y por qué aquí casi no se usa)
Reutilizar definiendo una clase a partir de otra ("es-un"). Es el pilar más
famoso y el más **sobreutilizado**: la herencia acopla fuerte. La regla moderna
es **composición sobre herencia** — y este proyecto la sigue: `ServicioProducto`
no HEREDA de un repositorio, RECIBE un repositorio (composición + inyección).

### 2.4 Polimorfismo
Distintas clases responden al mismo mensaje, cada una a su manera. Es el pilar
que sostiene todo el proyecto: cualquier clase que cumpla
`IRepositorioProducto` puede ocupar el lugar de otra — el PostgreSQL real, el
falso en memoria de las pruebas, o el MariaDB que llegará en la v3.

## 3. La P.O.O. en Python: particularidades que este proyecto explota

- **Todo es un objeto** (números, funciones, clases, módulos).
- **Duck typing:** a Python no le importa el árbol de herencia sino que el
  objeto "sepa responder" — si tiene los métodos, sirve.
- **`typing.Protocol` (PEP 544) = polimorfismo estructural verificable:** un
  contrato que las clases cumplen SIN heredar. Es la versión formal del duck
  typing y la forma en que este proyecto declara sus interfaces:

```python
class IRepositorioProducto(Protocol):
    async def obtener_todos(self, limite: int) -> list[dict]: ...
    async def obtener_por_codigo(self, codigo: str) -> dict | None: ...
    async def crear(self, datos: dict) -> bool: ...
    async def actualizar(self, codigo: str, datos: dict) -> int: ...
    async def eliminar(self, codigo: str) -> int: ...
```

Compárelo con `interface` de Java/C#: mismo propósito, pero sin obligar a
`implements` — cumplir el contrato basta (tipado estructural, no nominal).

## 4. Justificación: por qué P.O.O. para este proyecto

1. **El dominio se modela solo:** producto, factura, cliente… son objetos
   naturales con datos y reglas propias.
2. **El polimorfismo es EL requisito:** la meta del proyecto (cambiar de motor
   de BD sin tocar código) es literalmente un ejercicio de polimorfismo — tres
   repositorios intercambiables tras una interfaz.
3. **Probabilidad de prueba:** el criterio de aceptación 6 de la v1 (probar el
   servicio con un repositorio falso en memoria) solo es posible porque el
   servicio depende de una abstracción, no de PostgreSQL.
4. **Puente a SOLID:** los principios SOLID (documento
   [SOLID_Y_CAPAS.md](SOLID_Y_CAPAS.md)) son reglas de diseño **dentro** del
   paradigma orientado a objetos — sin P.O.O. no hay SOLID que aplicar.

## 5. Ejemplo resumido: la v1 vista con lentes de P.O.O.

```
Producto (Pydantic)          ← objeto de DATOS con validación (abstracción del dominio)
ServicioProducto             ← objeto de NEGOCIO; compone un IRepositorioProducto
IRepositorioProducto         ← contrato (Protocol): abstracción pura
RepositorioProductoPostgreSQL ← implementación concreta (encapsula SQL y conexión)
RepositorioFalsoEnMemoria    ← otra implementación (¡polimorfismo!) para probar sin BD
```

El mismo `ServicioProducto` funciona con ambos repositorios sin cambiar una
línea — eso es el paradigma haciendo su trabajo. En la v3, un tercer objeto
(`RepositorioProductoMysqlMariaDB`) entrará por la misma puerta.

## 6. Referencias

1. Python — Tutorial oficial de clases:
   <https://docs.python.org/es/3/tutorial/classes.html>
2. PEP 544 — *Protocols: Structural subtyping (static duck typing)*:
   <https://peps.python.org/pep-0544/>
3. Refactoring Guru (es) — catálogo de patrones de diseño orientados a objetos:
   <https://refactoring.guru/es/design-patterns>
4. Gamma, Helm, Johnson, Vlissides — *Design Patterns* (GoF, 1994): el origen
   de "composición sobre herencia" y "programar contra interfaces".
5. Alan Kay (creador del término "object-oriented", Smalltalk): la idea
   original era **objetos que se comunican por mensajes** — más cercana a
   "servicios que colaboran" que a "árboles de herencia".
6. En este repositorio: las interfaces y capas de la
   [v1](spec_kit/versiones/v1_producto_postgres/3_plan.md).
