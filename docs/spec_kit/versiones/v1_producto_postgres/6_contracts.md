# Contratos HTTP — API Facturas **v1**: producto + PostgreSQL

> **Versión 1** · Base: `http://localhost:8002`. Documentación interactiva:
> `/docs` (Swagger) y `/redoc`.

---

## 0. Convenciones

- Router con prefix `/api`, tag `Producto`.
- Errores SIEMPRE como `HTTPException` con `detail` estructurado:

```json
{ "detail": { "estado": 404, "mensaje": "Producto no encontrado.", "detalle": "..." } }
```

| Origen | HTTP |
|---|---|
| Body inválido (Pydantic) | **422** (formato estándar de FastAPI) |
| `ValueError` del servicio | 400 |
| `LookupError` (código inexistente) | 404 |
| Error del motor (PK duplicada, BD caída) | 500 con el mensaje en `detalle` |

## 1. `GET /api/producto` — Listar

```
→ 200 { "tabla": "producto", "total": 8,
        "datos": [ { "codigo": "PR001", "nombre": "Laptop Lenovo IdeaPad",
                     "stock": 17, "valorunitario": 2500000.0 }, … ] }
→ 204 (cuerpo vacío) si no hay productos
```

## 2. `GET /api/producto/{codigo}` — Obtener uno

```
GET /api/producto/PR001
→ 200 { "codigo": "PR001", "nombre": "Laptop Lenovo IdeaPad",
        "stock": 17, "valorunitario": 2500000.0 }
→ 404 detail { estado: 404, mensaje: "Producto no encontrado.",
               detalle: "No existe un producto con codigo = PR999" }
```

## 3. `POST /api/producto` — Crear

Body (modelo Pydantic `Producto`, todos obligatorios):

```
POST /api/producto
body { "codigo": "PR009", "nombre": "Webcam Logitech", "stock": 5, "valorunitario": 120000 }
→ 200 { "estado": 200, "mensaje": "Producto creado exitosamente." }
→ 422 si falta un campo, stock < 0 o valorunitario < 0   (respuesta de Pydantic)
→ 500 si el código ya existe (error del motor en detalle)
```

## 4. `PUT /api/producto/{codigo}` — Actualizar

Body (modelo `ProductoActualizar`, todos opcionales — solo se cambian los enviados):

```
PUT /api/producto/PR009      body { "stock": 7 }
→ 200 { "estado": 200, "mensaje": "Producto actualizado exitosamente.",
        "filasAfectadas": 1 }
→ 404 si el código no existe
→ 422 si algún campo enviado viola la validación
```

## 5. `DELETE /api/producto/{codigo}` — Eliminar

```
DELETE /api/producto/PR009
→ 200 { "estado": 200, "mensaje": "Producto eliminado exitosamente.",
        "filasEliminadas": 1 }
→ 404 si el código no existe
```

## 6. `GET /` — Diagnóstico

```
→ 200 { "mensaje": "API Facturas funcionando", "version": "v1",
        "documentacion": "/docs" }
```

## 7. Estabilidad de este contrato

Estos 6 endpoints **no cambian en las versiones siguientes**: v2 agrega
entidades nuevas (rutas nuevas), v3/v4 cambian el motor por configuración —
si algún cambio futuro rompiera este contrato, es una decisión mayor que debe
quedar registrada en la spec de esa versión.
