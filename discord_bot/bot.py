from typing import Optional
import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("daily_bot.log"),  # Guardar logs en archivo
        logging.StreamHandler(),  # Mostrar logs en consola
    ],
)
logger = logging.getLogger("daily_bot")

# Cargar y validar variables de entorno
load_dotenv()
FLASK_API_URL = os.getenv("FLASK_API_URL")
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN no está configurado")
if not FLASK_API_URL:
    raise ValueError("FLASK_API_URL no está configurado")

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.guilds = True  # Añade esta línea
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)


class DailyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="iniciar_daily",
        description="Inicia tu Daily personal y recibe tus preguntas por DM",
    )
    async def iniciar_daily(self, interaction: discord.Interaction):
        preguntas = [
            "¿Qué hiciste ayer?",
            "¿Qué harás hoy?",
            "¿Hay algo que te esté deteniendo en tu progreso?",
        ]
        mensaje = "Tus preguntas para hoy son:\n" + "\n".join(preguntas)
        try:
            await interaction.user.send(mensaje)
            await interaction.response.send_message(
                "Te he enviado tus preguntas personales por DM.", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error enviando DM: {e}")
            await interaction.response.send_message(
                "No pude enviarte las preguntas por DM. Revisa tu configuración de privacidad.",
                ephemeral=True,
            )

    @app_commands.command(
        name="iniciar_daily_efimero", description="Inicia tu Daily personal (efímero)"
    )
    async def iniciar_daily_efimero(self, interaction: discord.Interaction):
        preguntas = [
            "¿Qué hiciste ayer?",
            "¿Qué harás hoy?",
            "¿Hay algo que te esté deteniendo en tu progreso?",
        ]
        mensaje = "Tus preguntas para hoy:\n" + "\n".join(preguntas)
        await interaction.response.send_message(mensaje, ephemeral=True)

    @app_commands.command(
        name="pregunta_sprint",
        description="Publica la pregunta grupal del Sprint en el canal asignado",
    )
    async def pregunta_sprint(
        self, interaction: discord.Interaction, team_id: int, pregunta: str
    ):
        try:
            response = requests.get(f"{FLASK_API_URL}/api/obtener_equipo/{team_id}")
            if response.status_code != 200:
                logger.error(f"Error obteniendo equipo: {response.status_code}")
                await interaction.response.send_message(
                    "No se encontró la información del equipo.", ephemeral=True
                )
                return

            equipo_info = response.json()
            channel_id = equipo_info.get("channel_id")
            canal = self.bot.get_channel(channel_id)

            if not canal:
                await interaction.response.send_message(
                    "El canal asignado no se encuentra en este servidor.",
                    ephemeral=True,
                )
                return

            miembros = [m for m in interaction.guild.members if not m.bot]
            menciones = " ".join([member.mention for member in miembros])
            mensaje = f"**Pregunta Global del Sprint:** {pregunta}\n\n{menciones}"
            await canal.send(mensaje)
            await interaction.response.send_message(
                "Pregunta grupal publicada correctamente.", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error en pregunta_sprint: {e}")
            await interaction.response.send_message(
                "Error al procesar la pregunta del sprint.", ephemeral=True
            )

    @app_commands.command(
        name="iniciar_sprint", description="Inicia un sprint (global) para el equipo"
    )
    async def iniciar_sprint(
        self,
        interaction: discord.Interaction,
        team_id: int,
        start_date: str,
        end_date: str,
    ):
        try:
            data = {"team_id": team_id, "start_date": start_date, "end_date": end_date}
            response = requests.post(f"{FLASK_API_URL}/iniciar_sprint", json=data)
            if response.status_code == 200:
                sprint_info = response.json()
                await interaction.response.send_message(
                    f"Sprint iniciado: {sprint_info}"
                )
            else:
                logger.error(f"Error iniciando sprint: {response.status_code}")
                await interaction.response.send_message(
                    "Error iniciando sprint.", ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error en iniciar_sprint: {e}")
            await interaction.response.send_message(
                "Error inesperado al iniciar el sprint.", ephemeral=True
            )

    @app_commands.command(
        name="finalizar_sprint",
        description="Finaliza el sprint actual y registra los compromisos",
    )
    async def finalizar_sprint(
        self, interaction: discord.Interaction, sprint_id: int, compromisos: str
    ):
        try:
            import json

            comp_list = json.loads(compromisos)
            data = {"sprint_id": sprint_id, "compromisos": comp_list}
            response = requests.post(f"{FLASK_API_URL}/finalizar_sprint", json=data)

            if response.status_code == 200:
                await interaction.response.send_message(
                    "Sprint finalizado y compromisos guardados."
                )
            else:
                logger.error(f"Error finalizando sprint: {response.status_code}")
                await interaction.response.send_message(
                    "Error finalizando sprint.", ephemeral=True
                )
        except json.JSONDecodeError:
            await interaction.response.send_message(
                "Formato de compromisos inválido. Asegúrate de enviar un JSON válido.",
                ephemeral=True,
            )
        except Exception as e:
            logger.error(f"Error en finalizar_sprint: {e}")
            await interaction.response.send_message(
                "Error inesperado al finalizar el sprint.", ephemeral=True
            )

    @app_commands.command(
        name="crear_daily", description="Crea la sesión diaria para el equipo"
    )
    async def crear_daily(self, interaction: discord.Interaction, team_id: int):
        try:
            data = {"team_id": team_id}
            response = requests.post(f"{FLASK_API_URL}/crear_daily", json=data)

            if response.status_code == 200:
                daily_info = response.json()
                await interaction.response.send_message(
                    f"Daily creada para la fecha: {daily_info['date']}", ephemeral=True
                )
            else:
                logger.error(f"Error creando daily: {response.status_code}")
                await interaction.response.send_message(
                    "Error creando la daily.", ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error en crear_daily: {e}")
            await interaction.response.send_message(
                "Error inesperado al crear la daily.", ephemeral=True
            )

    @app_commands.command(
        name="responder_daily", description="Registra tu respuesta al daily"
    )
    async def responder_daily(
        self,
        interaction: discord.Interaction,
        member_id: int,
        question_id: int,
        answer_text: str,
    ):
        try:
            data = {
                "member_id": member_id,
                "question_id": question_id,
                "answer_text": answer_text,
            }
            response = requests.post(f"{FLASK_API_URL}/responder_daily", json=data)

            if response.status_code == 200:
                resp = response.json()
                await interaction.response.send_message(
                    f"Respuesta registrada, ID: {resp['answer_id']}", ephemeral=True
                )
            else:
                logger.error(f"Error registrando respuesta: {response.status_code}")
                await interaction.response.send_message(
                    "Error registrando la respuesta.", ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error en responder_daily: {e}")
            await interaction.response.send_message(
                "Error inesperado al registrar la respuesta.", ephemeral=True
            )

    @app_commands.command(
        name="registrar_equipo",
        description="Registra el equipo usando el canal actual para recordatorios.",
    )
    @app_commands.describe(
        team_name="Nombre opcional del equipo. Si no se especifica, se usará el nombre del canal."
    )
    async def registrar_equipo(
        self, interaction: discord.Interaction, team_name: str = None
    ):
        try:
            team_name = team_name or interaction.channel.name
            channel_id = interaction.channel.id
            data = {"team_name": team_name, "channel_id": channel_id}

            logger.info(f"Registrando equipo: {team_name} {FLASK_API_URL}")
            response = requests.post(f"{FLASK_API_URL}/api/registrar_equipo", json=data)

            if response.status_code == 200:
                equipo_info = response.json()
                await interaction.response.send_message(
                    f"Equipo **{team_name}** registrado con ID {equipo_info['team_id']} "
                    f"y canal: {channel_id}.",
                    ephemeral=True,
                )
            else:
                error_msg = (
                    f"Error registrando el equipo. Status: {response.status_code}"
                )
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('message', '')}"
                except:
                    pass
                await interaction.response.send_message(error_msg, ephemeral=True)
        except Exception as e:
            logger.error(f"Error en registrar_equipo: {e}")
            await interaction.response.send_message(
                "Error inesperado al registrar el equipo.", ephemeral=True
            )

    @app_commands.command(
        name="registrar_miembros",
        description="Registra todos los miembros del canal actual al equipo",
    )
    async def registrar_miembros(
        self, interaction: discord.Interaction, team_id: Optional[int] = None
    ):
        try:
            # Si no se proporciona team_id, buscarlo por el canal actual
            if not team_id:
                channel_id = interaction.channel.id
                response = requests.get(
                    f"{FLASK_API_URL}/api/obtener_equipo_por_canal/{channel_id}"
                )
                if response.status_code != 200:
                    await interaction.response.send_message(
                        "No se encontró un equipo registrado para este canal. "
                        "Usa /registrar_equipo primero.",
                        ephemeral=True,
                    )
                    return
                team_id = response.json()["team_id"]

            # Obtener miembros no-bot del canal
            miembros = [
                member for member in interaction.channel.members if not member.bot
            ]

            if not miembros:
                await interaction.response.send_message(
                    "No se encontraron miembros para registrar.", ephemeral=True
                )
                return

            # Preparar datos
            members_data = [
                {
                    "member_name": member.name,
                    "member_id": str(member.id),
                    "team_id": team_id,
                }
                for member in miembros
            ]

            # Enviar a API
            response = requests.post(
                f"{FLASK_API_URL}/api/registrar_miembros",
                json={"members": members_data},
            )
            print(response.json())
            if response.status_code == 200:
                await interaction.response.send_message(
                    f"✅ Registrados {len(miembros)} miembros al equipo {team_id}\n"
                    f"Miembros: {', '.join(m.name for m in miembros)}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"❌ Error al registrar miembros: {response.json().get('error')}",
                    ephemeral=True,
                )

        except Exception as e:
            logger.error(f"Error en registrar_miembros: {e}")
            await interaction.response.send_message(
                "Error inesperado al registrar miembros", ephemeral=True
            )


# Modificar el setup para eliminar sincronización redundante
async def setup(bot):
    await bot.add_cog(DailyCommands(bot))


# Modificar on_ready para mejor manejo
@bot.event
async def on_ready():
    logger.info(f"{bot.user} se ha conectado a Discord!")
    try:
        if not bot.get_cog("DailyCommands"):
            await bot.add_cog(DailyCommands(bot))
            logger.info("Cog DailyCommands agregado")

        # Iniciar recordatorio sin sincronizar aquí
        daily_reminder.start()
        logger.info("Recordatorio diario iniciado")

    except Exception as e:
        logger.error(f"Error en on_ready: {e}")


# Mejorar comando sync con opciones
@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx, guild_id: Optional[int] = None):
    """Sincroniza los comandos con delay para evitar rate limits"""
    try:
        if guild_id:
            # Sync específico para un guild
            guild = bot.get_guild(guild_id)
            if not guild:
                await ctx.send("❌ Guild no encontrado")
                return
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            await ctx.send(f"✅ Comandos sincronizados para {guild.name}")
        else:
            # Sync global con delay
            await ctx.send("⏳ Iniciando sincronización global...")
            await asyncio.sleep(2)  # Delay para evitar rate limit
            synced = await bot.tree.sync()
            await ctx.send(f"✅ {len(synced)} comandos sincronizados globalmente")

    except discord.errors.Forbidden:
        await ctx.send("❌ No tengo permisos para sincronizar comandos")
    except Exception as e:
        logger.error(f"Error en sync: {e}")
        await ctx.send(f"❌ Error: {str(e)}")


# Mantén todas las importaciones y configuraciones previas hasta la clase DailyCommands...
# Registrar todos los mensajes enviados al bot
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    logger.info(
        f"Mensaje recibido de {message.author.name} en #{message.channel.name}: {message.content}"
    )
    await bot.process_commands(
        message
    )  # Permite que otros comandos procesen el mensaje


# Registrar interacciones de comandos slash
@bot.event
async def on_interaction(interaction: discord.Interaction):
    try:
        if interaction.type == discord.InteractionType.application_command:
            logger.info(
                f"Comando slash ejecutado: {interaction.command.name} "
                f"por {interaction.user.name} en {interaction.guild.name}"
            )
    except Exception as e:
        logger.error(f"Error en on_interaction: {e}")


# Manejo de errores en comandos
@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Error ejecutando comando: {error}")
    await ctx.send(f"Hubo un error ejecutando el comando: {error}")


async def enviar_recordatorio(team_id: int, member_id: int):
    response = requests.get(f"{FLASK_API_URL}/api/obtener_equipo/{team_id}")
    if response.status_code != 200:
        logger.error(f"Error obteniendo equipo {team_id}: {response.status_code}")
        return
    equipo_info = response.json()
    channel_id = equipo_info.get("channel_id")
    canal = bot.get_channel(channel_id)
    if not canal:
        logger.error(f"El canal con ID {channel_id} no se encontró.")
        return

    member = canal.guild.get_member(member_id)
    if not member:
        logger.error(f"Miembro con ID {member_id} no encontrado.")
        return

    mensaje = f"{member.mention}, recuerda completar tu daily para el día de hoy."
    await canal.send(mensaje)


@tasks.loop(hours=24)
async def daily_reminder():
    try:
        team_id = 1
        test_member_id = 123456789012345678
        await enviar_recordatorio(team_id, test_member_id)
    except Exception as e:
        logger.error(f"Error en daily_reminder: {e}")


@daily_reminder.before_loop
async def before_daily_reminder():
    await bot.wait_until_ready()


if __name__ == "__main__":
    logger.info("Iniciando bot...")
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        logger.error(f"Error al iniciar el bot: {e}")
