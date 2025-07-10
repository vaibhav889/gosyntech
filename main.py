from threading import Thread
from web import run

Thread(target=run).start()

import discord
from discord import app_commands
from discord.app_commands import Choice
import requests
import random
from langdetect import detect
import os
import time

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
GOSYNTECH_USER = os.getenv("GOSYNTECH_USER")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
SERVER_NAME = os.getenv("SERVER_NAME")
ADMIN_IDS = [int(uid) for uid in os.getenv("ADMIN_IDS", "").split(",") if uid]
MINECRAFT_CHANNEL_NAME = 'the-delta-chat'

BASE_URL = "https://gosyntech.in/api/v1/index.php"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

RESPONSE_MAP = {
    'en': [
        "You're the kind of noob who thinks gravel is a great building block.",
        "You punch trees like it's an Olympic sport—but still no wood.",
        "You died to a chicken, didn't you?",
        "Even villagers shake their heads at your gameplay.",
        "You build with dirt and call it modern architecture.",
        "You mine coal thinking it's diamond. Classic.",
        "Your redstone is worse than spaghetti wiring.",
        "You're the creeper of the group—unwanted and explosive.",
        "You fell in lava again? That's talent.",
        "You think obsidian breaks with a wooden pickaxe?",
        "The only thing you’ve ever conquered is your own confusion.",
        "Even a silverfish has more skill than you.",
        "Mojang should patch you out.",
        "Your nether portal leads to a noob dimension.",
        "You place water in the Nether and expect it to work.",
        "Skeletons hit you more than your crush ever did.",
        "You tried to tame a creeper, didn’t you?",
        "Your builds look like AI-generated trash.",
        "Your mining strategy: dig straight down and pray.",
        "Even zombies run away from your IQ.",
        "You call TNT 'advanced mining equipment'.",
        "Your compass points to 'L'.",
        "You wear leather armor and act invincible.",
        "You thought punching Ender Dragon was a good idea.",
        "Your Minecraft knowledge is from 2012 memes.",
        "You sleep in the End and wonder why you died.",
        "You asked if diamonds grow on trees.",
        "You think redstone is magic. Hogwarts drop-out?",
        "You build nether portals with crying obsidian.",
        "Your parkour skills embarrass slimes.",
        "Even phantoms find you boring.",
        "Villagers charge extra just to deal with you.",
        "You swim in lava and blame Mojang.",
        "You craft a hoe before a pickaxe. Priorities, right?",
        "Your Minecraft house is a box with no roof.",
        "You fell off a ladder in creative mode.",
        "You dig dirt with a sword. Respect.",
        "You tried to milk a zombie cow.",
        "You use flint and steel for cooking.",
        "You put torches underwater and rage when they break.",
        "Your sword has Bane of Noobs enchantment.",
        "You tried to eat diamonds for health regen.",
        "You use sugar cane as a weapon.",
        "You use gravel to build staircases.",
        "Even ghasts say you're bad at aiming.",
        "You thought a beacon is a fancy torch.",
        "You put a chest in lava and wonder why it burns.",
        "You drown in one block of water.",
        "Minecraft’s debug stick couldn’t fix you.",
    ],
    'hi': [
        "Tu itna noob hai ki cobblestone ko diamond samajhta hai.",
        "Tu toh wooden sword se Ender Dragon maarne gaya tha!",
        "Creative mode mein bhi tu mar jaata hai.",
        "Zombie tujhe dekh ke rotate ho jaata hai.",
        "Dirt se ghar banake khud ko architect samajhta hai.",
        "Tu lava mein jump karke kehta hai paani hai shayad.",
        "Minecraft ne tujhe ignore kar diya, tu bhi game uninstall kar de.",
        "Tu ghar banata hai bina door ke.",
        "Tu obsidian ko wooden pickaxe se todta hai.",
        "Nether portal banana bhi nahi aata tujhe.",
        "Ghast tujhe dekh ke ulti kar dete hain.",
        "Tu iron ko gold samajh ke khush hota hai.",
        "Skeleton tujhe sniper training deta hai roz.",
        "Tu piston lagake redstone bhool jaata hai.",
        "Tere build dekh ke villagers bhi migrate kar jaate hain.",
        "Tu boat se lava paar karne jaata hai.",
        "Tu Minecraft mein bhi salary maangta hai.",
        "Tu bed ko lava mein lagata hai.",
        "Tu creeper ko hug karne jaata hai.",
        "Endermen tujhe ignore karte hain.",
        "Tu ladder chadhte chadhte gir jaata hai.",
        "Tu crafting table mein bed banana bhool gaya tha.",
        "Tu shovel se cow maarne gaya tha.",
        "Tu compass ko spinner samajhta hai.",
        "Tu slime ko friend banane gaya tha.",
        "Tu parrot ko blaze samajh kar maar diya.",
        "Tu zombie se dosti karne gaya tha.",
        "Tu elytra pe chadh kar ghoomne gaya tha.",
        "Tu horse pe bed lagake sona chahta tha.",
        "Tu cactus khaane ki koshish karta hai.",
        "Tu beacon ko disco light samajhta hai.",
        "Tu sand mein house banake surprise hota hai jab girta hai.",
        "Tu skeleton ko snowman bolta hai.",
        "Tu creeper ke saath selfie leta hai.",
        "Tu fire resistance potion pee ke pani mein jaata hai.",
        "Tu enchanted book ko padhne ki koshish karta hai.",
        "Tu end portal mein fishing karta hai.",
        "Tu TNT se base design karta hai.",
        "Tu tree punch karta hai aur rage quit kar deta hai.",
        "Tu piston se nether gate kholna chahta hai.",
        "Tu dirt sword banana chahta hai.",
        "Tu horse ko armor pehnata hai aur saddle bhool jaata hai.",
        "Tu spawn point nether mein set karta hai.",
        "Tu bedrock ko shovel se todne ki koshish karta hai.",
        "Tu spider se race karta hai.",
        "Tu torch se dragon maarne gaya tha.",
        "Tu desert temple mein dance karta hai.",
        "Tu zombie villager ko marriage proposal deta hai.",
        "Tu netherite armor lava mein fake ke test karta hai.",
    ],
    'hin': [
        "Tu toh iron ke jagah gold le aaya tha.",
        "Tu wooden sword se creeper ko maar raha tha.",
        "Tu AFK gaya aur lava mein tap gaya.",
        "Tu creative mein bhi fall damage leta hai.",
        "Tu obsidian ko punch karke tod raha tha.",
        "Tu diamond pe furnace laga deta hai.",
        "Tu ghast ke saamne khada ho jaata hai bina bow ke.",
        "Tu zombie ke saath base share karta hai.",
        "Tu beacon ko decorative light samajhta hai.",
        "Tu water bucket lava mein daal ke pool banana chahta hai.",
        "Tu creeper ke explosion ko fireworks bolta hai.",
        "Tu flint and steel se cake bake karne jaata hai.",
        "Tu crafting table se stairs banane ki koshish karta hai.",
        "Tu pumpkin helmet pehn ke End jaata hai.",
        "Tu boat mein horse le jaata hai nether mein.",
        "Tu fishing rod se creeper kheechta hai.",
        "Tu XP farm mein mar jaata hai.",
        "Tu ladders ko bed samajh ke leta hai.",
        "Tu parrot ko phantom samajh ke uda deta hai.",
        "Tu iron sword se obsidian todta hai.",
        "Tu enchanting table pe khaana rakh deta hai.",
        "Tu grass block ko diamond block bolta hai.",
        "Tu TNT se mining karta hai bina armor ke.",
        "Tu door pe pressure plate lagata hai nether mein.",
        "Tu cobweb mein fas jaata hai creative mein.",
        "Tu fox ko tame karne mein khud cat ban jaata hai.",
        "Tu glass ke ghar mein nether portal banata hai.",
        "Tu creeper ka naam rakhta hai 'Bestie'.",
        "Tu command block se door open karta hai survival mein.",
        "Tu warden ko dog samajh ke bone deta hai.",
        "Tu mob farm mein ghus ke spawn block tor deta hai.",
        "Tu parrot ke saath music sunta hai aur jalta bhi hai.",
        "Tu cauldron mein jump karke clean hona chahta hai.",
        "Tu glow squid ko XP source samajhta hai.",
        "Tu donkey ko chest samajh ke bharta rehta hai.",
        "Tu armor stand ko army bolta hai.",
        "Tu boat se water park banata hai.",
        "Tu creeper se chat karta hai discord pe.",
        "Tu slime pe jump karke bhi gir jaata hai.",
        "Tu potion of swiftness pee ke still slow hai.",
        "Tu sand ko ladder bolta hai.",
        "Tu cactus pe garden banata hai.",
        "Tu TNT cart ko roller coaster bolta hai.",
        "Tu redstone repeater ko clock bolta hai.",
        "Tu snowman se lava clean karwata hai.",
        "Tu anvil ko trap banata hai.",
        "Tu xp ko collect karke chest mein daalna chahta hai.",
        "Tu bed nether mein set karta hai daily.",
        "Tu blaze ko light source banata hai.",
    ],
    'kok': [
        "Tu Minecraft-u khelcho nakoso, tu Mario-u khel.",
        "Tuje gravel-u ani diamond-u farak zaina!",
        "Dirt-u ghevun tower kortolo re tu?",
        "Tu ghara bandta glass ani lava ghevun.",
        "Creeper mhun 'maka ek zodd' ani phatlo.",
        "Redstone-u tujya hatant aslo mhun server crash zalo.",
        "Tuje gameplay mhaka lagta mod asa!",
        "Tu obsidian-u shovel ani todta.",
        "Creeper-u tujya side-u yeta naka.",
        "Tu bed-u nether-u ghalun zopta re?",
        "Tu XP-u ghevun chest-u bhorp kortolo.",
        "Tuje fishing rod-u zombie gheun eta.",
        "Tu spider-u ride kortolo?",
        "Tu bucket-u ghevun lava-u pitta.",
        "Tu horse-u ni ladder chaddta.",
        "Tu warden-u patta kortolo!",
        "Tu cauldron-u bath gheta.",
        "Tu slime-u jump marun potta.",
        "Tu fox-u tame korunk self-u cat jallo.",
        "Tu ghast-u kiteak bow-u sodta naka?",
        "Tu flint and steel-u cake bake kortolo.",
        "Tu mob farm-u survival-u maze karta.",
        "Tu zombie ke wedding invite pathaun dita.",
        "Tu bone-u blaze ke fankta.",
        "Tu ghara glass-u ani firework-u full asa.",
        "Tu Minecraft-u UI samzat naka.",
        "Tu sand-u ni beacon ghalta.",
        "Tu potion-u ghetun hunger vatta.",
        "Tu XP farm-u torun naka re!",
        "Tu turtle-u ni creeper confuse korta.",
        "Tu netherite-u test kortolo lava-u fankun.",
        "Tu glowstone-u flashlight samajta.",
        "Tu command block-u banner samajta.",
        "Tu donkey-u refrigerator banavta.",
        "Tu parrot-u ni phantom fight korta.",
        "Tu snowman-u lava clean korta.",
        "Tu boat-u ani minecart exchange korta.",
        "Tu dirt-u ni glass-u mix korta.",
        "Tu grass block-u diamond bolta.",
        "Tu torch-u pani andar ghalta.",
        "Tu warden-u dog bolta ani bone dita.",
        "Tu fire resistance peeun pani vatla.",
        "Tu creeper-u side photo gheta.",
        "Tu skeleton-u ghara invite korta.",
        "Tu nether portal-u painting vatta.",
        "Tu cow-u milk kaddta paache drink kortolo lava-u.",
        "Tu carrot sword banavta.",
        "Tu sand farm-u karun glass decorate kortolo.",
    ]
}

