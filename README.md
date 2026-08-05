# Proyecto Paradigmas — construcción por versiones

Proyecto del curso **Paradigmas de Programación** (USB Medellín). Aquí NO se
descarga un sistema terminado: **se construye un sistema real por versiones**,
guiado por especificaciones. El repositorio siempre contiene la **versión en
curso, funcionando** — usted la ejecuta, la estudia y luego la **reconstruye
desde cero** en su propio proyecto.

---

## 1. Cómo le trabaja el estudiante (léame primero)

### Qué necesita instalado (una sola vez)

| Herramienta | Para qué |
|---|---|
| **Git** | Clonar el repositorio y traer versiones nuevas |
| **Docker Desktop** | La base de datos corre en un contenedor (no se instala PostgreSQL) |
| **Python 3.12** | El lenguaje de la API |
| **VS Code** | El editor — y su terminal integrada (*Terminal → New Terminal*) |

### Primera vez: cargar y EJECUTAR la versión del repositorio

Copie estos comandos en la terminal integrada de VS Code, en orden:

```powershell
# 1) Clonar el repositorio y entrar
git clone https://github.com/ccastro2050/proyecto_paradigmas.git
cd proyecto_paradigmas

# 2) Levantar la base de datos (un contenedor con TODO cargado: db/init.sql)
docker run -d --name bd_v1 -p 15432:5432 `
  -e POSTGRES_DB=bdfacturas_postgres_local `
  -e POSTGRES_USER=paradigmas -e POSTGRES_PASSWORD=paradigmas123 `
  -v ${PWD}/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro `
  postgres:16-alpine

# 3) Crear el entorno virtual de Python e instalar las dependencias
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r api_facturas/requirements.txt

# 4) Arrancar la API
$env:DB_POSTGRES = "postgresql+asyncpg://paradigmas:paradigmas123@localhost:15432/bdfacturas_postgres_local"
cd api_facturas
uvicorn main:app --port 8002 --reload
```

**Listo.** Abra http://localhost:8002/docs — ahí está Swagger para probar
todos los endpoints (pruebe: PUT con solo `{"stock": 99}` → 422; el mismo
body en PATCH → 200. Esa diferencia es parte de lo que enseña la v1).

### Los días siguientes (volver a encender)

```powershell
docker start bd_v1                    # la BD conserva sus datos
cd proyecto_paradigmas
.\.venv\Scripts\Activate.ps1
$env:DB_POSTGRES = "postgresql+asyncpg://paradigmas:paradigmas123@localhost:15432/bdfacturas_postgres_local"
cd api_facturas
uvicorn main:app --port 8002 --reload
```

### Cuando hay cambios

| Qué cambió | Qué hacer |
|---|---|
| **Usted edita un `.py`** | **Nada** — `--reload` reinicia la API sola al guardar |
| **El profesor publicó una versión nueva** | `git pull` en la carpeta clonada (y `pip install -r api_facturas/requirements.txt` si cambiaron dependencias) |
| **Quiere resetear la BD** a sus datos originales | `docker rm -f bd_v1` y repetir el paso 2 de la primera vez |
| **La BD "no tiene datos"** al arrancar | El contenedor ya existía cuando montó otro script: mismo reset de arriba |

### Y ahora, SU trabajo: reconstruirla desde cero

Ejecutar la versión del repo es solo el punto de partida. Lo que se evalúa es
**reconstruirla usted mismo, en una carpeta propia (fuera del clon)**,
siguiendo las especificaciones — con o sin ayuda de IA:

> 🤖 **[Guía para construir la versión con IA](docs/GUIA_IA.md)** — los dos
> caminos con su prompt listo para copiar: **chat web** (Gemini, DeepSeek,
> ChatGPT) e **IDE agéntico** (Antigravity, Cursor, Claude Code).

### Conceptos resumidos (los que acaba de usar)

| Concepto | En una frase |
|---|---|
| **Clonar** | Descargar el repositorio con su historial; `git pull` trae lo nuevo |
| **Contenedor** | La BD corre en una "caja" de Docker: nada que instalar, se borra y recrea sin miedo |
| **Volumen/estado** | `docker stop`/`start` conserva los datos; `docker rm -f` los borra (reset) |
| **Entorno virtual (venv)** | Las librerías del proyecto viven en `.venv/`, no en su Python global |
| **uvicorn --reload** | El servidor de la API; recarga solo cuando usted guarda un archivo |
| **Swagger (/docs)** | La documentación interactiva: probar la API desde el navegador |
| **Spec kit** | Los documentos que dicen QUÉ/CÓMO/EN QUÉ ORDEN — la fuente de verdad |
| **Versión / tag** | Un incremento cerrado y verificado (`v1`, `v2`, …): se avanza solo en verde |

---

## 2. La ruta de versiones

```
v1  api_facturas: CRUD de producto, solo PostgreSQL   ← USTED ESTÁ AQUÍ (cerrada: tag v1)
v2  más tablas (persona, factura maestro-detalle…)
v3  segundo motor (MariaDB) — nace la fábrica y DB_PROVIDER
v4  tercer motor (SQL Server) + docker compose completo
v5  API genérica (/api/{tabla})
v6  frontend Flask
```

La regla del juego: la **constitución** es permanente, cada versión tiene su
propia spec, y una versión está TERMINADA solo cuando pasa sus criterios de
aceptación (se cierra con tag). Detalle completo:
**[mapa de versiones](docs/spec_kit/versiones/0_mapa_versiones.md)**.

## 3. Las especificaciones de la versión actual (v1)

| Documento | Qué contiene |
|---|---|
| [Constitución](docs/spec_kit/1_constitution.md) | Las reglas permanentes del proyecto |
| [2_spec.md](docs/spec_kit/versiones/v1_producto_postgres/2_spec.md) | QUÉ construir y los 6 criterios de aceptación |
| [3_plan.md](docs/spec_kit/versiones/v1_producto_postgres/3_plan.md) | CÓMO: stack, carpetas, capas e interfaces |
| [5_data_model.md](docs/spec_kit/versiones/v1_producto_postgres/5_data_model.md) | La BD completa (dada) y la tabla `producto` que usa la v1 |
| [6_contracts.md](docs/spec_kit/versiones/v1_producto_postgres/6_contracts.md) | Los 7 endpoints con formatos exactos (5 verbos HTTP) |
| [7_quickstart.md](docs/spec_kit/versiones/v1_producto_postgres/7_quickstart.md) | Smoke test para validar lo construido |
| [8_tasks.md](docs/spec_kit/versiones/v1_producto_postgres/8_tasks.md) | Las fases de construcción, en orden |

## 4. Material conceptual del curso

| Documento | Qué cubre |
|---|---|
| [SDD y Spec Kit](docs/SDD_SPECKIT.md) | La metodología con la que se trabaja este curso: la spec manda sobre el código |
| [El paradigma P.O.O.](docs/PARADIGMA_POO.md) | Qué es un paradigma, los 4 pilares, la P.O.O. de Python (`Protocol`, duck typing) y **Pydantic** como clases que validan datos |
| [SOLID y programación por capas](docs/SOLID_Y_CAPAS.md) | Los 5 principios y las capas — y en qué versión se demuestra cada uno |
| [Principios ACID](docs/PRINCIPIOS_ACID.md) | Las 4 garantías transaccionales, por qué una facturación las exige, y el contraste con BASE |

---

*Proyecto Paradigmas · USB Med · La rama `sistema-completo` conserva el sistema
de referencia terminado (consultarla es decisión del profesor, no un atajo).*
