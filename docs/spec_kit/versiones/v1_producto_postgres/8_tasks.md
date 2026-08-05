# Tareas — Versión 1: api_facturas con producto + PostgreSQL

> **Versión 1** · El orden de construcción, partiendo de CERO. Cada fase termina
> en algo **verificable**. Requisitos: [2_spec.md](2_spec.md) · técnica:
> [3_plan.md](3_plan.md) · contratos: [6_contracts.md](6_contracts.md) ·
> validación final: [7_quickstart.md](7_quickstart.md).

---

## Fase 0 — Base de datos y esqueleto
- [ ] Guardar el `init.sql` de [5_data_model.md](5_data_model.md) §2 en
      `db/init.sql` y montar PostgreSQL con la receta de §3.
- [ ] Crear la carpeta `api_facturas/` con subcarpetas `models/`,
      `controllers/`, `servicios/` (`abstracciones/`), `repositorios/`
      (`abstracciones/`) y sus `__init__.py`.
- [ ] `requirements.txt`: fastapi, uvicorn, sqlalchemy[asyncio], asyncpg,
      greenlet, pydantic.
- [ ] Entorno virtual + `pip install -r requirements.txt`.

**Verificar:** `python -c "import fastapi, sqlalchemy, asyncpg"` no falla, y un
cliente SQL ve la tabla `producto` con 8 filas.

## Fase 1 — Modelo Pydantic
- [ ] `models/producto.py`: `Producto` (todos obligatorios, `stock ≥ 0`,
      `valorunitario ≥ 0`) y `ProductoActualizar` (todos opcionales, mismas
      restricciones) — según [3_plan.md](3_plan.md) §4.2.

**Verificar:** en un REPL, `Producto(codigo="X", nombre="Y", stock=-1,
valorunitario=1)` lanza `ValidationError`.

## Fase 2 — Contratos (interfaces)
- [ ] `repositorios/abstracciones/i_repositorio_producto.py`: Protocol con los
      5 métodos async (`obtener_todos`, `obtener_por_codigo`, `crear`,
      `actualizar`, `eliminar`).
- [ ] `servicios/abstracciones/i_servicio_producto.py`: Protocol del servicio.

**Verificar:** los archivos importan sin errores (son solo contratos).

## Fase 3 — Repositorio PostgreSQL
- [ ] `repositorios/repositorio_producto_postgresql.py`: engine async perezoso,
      los 5 métodos con SQL parametrizado de [3_plan.md](3_plan.md) §4.4,
      `Decimal` → float al serializar.

**Verificar:** un script suelto instancia el repositorio con `DB_POSTGRES` y
lista los 8 productos.

## Fase 4 — Servicio (y la prueba de capas)
- [ ] `servicios/servicio_producto.py`: recibe `IRepositorioProducto` por
      constructor; valida código no vacío; traduce "no encontrado" a
      `LookupError`.
- [ ] `servicios/ensamblador.py`: `crear_servicio_producto()` — las 3 líneas de
      [3_plan.md](3_plan.md) §4.3 (sin fábrica multi-motor: eso es v3).

**Verificar (criterio 6 de la spec):** un script instancia `ServicioProducto`
con un **repositorio falso en memoria** (una clase con los 5 métodos sobre un
dict) y hace crear/listar/eliminar SIN PostgreSQL corriendo. Si esto funciona,
las capas quedaron bien.

## Fase 5 — Controller y aplicación
- [ ] `controllers/producto_controller.py`: los 5 endpoints de
      [6_contracts.md](6_contracts.md) con la traducción de excepciones de
      [3_plan.md](3_plan.md) §4.5 (ValueError→400, LookupError→404, resto→500)
      y el 204 para lista vacía.
- [ ] `main.py`: app FastAPI (`title="API Facturas"`, `version="v1"`),
      `include_router(prefix="/api")`, endpoint `/` de diagnóstico.

**Verificar:** `uvicorn main:app --port 8002 --reload` y en `/docs` probar:
listar (200 con 8), obtener PR001 (200), PR999 (404), POST inválido (422).

## Fase 6 — Cierre de la versión
- [ ] Correr el smoke test completo de [7_quickstart.md](7_quickstart.md) §3 —
      equivale a los 6 criterios de aceptación de [2_spec.md](2_spec.md) §5.
- [ ] `.gitignore` (`__pycache__/`, `.venv/`, `.env*`).
- [ ] Commit y tag `v1`.

**La v1 está TERMINADA.** Solo ahora se escribe la spec de la v2
([mapa de versiones](../0_mapa_versiones.md)).