SUPPORTED_LANGS = RESPONSE_MAP.keys()

def detect_language(text):
    try:
        lang = detect(text)
        if lang in SUPPORTED_LANGS:
            return lang
        elif lang == 'hi':
            return 'hi'
        elif lang == 'en':
            return 'en'
        else:
            return 'en'
    except:
        return 'en'

def generate_response(lang):
    responses = RESPONSE_MAP.get(lang, RESPONSE_MAP['en'])
    return random.choice(responses)

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
        await interaction.response.send_message("🚀 Server is starting!" if r.status_code == 200 else "❌ Failed to start server.", ephemeral=True)

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

    usage = r2.json().get("server_usage", {})

    status = usage.get("server_status", "unknown")
    uptime = usage.get("uptime", "N/A")
    ram = usage.get("ram_usage", "N/A")
    cpu = usage.get("cpu_usage", "N/A")
    disk = usage.get("disk_usage", "N/A")
    ip = "McDelta.2tps.pro:10789"

    embed = discord.Embed(title=f"📊 Server Panel - {SERVER_NAME}", color=discord.Color.blurple())
    embed.add_field(name="Status", value=status, inline=True)
    embed.add_field(name="Uptime", value=uptime, inline=True)
    embed.add_field(name="IP", value=ip, inline=False)
    embed.add_field(name="RAM", value=ram, inline=True)
    embed.add_field(name="CPU", value=cpu, inline=True)
    embed.add_field(name="Disk", value=disk, inline=True)

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

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    bot_mentioned = client.user.mention in message.content

    if str(channel.name) == MINECRAFT_CHANNEL_NAME or bot_mentioned:
        lang = detect_language(message.content)
        roast = generate_response(lang)
        await message.reply(roast)
        
try:
    client.run(TOKEN)
except Exception as e:
    print("Bot failed to start:", e)
