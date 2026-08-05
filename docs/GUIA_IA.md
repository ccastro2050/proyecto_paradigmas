# Cómo construir la versión con una IA de chat (Gemini, DeepSeek, ChatGPT…)

> Guía para trabajar la versión en curso con una IA **por chat web**, sin IDE
> con agente. La clave del método: la IA no inventa — **sigue el spec kit**.
> Usted es quien ejecuta el código y verifica; la IA propone.

---

## 1. Qué subirle (los 7 archivos de la v1)

En el chat (Gemini, DeepSeek y ChatGPT aceptan adjuntar archivos; si el suyo
no, pegue el contenido de cada uno en el mismo orden):

| # | Archivo | Papel |
|---|---|---|
| 1 | `docs/spec_kit/1_constitution.md` | Las reglas permanentes |
| 2 | `docs/spec_kit/versiones/v1_producto_postgres/2_spec.md` | QUÉ construir y los criterios de aceptación |
| 3 | `.../v1_producto_postgres/3_plan.md` | CÓMO: stack, carpetas, capas |
| 4 | `.../v1_producto_postgres/5_data_model.md` | La tabla producto (DDL + docker run) |
| 5 | `.../v1_producto_postgres/6_contracts.md` | Los 7 endpoints exactos |
| 6 | `.../v1_producto_postgres/7_quickstart.md` | El smoke test de validación |
| 7 | `.../v1_producto_postgres/8_tasks.md` | Las fases, en orden |

**No suba nada más.** El mapa de versiones no hace falta (y le revelaría a la
IA lo que viene — la regla es que la v1 no anticipa).

## 2. El prompt (cópielo tal cual como PRIMER mensaje)

```
Actúa como mi asistente de programación para construir la VERSIÓN 1 de un
proyecto universitario, partiendo de cero. Te adjunto 7 documentos: una
constitución (reglas permanentes) y el spec kit de la versión 1 (spec, plan,
modelo de datos, contratos, quickstart y tareas).

REGLAS DE TRABAJO (no negociables):

1. La especificación manda. No agregues NADA que los documentos no pidan:
   ni tablas extra, ni motores extra, ni fábricas "por si acaso", ni
   autenticación, ni mejoras de tu cosecha. Si crees que falta algo,
   pregúntame antes.
2. Vamos a seguir 8_tasks.md FASE POR FASE, en orden. En cada fase:
   a. Me explicas en 3-5 líneas qué vamos a hacer y por qué.
   b. Me das el contenido COMPLETO de cada archivo de esa fase (con su ruta
      exacta según la estructura de 3_plan.md), con los comentarios
      didácticos en español que exige la constitución.
   c. Me dices el comando de verificación de la fase y QUÉ salida esperar.
   d. TE DETIENES y esperas a que yo ejecute y te pegue el resultado.
      No avanzas a la siguiente fase sin mi confirmación.
3. Si mi resultado muestra un error, lo diagnosticamos y corregimos ANTES de
   avanzar. Nunca "sigamos y después lo arreglamos".
4. El código debe cumplir los contratos de 6_contracts.md al pie de la letra:
   mismos verbos, mismas rutas, mismos códigos de estado, mismos formatos de
   respuesta (incluido el contraste PUT=reemplazo completo vs PATCH=parcial).
5. Todo en español: nombres, comentarios, docstrings y mensajes.
6. Yo trabajo en Windows con PowerShell, VS Code, Python 3.12 y Docker
   Desktop. Dame los comandos para ese entorno.

Al final, la versión 1 está TERMINADA solo cuando pasan los 6 criterios de
aceptación de 2_spec.md, verificados con el smoke test de 7_quickstart.md.

Empieza: resume en máximo 10 líneas qué vamos a construir (para confirmar que
entendiste el alcance) y luego arranca con la Fase 0.
```

## 3. Cómo trabajar la conversación (el método)

1. **La IA propone, usted ejecuta.** Copie cada archivo que la IA le entregue
   a la ruta exacta en VS Code; corra el comando de verificación en PowerShell;
   pegue la salida REAL en el chat (completa, con el error si lo hay).
2. **Una fase a la vez.** Si la IA se embala y le entrega tres fases juntas,
   recuérdele la regla 2d: "detente, vamos fase por fase".
3. **Vigile las alucinaciones de alcance.** Si aparece un `DB_PROVIDER`, una
   fábrica con diccionario, una tabla `persona` o un `docker-compose.yml`,
   la IA se salió de la v1: dígale "eso no está en la spec de esta versión,
   quítalo" (la spec gana la discusión, siempre).
4. **El cierre no es opinión.** Corra el smoke test completo de
   7_quickstart.md §3. Los 6 criterios en verde = terminado; uno en rojo =
   no está terminado, sin importar lo que diga la IA.
5. **Si el chat pierde el contexto** (conversaciones largas): abra un chat
   nuevo, vuelva a subir los 7 documentos, y agregue al prompt: "Ya tengo
   construidas las fases 0 a N; te pego el código actual. Continuemos en la
   fase N+1" (y pegue sus archivos).

## 4. Por qué funciona (la lección del curso)

Esto ES spec-driven development ([SDD_SPECKIT.md](SDD_SPECKIT.md)): la misma
IA que con "hazme una API de productos" produce cualquier cosa, con una
constitución + spec + plan + tareas produce EL sistema especificado — y usted
puede verificarlo contra criterios escritos antes de la primera línea de
código. La habilidad que está practicando no es "pedirle código a la IA":
es **dirigirla con especificaciones**.
