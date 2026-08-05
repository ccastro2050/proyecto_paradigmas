# Especificación — Versión 1 del proyecto: api_facturas con producto + PostgreSQL

> **Versión 1** del desarrollo incremental ([mapa de versiones](../0_mapa_versiones.md)).
> Rige la constitución del proyecto: [../../1_constitution.md](../../1_constitution.md).
> En v1 el sistema completo ES esto: **no existe frontend, no existe API
> genérica, no hay más tablas ni más motores.**
>
> | Documento de esta versión | Contenido |
> |---|---|
> | **2_spec.md** (este) | QUÉ construir en v1 y sus criterios de aceptación |
> | [3_plan.md](3_plan.md) | CÓMO: stack, estructura y diseño de las capas |
> | [5_data_model.md](5_data_model.md) | La tabla `producto` (DDL + datos de ejemplo) |
> | [6_contracts.md](6_contracts.md) | Los 6 endpoints con formatos exactos |
> | [7_quickstart.md](7_quickstart.md) | Arranque y smoke test |
> | [8_tasks.md](8_tasks.md) | Orden de construcción por fases verificables |

---

## 1. Propósito de la v1

Construir la **primera rebanada vertical** de la API de facturación: el CRUD
completo de **una sola entidad (`producto`)** contra **un solo motor
(PostgreSQL)** — pero con la **arquitectura en capas completa desde el primer
día**: controller → servicio → repositorio, comunicados por interfaces.

La v1 es pequeña a propósito: su valor no está en la funcionalidad sino en
dejar el **esqueleto arquitectónico correcto** sobre el que las versiones
siguientes agregan tablas (v2), motores (v3, v4), la API genérica (v5) y el
frontend (v6) **sin reescribir lo construido**.

## 2. Alcance

**Incluye:**
- CRUD de `producto`: listar, obtener por código, crear, actualizar, eliminar.
- Validación **Pydantic** de la entidad (tipos, obligatorios, no-negativos).
- Capas con interfaces: `IRepositorioProducto` (Protocol) implementada por
  `RepositorioProductoPostgreSQL`; el servicio depende de la interfaz.
- Configuración por variable de entorno (`DB_POSTGRES`); PostgreSQL en Docker.
- Swagger automático (`/docs`) y endpoint `/` de diagnóstico.

**No incluye (y es deliberado — ver [mapa de versiones](../0_mapa_versiones.md)):**
- **Ningún frontend** (llega en v6) y **ninguna API genérica** (llega en v5).
- Otras tablas (v2) · otros motores y la fábrica `DB_PROVIDER` (v3, v4) ·
  docker compose e imagen propia (v4).
- Autenticación, triggers/SPs de facturación (llegan con `factura` en v2+).

## 3. Requisitos funcionales

### RF1 — Listar productos
`GET /api/producto` → 200 con envoltura `{tabla, total, datos:[…]}`;
tabla vacía → **204** sin cuerpo.

### RF2 — Obtener por código
`GET /api/producto/{codigo}` → 200 con el producto; inexistente → 404.

### RF3 — Crear producto
`POST /api/producto` con body validado por Pydantic
(`codigo`, `nombre`, `stock ≥ 0`, `valorunitario ≥ 0`).
Éxito → 200 `{estado, mensaje}`; body inválido → **422** (detalle de Pydantic);
código duplicado → 500 con el error del motor en `detalle`.

### RF4 — Actualizar producto
`PUT /api/producto/{codigo}` con body Pydantic (campos a cambiar).
Devuelve `filasAfectadas`; código inexistente → 404.

### RF5 — Eliminar producto
`DELETE /api/producto/{codigo}`. Devuelve `filasEliminadas`;
inexistente → 404.

### RF6 — Diagnóstico
`GET /` → JSON con mensaje, versión (`"v1"`) y ruta de documentación.

## 4. Requisitos no funcionales

- **RNF1 — Capas estrictas:** el controller no toca SQL; el servicio no conoce
  FastAPI ni el motor; el repositorio no conoce HTTP. Interfaces por `Protocol`.
- **RNF2 — Asíncrona:** driver async (asyncpg vía SQLAlchemy `text()`).
- **RNF3 — SQL parametrizado siempre** (`:param`); nada de concatenar valores.
- **RNF4 — Errores uniformes:** `{estado, mensaje, detalle}`;
  ValueError→400 · LookupError→404 · resto→500.
- **RNF5 — Sin anticipación:** ni fábrica multi-motor ni `DB_PROVIDER` en v1
  (los introduce la v3 cuando exista el segundo motor).

## 5. Criterios de aceptación

1. PostgreSQL arranca con el `init.sql` de [5_data_model.md](5_data_model.md)
   y `uvicorn main:app --port 8002` levanta la API; `GET /` responde el JSON
   de diagnóstico y `/docs` abre Swagger.
2. `GET /api/producto` devuelve los 8 productos de ejemplo con
   `{tabla:"producto", total:8, datos:[…]}`.
3. `GET /api/producto/PR001` devuelve la Laptop Lenovo; `/api/producto/PR999`
   responde 404 con mensaje claro.
4. Ciclo completo: `POST` crea `PR009` → `PUT` le cambia el stock →
   `GET` lo confirma → `DELETE` lo elimina (200/200/200/200) y un segundo
   `DELETE` responde 404.
5. `POST` con `stock: -5` o sin `nombre` → **422** (lo rechaza Pydantic, nunca
   llega a la BD); `POST` con código duplicado → 500 con el error del motor.
6. Prueba de capas (la evidencia de que la arquitectura quedó bien): el
   servicio se puede probar con un repositorio **falso** en memoria que cumpla
   `IRepositorioProducto`, sin PostgreSQL corriendo.

## 6. Definición de TERMINADA

Los 6 criterios pasan → commit + tag `v1` → recién entonces se escribe la spec
de la v2 ([mapa](../0_mapa_versiones.md)).
