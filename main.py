from threading import Thread
from web import run

Thread(target=run).start()

import discord
from discord import app_commands
from discord.app_commands import Choice
import requests
import os
import time

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
GOSYNTECH_USER = os.getenv("GOSYNTECH_USER")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
SERVER_NAME = os.getenv("SERVER_NAME")
ADMIN_IDS = [int(uid) for uid in os.getenv("ADMIN_IDS", "").split(",") if uid]

BASE_URL = "https://gosyntech.in/api/v1/index.php"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def is_admin(user_id):
    return user_id in ADMIN_IDS

def gosyntech_api(action, extra_params=""):
    return f"{BASE_URL}?user={GOSYNTECH_USER}&auth_token={AUTH_TOKEN}&action={action}&server_name={SERVER_NAME}{extra_params}"

class ServerControlView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        r = requests.get(gosyntech_api("start_server"))
        await interaction.response.send_message("✅ Server starting..." if r.status_code == 200 else "❌ Failed to start server.", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_admin(interaction.user.id):
            return await interaction.response.send_message("❌ Not authorized.", ephemeral=True)
        r = requests.get(gosyntech_api("stop_server"))
        await interaction.response.send_message("🛑 Server stopping..." if r.status_code == 200 else "❌ Failed to stop.", ephemeral=True)

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.primary)
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_admin(interaction.user.id):
            return await interaction.response.send_message("❌ Not authorized.", ephemeral=True)
        r = requests.get(gosyntech_api("restart_server"))
        await interaction.response.send_message("🔁 Restarting..." if r.status_code == 200 else "❌ Failed to restart.", ephemeral=True)

@tree.command(name="panel", description="Show server status panel")
async def panel(interaction: discord.Interaction):
    await interaction.response.defer()
    r1 = requests.get(gosyntech_api("show_server_info"))
    r2 = requests.get(gosyntech_api("fetch_server_usage"))

    if r1.status_code != 200 or r2.status_code != 200:
        return await interaction.followup.send("❌ Failed to fetch server data.")

    info = r1.json()
    usage = r2.json()

    embed = discord.Embed(title=f"📊 Server Panel - {SERVER_NAME}", color=discord.Color.blue())
    embed.add_field(name="Status", value=info.get("status", "N/A"), inline=True)
    embed.add_field(name="Uptime", value=usage.get("uptime", "N/A"), inline=True)
    embed.add_field(name="IP", value="McDelta.2tps.pro:10789", inline=False)
    embed.add_field(name="RAM", value=f"{usage.get('ram_used', 'N/A')} / {usage.get('ram_total', 'N/A')} MB", inline=True)
    embed.add_field(name="CPU", value=f"{usage.get('cpu_used', 'N/A')} / {usage.get('cpu_total', 'N/A')} %", inline=True)
    embed.add_field(name="Disk", value=f"{usage.get('disk_used', 'N/A')} / {usage.get('disk_total', 'N/A')} MB", inline=True)
    await interaction.followup.send(embed=embed, view=ServerControlView(interaction.user.id))

# Existing commands stay the same...

# (The rest of your commands like start, stop, restart, cmd, backup, etc., remain unchanged below this point)

@tree.command(name="start", description="Start the Minecraft server")
async def start(interaction: discord.Interaction):
    await interaction.response.defer()
    r = requests.get(gosyntech_api("start_server"))
    if r.status_code == 200:
        await interaction.followup.send("🚀 Server is starting!")
    else:
        await interaction.followup.send("❌ Failed to start the server.")

@tree.command(name="stop", description="Stop the Minecraft server (admin only)")
async def stop(interaction: discord.Interaction):
    await interaction.response.defer()
    if not is_admin(interaction.user.id):
        return await interaction.followup.send("❌ You’re not allowed to use this.")
    r = requests.get(gosyntech_api("stop_server"))
    await interaction.followup.send("🛑 Server stopping..." if r.status_code == 200 else "❌ Failed to stop.")

@tree.command(name="restart", description="Restart the Minecraft server (admin only)")
async def restart(interaction: discord.Interaction):
    await interaction.response.defer()
    if not is_admin(interaction.user.id):
        return await interaction.followup.send("❌ You’re not allowed to use this.")
    r = requests.get(gosyntech_api("restart_server"))
    await interaction.followup.send("🔁 Restarting..." if r.status_code == 200 else "❌ Failed to restart.")

@tree.command(name="status", description="Get server status")
async def status(interaction: discord.Interaction):
    await interaction.response.defer()
    r = requests.get(gosyntech_api("show_server_info"))
    if r.status_code != 200:
        return await interaction.followup.send("❌ Failed to fetch server info.")
    data = r.json()
    state = data.get("status", "unknown")
    await interaction.followup.send(f"📊 Server status: **{state.upper()}**")

@tree.command(name="ip", description="Get the Minecraft server IP")
async def ip(interaction: discord.Interaction):
    await interaction.response.send_message("📡 Server IP: `McDelta.2tps.pro:10789`")

@tree.command(name="uptime", description="Get server uptime")
async def uptime(interaction: discord.Interaction):
    await interaction.response.defer()
    r = requests.get(gosyntech_api("fetch_server_usage"))
    if r.status_code != 200:
        return await interaction.followup.send("❌ Failed to fetch server usage.")
    data = r.json()
    uptime = data.get("uptime", "N/A")
    await interaction.followup.send(f"🕒 Uptime: {uptime}")

@tree.command(name="website", description="View the SMP's official website")
async def website(interaction: discord.Interaction):
    await interaction.response.send_message("🌍 Visit our official website: https://mcdeltasmp.vercel.app/")

@tree.command(name="vote", description="Vote for the SMP")
async def vote(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**🗳 Vote for McDelta SMP!**\n"
        "1. https://discordservers.com/bump/1354330313240871022\n"
        "2. https://discords.com/servers/1354330313240871022/upvote\n"
        "3. https://discadia.com/vote/mcdeltasmp/"
    )

@tree.command(name="cmd", description="Run a console command (admin only)")
@app_commands.describe(command="The command to run")
async def cmd(interaction: discord.Interaction, command: str):
    await interaction.response.defer()
    if not is_admin(interaction.user.id):
        return await interaction.followup.send("❌ You are not authorized.")
    encoded_command = requests.utils.quote(command)
    r = requests.get(gosyntech_api("send_command", f"&command={encoded_command}"))
    await interaction.followup.send(f"✅ Sent command: `{command}`" if r.status_code == 200 else "❌ Failed to send command.")

@tree.command(name="backup", description="Backup server (admin only)")
@app_commands.describe(action="Action to perform")
@app_commands.choices(action=[
    Choice(name="create", value="create"),
    Choice(name="delete", value="delete"),
])
async def backup(interaction: discord.Interaction, action: Choice[str]):
    await interaction.response.defer()
    if not is_admin(interaction.user.id):
        return await interaction.followup.send("❌ You are not authorized.")

    if action.value == "create":
        r = requests.get(gosyntech_api("create_backup"))
        await interaction.followup.send("✅ Backup started." if r.status_code == 200 else "❌ Failed to create backup.")

    elif action.value == "delete":
        r = requests.get(gosyntech_api("delete_backup"))
        await interaction.followup.send("🗑 Backup deleted." if r.status_code == 200 else "❌ Failed to delete backup.")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        print("Registering commands manually...")
        guild = discord.Object(id=GUILD_ID)
        tree.copy_global_to(guild=guild)
        synced = await tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"Sync failed: {e}")
        
try:
    client.run(TOKEN)
except Exception as e:
    print("Bot failed to start:", e)
