# Configuracion y test

```
python3 -m venv venv
source venv/bin/activate
pip install -r requeriments.txt

python3 run.py
python3 discord_bot/bot.py
```

# Comandos disponibles

1. Registrar equipo
Endpoint: POST /api/registrar_equipo

Objetivo:
Crea un nuevo equipo y su configuración básica (por ejemplo, canal de Discord).

Parámetros esperados (JSON):

team_name (string): Nombre del equipo.
channel_id (int): ID del canal (en caso de integraciones con Discord u otras plataformas).
Respuesta exitosa (JSON):

Devuelve un objeto con la información del nuevo equipo y su configuración.
2. Registrar miembros
Endpoint: POST /api/registrar_miembros

Objetivo:
Registra uno o varios miembros en el sistema, asociándolos a un equipo.

Parámetros esperados (JSON):

members (array de objetos): Cada objeto debe incluir información como team_id, member_name, etc.
Respuesta exitosa (JSON):

Lista o resumen de los miembros registrados.
3. Obtener equipo (por ID)
Endpoint: GET /api/obtener_equipo/<int:team_id>

Objetivo:
Recupera la información de configuración de un equipo específico, principalmente el channel_id.

Parámetros en la URL:

team_id (int): ID del equipo.
Respuesta exitosa (JSON):

Devuelve un objeto con la configuración del equipo (p. ej., team_id y channel_id).
4. Obtener equipo (por canal)
Endpoint: GET /api/obtener_equipo_por_canal/<int:channel_id>

Objetivo:
Dado un channel_id, obtener el equipo asociado.

Parámetros en la URL:

channel_id (int): ID del canal (Discord u otro).
Respuesta exitosa (JSON):

Devuelve un objeto con el team_id correspondiente.
5. Iniciar sprint
Endpoint: POST /api/iniciar_sprint

Objetivo:
Crea e inicia un nuevo sprint para un equipo, indicando fechas de inicio y fin.

Parámetros esperados (JSON):

team_id (int): ID del equipo al que se asocia el sprint.
start_date (string, formato YYYY-MM-DD): Fecha de inicio del sprint.
end_date (string, formato YYYY-MM-DD): Fecha de fin del sprint.
Respuesta exitosa (JSON):

Devuelve el sprint_id creado y el team_id.
6. Crear sesión de Daily
Endpoint: POST /api/crear_daily

Objetivo:
Crea una nueva sesión de daily para el equipo (generalmente se hace cada día dentro de un sprint).

Parámetros esperados (JSON):

team_id (int): ID del equipo.
Respuesta exitosa (JSON):

Devuelve el daily_id generado y la fecha de la sesión.
7. Responder daily
Endpoint: POST /api/responder_daily

Objetivo:
Registra la respuesta de un miembro a una pregunta de la daily (por ejemplo, “¿Qué hiciste ayer?”, “¿Qué harás hoy?”, “¿Tienes algún bloqueo?”).

Parámetros esperados (JSON):

member_id (int): ID del miembro que responde.
question_id (int): ID de la pregunta.
answer_text (string): Texto de la respuesta.
Respuesta exitosa (JSON):

Devuelve un identificador de la respuesta registrada (answer_id).
8. Resumen de Daily
Endpoint: GET /api/daily_summary/<int:team_id>

Objetivo:
Obtener todas las respuestas de daily de un equipo ordenadas por fecha, para tener un resumen de la actividad de cada miembro.

Parámetros en la URL:

team_id (int): ID del equipo.
Respuesta exitosa (JSON):

Devuelve un array con los detalles de las respuestas (member_id, question_id, answer_text, answered_at).
9. Finalizar sprint
Endpoint: POST /api/finalizar_sprint

Objetivo:
Marca un sprint como finalizado e incluye los compromisos o conclusiones de cada miembro al cerrar el sprint.

Parámetros esperados (JSON):

sprint_id (int): ID del sprint que se quiere finalizar.
compromisos (array de objetos): Cada objeto podría tener member_id y commitment_description.
Respuesta exitosa (JSON):

Mensaje confirmando que el sprint fue finalizado y los compromisos guardados.
Orden de Uso Recomendado
Registrar equipo (/api/registrar_equipo)
Registrar miembros (/api/registrar_miembros)
(Opcional si se requiere info específica) Obtener equipo (/api/obtener_equipo/<team_id>)
(Opcional si se maneja vía canal) Obtener equipo por canal (/api/obtener_equipo_por_canal/<channel_id>)
Iniciar sprint (/api/iniciar_sprint)
Crear sesión de Daily (/api/crear_daily)
Responder daily (/api/responder_daily)
(En cualquier momento que se requiera un reporte) Resumen de Daily (/api/daily_summary/<team_id>)
Finalizar sprint (/api/finalizar_sprint)
Este flujo cubre el ciclo de vida típico de un sprint y las actividades diarias, desde la creación del equipo, registro de miembros, inicio de sprint, creación de la daily, respuestas y, finalmente, la finalización del sprint. Los endpoints de “obtener_equipo” y “obtener_equipo_por_canal” son de utilidad para recuperar información del equipo según sea necesario.