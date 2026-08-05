# Proyecto Paradigmas — construcción por versiones

Proyecto del curso **Paradigmas de Programación** (USB Medellín). Aquí NO se
clona un sistema terminado: **se construye un sistema real por versiones**,
siguiendo especificaciones (spec-driven development). Cada versión es pequeña,
verificable y deja el terreno listo para la siguiente.

```
v1  api_facturas: CRUD de producto, solo PostgreSQL   ← USTED ESTÁ AQUÍ
v2  más tablas (persona, factura maestro-detalle…)
v3  segundo motor (MariaDB) — nace la fábrica y DB_PROVIDER
v4  tercer motor (SQL Server) + docker compose completo
v5  API genérica (/api/{tabla})
v6  frontend Flask
```

## Cómo se trabaja

1. Lea la **constitución** — las reglas permanentes del proyecto:
   [docs/spec_kit/1_constitution.md](docs/spec_kit/1_constitution.md)
2. Lea el **mapa de versiones** — la ruta completa y sus reglas:
   [docs/spec_kit/versiones/0_mapa_versiones.md](docs/spec_kit/versiones/0_mapa_versiones.md)
3. Construya la **versión actual** siguiendo su spec kit — empiece por la spec
   y termine con las tareas:

| Documento de la v1 | Qué contiene |
|---|---|
| [2_spec.md](docs/spec_kit/versiones/v1_producto_postgres/2_spec.md) | QUÉ construir y los 6 criterios de aceptación |
| [3_plan.md](docs/spec_kit/versiones/v1_producto_postgres/3_plan.md) | CÓMO: stack, carpetas, capas e interfaces |
| [5_data_model.md](docs/spec_kit/versiones/v1_producto_postgres/5_data_model.md) | La tabla `producto` (DDL completo + cómo montar PostgreSQL) |
| [6_contracts.md](docs/spec_kit/versiones/v1_producto_postgres/6_contracts.md) | Los 6 endpoints con formatos exactos |
| [7_quickstart.md](docs/spec_kit/versiones/v1_producto_postgres/7_quickstart.md) | Smoke test para validar lo construido |
| [8_tasks.md](docs/spec_kit/versiones/v1_producto_postgres/8_tasks.md) | Las 7 fases de construcción, en orden |

4. Una versión está **TERMINADA** cuando pasa todos sus criterios de
   aceptación. Se cierra con commit + tag (`v1`), y solo entonces aparece la
   spec de la siguiente.

## Qué se necesita

- **Docker Desktop** (para PostgreSQL; la API corre local en v1).
- **Python 3.12** y un editor (VS Code recomendado).
- Saber que la especificación manda: si el código hace algo que la spec no
  dice, se corrige el código o se corrige la spec — nunca se dejan divergir.

## Puesta en marcha de la v1 (resumen)

```powershell
git clone https://github.com/ccastro2050/proyecto_paradigmas.git
cd proyecto_paradigmas
# seguir docs/spec_kit/versiones/v1_producto_postgres/8_tasks.md fase por fase
```

---

*Proyecto Paradigmas · USB Med · La rama `sistema-completo` conserva el sistema
de referencia terminado (consultarla es decisión del profesor, no un atajo).*
