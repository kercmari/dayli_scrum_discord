from datetime import datetime, date
from .models import Team, TeamSettings, Sprint, DailySession, Answer, Commitment, Member
from .__init__ import db


def iniciar_sprint(team_id, start_date, end_date):
    sprint = Sprint(team_id=team_id, start_date=start_date, end_date=end_date)
    db.session.add(sprint)
    db.session.commit()
    return sprint


def finalizar_sprint(sprint_id, compromisos):
    """
    'compromisos' es una lista de diccionarios con keys: member_id y commitment_description.
    """
    from models import Commitment

    sprint = Sprint.query.get(sprint_id)
    if not sprint:
        return None
    for comp in compromisos:
        commitment = Commitment(
            sprint_id=sprint_id,
            member_id=comp["member_id"],
            commitment_description=comp["commitment_description"],
        )
        db.session.add(commitment)
    db.session.commit()
    return sprint


def crear_daily_session(team_id):
    today = date.today()
    existing = DailySession.query.filter_by(team_id=team_id, date=today).first()
    if existing:
        return existing
    daily = DailySession(team_id=team_id, date=today)
    db.session.add(daily)
    db.session.commit()
    return daily


def responder_daily(member_id, question_id, answer_text):
    answer = Answer(
        member_id=member_id, question_id=question_id, answer_text=answer_text
    )
    db.session.add(answer)
    db.session.commit()
    return answer


def registrar_equipo(team_name, channel_id):
    """
    Servicio que crea un equipo y su configuración asociada.
    """
    try:
        # Crear el equipo
        team = Team(team_name=team_name)
        db.session.add(team)
        db.session.flush()

        # Crear la configuración del equipo
        settings = TeamSettings(
            team_id=team.id,
            daily_time=datetime.utcnow().time(),
            reminder_interval=24,
            channel_id=channel_id,
        )
        db.session.add(settings)
        db.session.commit()

        return {"team_id": team.id, "channel_id": channel_id}

    except Exception as e:
        print(e)
        db.session.rollback()
        raise


def registrar_miembros(members):
    """
    Servicio que registra miembros en un equipo.
    """
    try:
        for member in members:
            member = Member(
                team_id=member["team_id"],
                member_id=member["member_id"],
                member_name=member["member_name"],
            )
            db.session.add(member)
        db.session.commit()
        return {"message": "Miembros registrados correctamente."}
    except Exception as e:
        print(e)
        db.session.rollback
