from threading import Thread
from web import run

Thread(target=run).start()

import discord
from discord import app_commands
from discord.app_commands import Choice
import aiohttp
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
GOSYNTECH_USER = os.getenv("GOSYNTECH_USER")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
SERVER_NAME = os.getenv("SERVER_NAME")
ADMIN_IDS = [int(uid) for uid in os.getenv("ADMIN_IDS", "").split(",") if uid]

BASE_URL = "https://gosyntech.in/api/v1/index.php"
SERVER_IP = "McDelta.2tps.pro:10789"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def is_admin(user_id):
    return user_id in ADMIN_IDS

def gosyntech_api(action, extra_params=""):
    return f"{BASE_URL}?user={GOSYNTECH_USER}&auth_token={AUTH_TOKEN}&action={action}&server_name={SERVER_NAME}{extra_params}"

async def safe_api_call(action, extra_params=""):
    url = gosyntech_api(action, extra_params)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    return {"success": False, "message": f"API error: {resp.status}"}
                try:
                    return await resp.json()
                except aiohttp.ContentTypeError:
                    return {"success": False, "message": "❌ Invalid JSON response"}
    except aiohttp.ClientError as e:
        print(f"API error: {e}")
        return {"success": False, "message": "❌ API unreachable"}

class ServerControlView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = await safe_api_call("start_server")
        success = res.get("success", False)
        msg = res.get("message", "⚠️ Unexpected error")
        await interaction.response.send_message("🚀 Server starting..." if success else f"⚠️ {msg}", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_admin(interaction.user.id):
            return await interaction.response.send_message("❌ Not authorized.", ephemeral=True)
        res = await safe_api_call("stop_server")
        success = res.get("success", False)
        msg = res.get("message", "⚠️ Unexpected error")
        await interaction.response.send_message("🛑 Server stopping..." if success else f"⚠️ {msg}", ephemeral=True)

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.primary)
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_admin(interaction.user.id):
            return await interaction.response.send_message("❌ Not authorized.", ephemeral=True)
        res = await safe_api_call("restart_server")
        success = res.get("success", False)
        msg = res.get("message", "⚠️ Unexpected error")
        await interaction.response.send_message("🔁 Restarting..." if success else f"⚠️ {msg}", ephemeral=True)

@tree.command(name="panel", description="Show server status panel")
async def panel(interaction: discord.Interaction):
    await interaction.response.defer()
    info = await safe_api_call("show_server_info")
    usage = await safe_api_call("fetch_server_usage")

    if not info.get("success") or not usage.get("success"):
        return await interaction.followup.send("❌ Could not fetch server data. Try again later.")

    try:
        usage_data = usage.get("server_usage", {})
        status = usage_data.get("server_status", "Unknown")
        uptime = usage_data.get("uptime", "N/A")
        ram = usage_data.get("ram_usage", "N/A")
        cpu = usage_data.get("cpu_usage", "N/A")
        disk = usage_data.get("disk_usage", "N/A")

        color = discord.Color.green() if status.lower() == "online" else discord.Color.red()
        embed = discord.Embed(title=f"📊 Server Panel - {SERVER_NAME}", color=color)
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="IP", value=SERVER_IP, inline=False)
        embed.add_field(name="RAM", value=ram, inline=True)
        embed.add_field(name="CPU", value=cpu, inline=True)
        embed.add_field(name="Disk", value=disk, inline=True)

        await interaction.followup.send(embed=embed, view=ServerControlView(interaction.user.id))
    except Exception as e:
        print("Error in panel:", e)
        await interaction.followup.send("❌ Error parsing server info.")

@tree.command(name="start", description="Start the Minecraft server")
async def start(interaction: discord.Interaction):
    await interaction.response.defer()
    res = await safe_api_call("start_server")
    success = res.get("success", False)
    msg = res.get("message", "⚠️ Unexpected error")
    await interaction.followup.send("🚀 Server is starting!" if success else f"⚠️ {msg}")

@tree.command(name="stop", description="Stop the Minecraft server (admin only)")
async def stop(interaction: discord.Interaction):
    await interaction.response.defer()
    if not is_admin(interaction.user.id):
        return await interaction.followup.send("❌ You’re not allowed to use this.")
    res = await safe_api_call("stop_server")
    success = res.get("success", False)
    msg = res.get("message", "⚠️ Unexpected error")
    await interaction.followup.send("🛑 Server stopping..." if success else f"⚠️ {msg}")

@tree.command(name="restart", description="Restart the Minecraft server (admin only)")
async def restart(interaction: discord.Interaction):
    await interaction.response.defer()
    if not is_admin(interaction.user.id):
        return await interaction.followup.send("❌ You’re not allowed to use this.")
    res = await safe_api_call("restart_server")
    success = res.get("success", False)
    msg = res.get("message", "⚠️ Unexpected error")
    await interaction.followup.send("🔁 Restarting..." if success else f"⚠️ {msg}")

@tree.command(name="status", description="Get server status")
async def status(interaction: discord.Interaction):
    await interaction.response.defer()
    res = await safe_api_call("show_server_info")
    if not res.get("success"):
        return await interaction.followup.send(f"❌ Could not fetch status: {res.get('message', 'unknown error')}")
    state = res.get("status", "unknown")
    await interaction.followup.send(f"📊 Server status: **{state.upper()}**")

@tree.command(name="ip", description="Get the Minecraft server IP")
async def ip(interaction: discord.Interaction):
    await interaction.response.send_message(f"📡 Server IP: `{SERVER_IP}`")

@tree.command(name="uptime", description="Get server uptime")
async def uptime(interaction: discord.Interaction):
    await interaction.response.defer()
    res = await safe_api_call("fetch_server_usage")
    if not res.get("success"):
        return await interaction.followup.send(f"❌ Failed to fetch uptime: {res.get('message', 'unknown')}")
    uptime = res.get("uptime", "N/A") or res.get("server_usage", {}).get("uptime", "N/A")
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
    encoded_command = command.replace(" ", "%20")
    res = await safe_api_call("send_command", f"&command={encoded_command}")
    success = res.get("success", False)
    msg = res.get("message", "❌ Unexpected error")
    await interaction.followup.send(f"✅ Sent command: `{command}`" if success else f"❌ Failed: {msg}")

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
    action_map = {
        "create": ("create_backup", "✅ Backup started."),
        "delete": ("delete_backup", "🗑 Backup deleted.")
    }
    action_name, success_msg = action_map[action.value]
    res = await safe_api_call(action_name)
    success = res.get("success", False)
    msg = res.get("message", "❌ Unexpected error")
    await interaction.followup.send(success_msg if success else f"❌ Failed: {msg}")

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        tree.copy_global_to(guild=guild)
        synced = await tree.sync(guild=guild)
        print(f"✅ Synced {len(synced)} commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

try:
    client.run(TOKEN)
except Exception as e:
    print("❌ Bot failed to start:", e)
