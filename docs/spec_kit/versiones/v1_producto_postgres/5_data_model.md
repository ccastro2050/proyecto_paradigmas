# Modelo de datos — API Facturas **v1**: la tabla `producto`

> **Versión 1** · Una sola entidad, un solo motor. El modelo completo de
> `bdfacturas` (12 tablas, trigger, SPs) es la visión final; v1 crea
> únicamente lo que usa.

---

## 1. La entidad

| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `codigo` | VARCHAR(20) | **PK** | Identificador legible (PR001…) |
| `nombre` | VARCHAR(100) | NOT NULL | Nombre del producto |
| `stock` | INTEGER | NOT NULL, `CHECK (stock >= 0)` | Unidades disponibles |
| `valorunitario` | NUMERIC(12,2) | NOT NULL, `CHECK (valorunitario >= 0)` | Precio unitario |

Doble validación deliberada: **Pydantic** rechaza entradas inválidas en la API
(422) y los **CHECK** de la BD son la última línea de defensa — el mismo dato
está protegido en dos capas distintas.

## 2. `init.sql` de la v1 (completo)

```sql
-- v1: solo la tabla producto y sus datos de ejemplo
CREATE TABLE producto (
    codigo        VARCHAR(20)   PRIMARY KEY,
    nombre        VARCHAR(100)  NOT NULL,
    stock         INTEGER       NOT NULL CHECK (stock >= 0),
    valorunitario NUMERIC(12,2) NOT NULL CHECK (valorunitario >= 0)
);

INSERT INTO producto (codigo, nombre, stock, valorunitario) VALUES
('PR001', 'Laptop Lenovo IdeaPad',      17, 2500000),
('PR002', 'Monitor Samsung 24"',        27,  800000),
('PR003', 'Teclado Logitech K380',      42,  150000),
('PR004', 'Mouse HP',                   55,   90000),
('PR005', 'Impresora Epson EcoTank1',   14, 1100000),
('PR006', 'Auriculares Sony WH-CH510',  23,  240000),
('PR007', 'Tablet Samsung Tab A9',      15,  950000),
('PR008', 'Disco Duro Seagate 1TB',     32,  280000);
```

Los datos coinciden con los de la BD final `bdfacturas`: cuando v2 agregue las
demás tablas, `producto` no cambia.

## 3. Montar PostgreSQL para la v1

```powershell
# guardar el SQL de arriba como db/init.sql y desde la raíz del proyecto:
docker run -d --name bd_v1 -p 15432:5432 `
  -e POSTGRES_DB=bdfacturas_postgres_local `
  -e POSTGRES_USER=paradigmas -e POSTGRES_PASSWORD=paradigmas123 `
  -v ${PWD}/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro `
  postgres:16-alpine
```

Cadena de conexión para la API (variable de entorno):

```
DB_POSTGRES=postgresql+asyncpg://paradigmas:paradigmas123@localhost:15432/bdfacturas_postgres_local
```

## 4. Qué NO existe todavía (a propósito)

Ni `persona`, ni `factura`, ni FKs, ni el trigger de totales/stock, ni SPs:
llegan con la v2+ ([mapa de versiones](../0_mapa_versiones.md)). El nombre de
la BD ya es el definitivo para que las versiones siguientes solo **agreguen**
tablas al mismo sitio.
