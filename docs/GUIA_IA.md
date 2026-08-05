# Cómo construir la versión con IA — por chat o con un IDE agéntico

> Guía para trabajar la versión en curso con ayuda de IA por **cualquiera de
> los dos caminos**: un chat web (Gemini, DeepSeek, ChatGPT…) o un IDE
> agéntico (Antigravity, Cursor, Claude Code, Copilot en VS Code…).
> La clave del método es la misma en ambos: la IA no inventa — **sigue el
> spec kit**. Usted verifica; la IA propone (chat) o ejecuta bajo su
> supervisión (IDE).

---

## 0. Los dos caminos, en una tabla

| | **Camino A: chat web** | **Camino B: IDE agéntico** |
|---|---|---|
| Herramientas | Gemini, DeepSeek, ChatGPT, Claude (web) | Antigravity, Cursor, Claude Code, Copilot agente |
| ¿Cómo conoce la spec? | Usted le **sube los 7 archivos** | El agente **lee los archivos del repo clonado** |
| ¿Quién escribe los archivos? | Usted copia/pega lo que la IA propone | El agente crea y edita los archivos directamente |
| ¿Quién ejecuta los comandos? | Usted, en PowerShell, y pega la salida | El agente (pidiéndole permiso); usted revisa la salida |
| Su papel | Operador: ejecutar y reportar | Supervisor: revisar diffs y aprobar |
| Riesgo típico | La IA "olvida" el contexto en chats largos | El agente se embala y hace de más sin que usted lo note |

En ambos casos, "terminado" significa lo mismo: **los 6 criterios de
aceptación de `2_spec.md` en verde**, verificados con el smoke test de
`7_quickstart.md` — corrido por usted.

---

## Camino A — Chat web (Gemini, DeepSeek, ChatGPT…)

### A.1 Qué subirle (los 7 archivos de la v1)

En el chat (todos aceptan adjuntar archivos; si el suyo no, pegue el contenido
de cada uno en el mismo orden):

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

### A.2 El prompt (cópielo tal cual como PRIMER mensaje)

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

### A.3 El método de la conversación

1. **La IA propone, usted ejecuta.** Copie cada archivo a la ruta exacta en
   VS Code; corra el comando de verificación en PowerShell; pegue la salida
   REAL en el chat (completa, con el error si lo hay).
2. **Una fase a la vez.** Si la IA se embala y entrega tres fases juntas,
   recuérdele la regla 2d: "detente, vamos fase por fase".
3. **Si el chat pierde el contexto** (conversaciones largas): abra un chat
   nuevo, vuelva a subir los 7 documentos y agregue al prompt: "Ya tengo
   construidas las fases 0 a N; te pego el código actual. Continuemos en la
   fase N+1" (y pegue sus archivos).

---

## Camino B — IDE agéntico (Antigravity, Cursor, Claude Code…)

Un IDE agéntico tiene a la IA **dentro del proyecto**: lee los archivos del
repo por sí misma, crea y edita código directamente, y puede ejecutar
comandos en la terminal (pidiendo permiso). Usted pasa de operador a
**supervisor**.

### B.1 Preparación

1. Clone el repositorio y ábralo como carpeta del proyecto en el IDE
   (en Antigravity: *Open Folder* sobre la carpeta clonada; el agente ya ve
   `docs/spec_kit/` — no hay que subirle nada).
2. Tenga Docker Desktop corriendo (el agente necesitará levantar PostgreSQL).
3. Active el modo agente (en Antigravity, el *Agent Manager*; en otros IDE,
   el chat en modo "agent").

### B.2 El prompt para el agente (cópielo tal cual)

```
Construye la VERSIÓN 1 de este proyecto, partiendo de cero.

Primero lee, en este orden: docs/spec_kit/1_constitution.md y los seis
documentos de docs/spec_kit/versiones/v1_producto_postgres/ (2_spec, 3_plan,
5_data_model, 6_contracts, 7_quickstart, 8_tasks). Después resume en máximo
10 líneas qué vas a construir y espera mi confirmación antes de tocar nada.

REGLAS (no negociables):

1. La especificación manda. No agregues NADA que los documentos no pidan:
   ni tablas extra, ni motores extra, ni fábricas "por si acaso", ni
   autenticación, ni docker-compose. Si crees que falta algo, pregúntame.
2. Sigue 8_tasks.md FASE POR FASE. Al terminar cada fase, EJECUTA su
   verificación (la que dice la propia fase), muéstrame el resultado real,
   y espera mi OK antes de pasar a la siguiente.
3. El código debe cumplir 6_contracts.md al pie de la letra: verbos, rutas,
   códigos de estado y formatos de respuesta exactos (incluido el contraste
   PUT=reemplazo completo vs PATCH=parcial).
4. Todo en español: nombres, comentarios, docstrings y mensajes, con los
   comentarios didácticos que exige la constitución.
5. Al final, corre el smoke test completo de 7_quickstart.md §3 y muéstrame
   la evidencia de los 6 criterios de aceptación de 2_spec.md. La versión no
   está terminada hasta que los 6 estén en verde.
```

### B.3 El método de supervisión

1. **Revise cada diff antes de aceptar.** El IDE muestra qué archivos creó o
   cambió el agente — léalos. Si un archivo no está en la estructura de
   `3_plan.md` §2, pregunte por qué existe.
2. **Exija la evidencia, no el relato.** "Ya pasa la fase 3" no vale: pida la
   salida real del comando de verificación. Los agentes a veces declaran
   éxito sin ejecutar.
3. **Vigile el alcance igual que en el chat.** Si aparece un `DB_PROVIDER`,
   una fábrica con diccionario, una tabla `persona` o un `docker-compose.yml`,
   el agente se salió de la v1: "eso no está en la spec de esta versión,
   quítalo".
4. **El cierre lo corre usted.** Aunque el agente haya corrido el smoke test,
   ejecútelo usted mismo de principio a fin (`7_quickstart.md` §3): esa es SU
   verificación de que la versión está terminada.
5. **Consejo de Antigravity:** el agente genera "walkthroughs"/artefactos de
   lo que hizo — guárdelos: son evidencia de su proceso para la entrega.

---

## Por qué funciona (la lección del curso)

Esto ES spec-driven development ([SDD_SPECKIT.md](SDD_SPECKIT.md)): la misma
IA que con "hazme una API de productos" produce cualquier cosa, con una
constitución + spec + plan + tareas produce EL sistema especificado — y usted
puede verificarlo contra criterios escritos antes de la primera línea de
código. Note que **las reglas de los dos prompts son las mismas**; solo cambia
quién ejecuta. La habilidad que está practicando no es "pedirle código a la
IA": es **dirigirla con especificaciones** — y eso funciona igual en un chat
gratuito que en el IDE agéntico más sofisticado.
