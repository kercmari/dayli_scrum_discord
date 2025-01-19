from flask import Blueprint, request, jsonify
from datetime import datetime
from .services import (
    iniciar_sprint,
    finalizar_sprint,
    crear_daily_session,
    responder_daily,
    registrar_equipo,
    registrar_miembros,
)

from .models import Team, TeamSettings, Member, Answer

bp = Blueprint("main", __name__)


@bp.route("/api/iniciar_sprint", methods=["POST"])
def api_iniciar_sprint():
    data = request.get_json()
    team_id = data.get("team_id")
    start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
    end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
    sprint = iniciar_sprint(team_id, start_date, end_date)
    return jsonify({"sprint_id": sprint.id, "team_id": sprint.team_id}), 200


@bp.route("/api/finalizar_sprint", methods=["POST"])
def api_finalizar_sprint():
    data = request.get_json()
    sprint_id = data.get("sprint_id")
    compromisos = data.get(
        "compromisos"
    )  # lista de dicts [{"member_id":..., "commitment_description":...}]
    sprint = finalizar_sprint(sprint_id, compromisos)
    if sprint:
        return jsonify({"message": "Sprint finalizado y compromisos guardados."}), 200
    return jsonify({"error": "Sprint no encontrado."}), 404


@bp.route("/api/crear_daily", methods=["POST"])
def api_crear_daily():
    data = request.get_json()
    team_id = data.get("team_id")
    daily = crear_daily_session(team_id)
    return jsonify({"daily_id": daily.id, "date": str(daily.date)}), 200


@bp.route("/api/responder_daily", methods=["POST"])
def api_responder_daily():
    data = request.get_json()
    member_id = data.get("member_id")
    question_id = data.get("question_id")
    answer_text = data.get("answer_text")
    answer = responder_daily(member_id, question_id, answer_text)
    return jsonify({"answer_id": answer.id}), 200


@bp.route("/api/daily_summary/<int:team_id>", methods=["GET"])
def api_daily_summary(team_id):
    """
    Retorna las respuestas de los usuarios de un equipo ordenadas por fecha.
    """
    answers = (
        Answer.query.join(Member)
        .filter(Member.team_id == team_id)
        .order_by(Answer.answered_at)
        .all()
    )
    summary = [
        {
            "member_id": a.member_id,
            "question_id": a.question_id,
            "answer_text": a.answer_text,
            "answered_at": a.answered_at.isoformat(),
        }
        for a in answers
    ]
    return jsonify({"daily_summary": summary}), 200


@bp.route("/api/registrar_equipo", methods=["POST"])
def api_registrar_equipo():
    try:
        data = request.get_json()
        print("Esta es la data", data)
        team_name = data.get("team_name")
        channel_id = data.get("channel_id")

        if not team_name or not channel_id:
            return jsonify({"error": "Faltan datos (team_name o channel_id)."}), 400

        result = registrar_equipo(team_name, channel_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/api/obtener_equipo/<int:team_id>", methods=["GET"])
def api_obtener_equipo(team_id):
    """
    Retorna la configuración de un equipo (por ejemplo, canal de Discord).
    """
    settings = TeamSettings.query.filter_by(team_id=team_id).first()
    if not settings:
        return jsonify({"error": "Equipo no encontrado."}), 404
    return jsonify({"team_id": team_id, "channel_id": settings.channel_id}), 200


# En tu API Flask
@bp.route("/api/registrar_miembros", methods=["POST"])
def registrar_miembros():
    try:
        data = request.json
        members = data.get("members", [])

        result = registrar_miembros(members)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/api/obtener_equipo_por_canal/<int:channel_id>")
def obtener_equipo_por_canal(channel_id):
    team = (
        Team.query.join(TeamSettings)
        .filter(TeamSettings.channel_id == channel_id)
        .first()
    )

    if not team:
        return jsonify({"error": "Equipo no encontrado"}), 404

    return jsonify({"team_id": team.id})
