Comandos disponibles
1. Preguntas Diarias (Personales)
/iniciar_daily

Descripción: Inicia tu Daily personal y recibe preguntas por mensaje directo (DM).
Ejecución:
text


/iniciar_daily
/iniciar_daily_efimero

Descripción: Inicia tu Daily personal y recibe preguntas de manera efímera (visible solo para ti en el chat).
Ejecución:
text


/iniciar_daily_efimero
2. Preguntas Grupales del Sprint
/pregunta_sprint

Descripción: Publica una pregunta grupal del Sprint en el canal asignado al equipo.
Ejecución:
text


/pregunta_sprint team_id:<ID_del_equipo> pregunta:<Texto_de_la_pregunta>
Ejemplo:
text


/pregunta_sprint team_id:1 pregunta:"¿Cómo vamos con los objetivos del Sprint?"
/iniciar_sprint

Descripción: Inicia un Sprint global para el equipo.
Ejecución:
text


/iniciar_sprint team_id:<ID_del_equipo> start_date:<YYYY-MM-DD> end_date:<YYYY-MM-DD>
Ejemplo:
text


/iniciar_sprint team_id:1 start_date:2025-01-01 end_date:2025-01-15
/finalizar_sprint

Descripción: Finaliza el Sprint actual y registra los compromisos.
Ejecución:
text


/finalizar_sprint sprint_id:<ID_del_sprint> compromisos:<JSON_con_compromisos>
Ejemplo:
text


/finalizar_sprint sprint_id:1 compromisos:'[{"tarea":"Documentar APIs"},{"tarea":"Refactorización"}]'
3. Gestión de Dailies
/crear_daily

Descripción: Crea una sesión diaria para el equipo.
Ejecución:
text


/crear_daily team_id:<ID_del_equipo>
Ejemplo:
text


/crear_daily team_id:1
/responder_daily

Descripción: Registra tu respuesta a una pregunta diaria.
Ejecución:
text


/responder_daily member_id:<ID_del_miembro> question_id:<ID_de_la_pregunta> answer_text:<Respuesta>
Ejemplo:
text


/responder_daily member_id:123 question_id:1 answer_text:"Estoy trabajando en la implementación."
4. Gestión de Equipos
/registrar_equipo
Descripción: Registra un equipo y asocia el canal actual para notificaciones.
Ejecución:
text


/registrar_equipo team_name:<Nombre_del_equipo>
Ejemplo:
text


/registrar_equipo team_name:"Equipo Águilas"
