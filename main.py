from threading import Thread
from web import run

Thread(target=run).start()

import discord
from discord import app_commands
from discord.app_commands import Choice
import requests
import random
import re
from langdetect import detect
import os
import time

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
GOSYNTECH_USER = os.getenv("GOSYNTECH_USER")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
SERVER_NAME = os.getenv("SERVER_NAME")
ADMIN_IDS = [int(uid) for uid in os.getenv("ADMIN_IDS", "").split(",") if uid]
MINECRAFT_CHANNEL_NAME = '🔥get-roasted'

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
        "Creepers high-five each other after blowing you up.",
        "Even Steve would uninstall the game if he saw your skills.",
        "Even the Ender Dragon pities you.",
        "Even your friend says you built a lava pool under your bed.",
        "Even your friend says you called TNT 'instant mining'.",
        "Even your friend says you cooked rotten flesh thinking it’d become steak.",
        "Even your friend says you crafted 64 crafting tables — for backup.",
        "Even your friend says you dug straight down and then blamed gravity.",
        "Even your friend says you enchanted a carrot.",
        "Even your friend says you fought mobs with a stick.",
        "Even your friend says you got lost in your own base.",
        "Even your friend says you logged out in the Nether without a portal.",
        "Even your friend says you named your dirt house 'The Palace'.",
        "Even your friend says you punched a bee hive and blamed the lag.",
        "Even your friend says you put a door on a cactus.",
        "Even your friend says you put your bed in the End as a spawn point.",
        "Even your friend says you tried flying with fireworks and no elytra.",
        "Even your friend says you used a shovel to mine diamonds.",
        "In Minecraft history, you're known for how you built a lava pool under your bed.",
        "In Minecraft history, you're known for how you called TNT 'instant mining'.",
        "In Minecraft history, you're known for how you cooked rotten flesh thinking it’d become steak.",
        "In Minecraft history, you're known for how you crafted 64 crafting tables — for backup.",
        "In Minecraft history, you're known for how you dug straight down and then blamed gravity.",
        "In Minecraft history, you're known for how you enchanted a carrot.",
        "In Minecraft history, you're known for how you fought mobs with a stick.",
        "In Minecraft history, you're known for how you got lost in your own base.",
        "In Minecraft history, you're known for how you logged out in the Nether without a portal.",
        "In Minecraft history, you're known for how you named your dirt house 'The Palace'.",
        "In Minecraft history, you're known for how you punched a bee hive and blamed the lag.",
        "In Minecraft history, you're known for how you put a door on a cactus.",
        "In Minecraft history, you're known for how you put your bed in the End as a spawn point.",
        "In Minecraft history, you're known for how you tried flying with fireworks and no elytra.",
        "In Minecraft history, you're known for how you used a shovel to mine diamonds.",
        "Legend has it you built a lava pool under your bed.",
        "Legend has it you called TNT 'instant mining'.",
        "Legend has it you cooked rotten flesh thinking it’d become steak.",
        "Legend has it you crafted 64 crafting tables — for backup.",
        "Legend has it you dug straight down and then blamed gravity.",
        "Legend has it you enchanted a carrot.",
        "Legend has it you fought mobs with a stick.",
        "Legend has it you got lost in your own base.",
        "Legend has it you logged out in the Nether without a portal.",
        "Legend has it you named your dirt house 'The Palace'.",
        "Legend has it you punched a bee hive and blamed the lag.",
        "Legend has it you put a door on a cactus.",
        "Legend has it you put your bed in the End as a spawn point.",
        "Legend has it you tried flying with fireworks and no elytra.",
        "Legend has it you used a shovel to mine diamonds.",
        "No one but you built a lava pool under your bed.",
        "No one but you called TNT 'instant mining'.",
        "No one but you cooked rotten flesh thinking it’d become steak.",
        "No one but you crafted 64 crafting tables — for backup.",
        "No one but you dug straight down and then blamed gravity.",
        "No one but you enchanted a carrot.",
        "No one but you fought mobs with a stick.",
        "No one but you got lost in your own base.",
        "No one but you logged out in the Nether without a portal.",
        "No one but you named your dirt house 'The Palace'.",
        "No one but you punched a bee hive and blamed the lag.",
        "No one but you put a door on a cactus.",
        "No one but you put your bed in the End as a spawn point.",
        "No one but you tried flying with fireworks and no elytra.",
        "No one but you used a shovel to mine diamonds.",
        "Only you built a lava pool under your bed.",
        "Only you called TNT 'instant mining'.",
        "Only you cooked rotten flesh thinking it’d become steak.",
        "Only you crafted 64 crafting tables — for backup.",
        "Only you dug straight down and then blamed gravity.",
        "Only you enchanted a carrot.",
        "Only you fought mobs with a stick.",
        "Only you got lost in your own base.",
        "Only you logged out in the Nether without a portal.",
        "Only you named your dirt house 'The Palace'.",
        "Only you punched a bee hive and blamed the lag.",
        "Only you put a door on a cactus.",
        "Only you put your bed in the End as a spawn point.",
        "Only you tried flying with fireworks and no elytra.",
        "Only you used a shovel to mine diamonds.",
        "People laugh when you build a lava pool under your bed.",
        "People laugh when you call TNT 'instant mining'.",
        "People laugh when you cook rotten flesh thinking it’d become steak.",
        "People laugh when you craft 64 crafting tables — for backup.",
        "People laugh when you dig straight down and then blame gravity.",
        "People laugh when you enchant a carrot.",
        "People laugh when you fight mobs with a stick.",
        "People laugh when you get lost in your own base.",
        "People laugh when you log out in the Nether without a portal.",
        "People laugh when you name your dirt house 'The Palace'.",
        "People laugh when you punch a bee hive and blame the lag.",
        "People laugh when you put a door on a cactus.",
        "People laugh when you put your bed in the End as a spawn point.",
        "People laugh when you try flying with fireworks and no elytra.",
        "People laugh when you use a shovel to mine diamonds.",
        "They say you built a lava pool under your bed.",
        "They say you called TNT 'instant mining'.",
        "They say you cooked rotten flesh thinking it’d become steak.",
        "They say you crafted 64 crafting tables — for backup.",
        "They say you dug straight down and then blamed gravity.",
        "They say you enchanted a carrot.",
        "They say you fought mobs with a stick.",
        "They say you got lost in your own base.",
        "They say you logged out in the Nether without a portal.",
        "They say you named your dirt house 'The Palace'.",
        "They say you punched a bee hive and blamed the lag.",
        "They say you put a door on a cactus.",
        "They say you put your bed in the End as a spawn point.",
        "They say you tried flying with fireworks and no elytra.",
        "They say you used a shovel to mine diamonds.",
        "You're the kind of player who builds lava pools under beds.",
        "You're the kind of player who calls TNT 'instant mining'.",
        "You're the kind of player who cooks rotten flesh hoping it’s steak.",
        "You're the kind of player who crafts 64 crafting tables for fun.",
        "You're the kind of player who digs straight down — proudly.",
        "You're the kind of player who enchants a carrot and flexes it.",
        "You're the kind of player who fights mobs with flowers.",
        "You're the kind of player who gets lost inside their own house.",
        "You're the kind of player who logs out in the Nether with no portal.",
        "You're the kind of player who names a mud hut 'Luxury Villa'.",
        "You're the kind of player who punches bee hives and runs.",
        "You're the kind of player who places doors on cacti.",
        "You're the kind of player who tries to sleep in the End.",
        "You're the kind of player who tries elytra flight without elytra.",
        "You're the kind of player who uses a shovel on diamonds.",
        "You actually built a lava pool under your bed.",
        "You actually called TNT 'instant mining'.",
        "You actually cooked rotten flesh for steak.",
        "You actually crafted 64 crafting tables and ran out of wood.",
        "You actually dug straight down and fell in lava.",
        "You actually enchanted a carrot.",
        "You actually fought mobs with a stick.",
        "You actually got lost in your own starter base.",
        "You actually logged out in the Nether without thinking.",
        "You actually named a dirt shack 'God Base'.",
        "You actually punched a beehive wearing no armor.",
        "You actually put a door on a cactus thinking it's smart.",
        "You actually set your spawn in the End.",
        "You actually tried flying with fireworks and died instantly.",
        "You actually used a shovel to mine your first diamond.",
        "Your legacy is that you built lava pools indoors.",
        "Your legacy is that you renamed TNT as 'digging device'.",
        "Your legacy is cooking rotten flesh like it’s gourmet.",
        "Your legacy is flooding servers with crafting tables.",
        "Your legacy is digging into lava and yelling 'bruh'.",
        "Your legacy is enchanting carrots instead of gear.",
        "Your legacy is dying to bees — with a shield equipped.",
        "Your legacy is logging out mid creeper explosion.",
        "Your legacy is putting glass roofs on dirt huts.",
        "Your legacy is calling wooden swords ‘OP weapons’.",
        "Your legacy is PvPing using rotten flesh.",
        "Your legacy is thinking doors block explosions.",
        "Your legacy is sleeping in the End because why not.",
        "Your legacy is flying with no armor and no brain.",
        "Your legacy is shoveling your diamonds away.",
        "You smelted gravel and hoped it’d become diamonds.",
        "You once dug up into lava — twice.",
        "You placed lava in your house for lighting.",
        "You decorated your house with raw porkchops.",
        "You renamed dirt blocks to 'diamond'.",
        "You traded emeralds for dirt — and said good deal.",
        "You bred creepers thinking you’d get a charged one.",
        "You set your base next to 4 spawners — and died daily.",
        "You swam in lava to see what happens.",
        "You broke your only pickaxe mining obsidian.",
        "You made your bed out of TNT and clicked it.",
        "You slept during thunderstorms and called it strategy.",
        "You used snowballs in a wither fight — smart.",
        "You hit a golem and thought it wouldn't fight back.",
        "You built your beacon with cobblestone.",
        "You fished in the Nether — because why not.",
        "You tried making armor from redstone.",
        "You used chorus fruit to escape — into lava.",
        "You used a trapdoor as your shield.",
        "You tried to shear a creeper.",
        "You bridged with ice in the Nether.",
        "You made a nether portal using lava and wood.",
        "You trapped yourself in your own base with obsidian.",
        "You used flint and steel on your bed."
        "You started a hardcore world and died to a berry bush.",
        "You called a shovel 'the ultimate weapon'.",
        "You used a banner to fight off pillagers.",
        "You made a piston door that crushed yourself.",
        "You built a lava moat then fell in it.",
        "You used soul sand in your base flooring.",
        "You fought a spider jockey — and lost to the spider.",
        "You fell off a 3-block jump and blamed lag.",
        "You drowned in a 1-block deep puddle.",
        "You chased an Enderman during rain — genius.",
        "You slept in a bed surrounded by pressure plates.",
        "You summoned lightning — onto yourself.",
        "You broke your only torch in a creeper cave.",
        "You made a rollercoaster that ends in lava.",
        "You mined bedrock because 'YouTube said so'.",
        "You made a 1x1 tower and called it defense.",
        "You ran from a chicken jockey — and still died.",
        "You used gravel as scaffolding in a ravine.",
        "You died in a desert from snowballs.",
        "You thought you could break obsidian with your fists.",
        "You tried PvP using a cooked potato.",
        "You placed cactus next to your chest — big brain.",
        "You walked into your own redstone trap.",
        "You fought a blaze using a fishing rod.",
        "You spawned wither in your base — for fun.",
        "You hid in a boat during a raid.",
        "You fell off your own skyblock.",
        "You went AFK in the End.",
        "You tried to trap a phantom — and failed.",
        "You opened a trapped chest with TNT under it.",
        "You drank milk instead of healing.",
        "You ran from villagers with sticks.",
        "You placed lava in the overworld treehouse.",
        "You looted your own house.",
        "You fell in a one-block hole and starved.",
        "You got lost in a 3x3 bunker.",
        "You asked for a tutorial — to walk.",
        "You died to a falling anvil — placed by you.",
        "You summoned mobs — then forgot to run.",
        "You enchanted a flint and steel with knockback.",
        "You launched fireworks at a skeleton — and missed every shot."
    ],
    'hin': [
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
        "tu itna noob hai ki creeper bhi tujhe ignore karta hai.",
        "tera ghar dirt se zyada bekaar dikhta hai.",
        "tu ne lava mein swimming seekhne ki koshish ki — aur jala gaya.",
        "tu ne bedrock mine karne ki koshish ki — fist se.",
        "tu creative mode mein bhi mar jaata hai.",
        "ender dragon bhi tera gameplay dekh ke roya.",
        "tu nether mein bed rakh ke so gaya — legend!",
        "tera armor sirf decoration ke liye hota hai.",
        "tu turtle se race hara — dono baar.",
        "tu piston ko bhi confuse kar deta hai.",
        "tera redstone setup microwave se complex hai.",
        "tu obsidian ko haathon se todta hai.",
        "tu fox ko bone se tame karne gaya.",
        "tera dog bhi tujhe bite karta hai.",
        "tu creeper se pyaar se milne gaya — blast gift mila.",
        "tu diamond pickaxe se dirt todta hai.",
        "tera beacon cobblestone se bana hota hai.",
        "tu elytra pe fireworks chala ke gir gaya.",
        "tu khud apne hi trap mein fasa.",
        "tu nether portal banate waqt pani daal diya.",
        "tu end mein bed set kar ke so gaya.",
        "tu hardcore world shuru karke pehli raat mein mar gaya.",
        "tu afk chhod ke gaya, creeper party ho gayi.",
        "tu parkour try karta hai aur spawn pe laut aata hai.",
        "tu command likhta hai: /failmepls",
        "tera skeleton se ladte waqt khud hi damage ho jaata hai.",
        "tera nether base wooden planks se bana hai.",
        "tu gravel se bridge banata hai, aur gir jaata hai.",
        "tu boat mein hide karta hai raid se.",
        "tu potion ko pee kar ke bolta hai 'aur kuch nahi hua?'",
        "tu lava bucket ko potion samajh ke pi gaya.",
        "tu redstone repeater ko table ka decoration samajhta hai.",
        "tu ender pearl se teleport hokar lava mein land kiya.",
        "tu zombie ke sath hug karne gaya — RIP.",
        "tu hardcore world mein peaceful mode chalu kar deta hai.",
        "tu phantom ko trap karne gaya aur upar se gira.",
        "tu piston door banake khud ko crush kar leta hai.",
        "tu iron golem ko thappad maar deta hai — aur fir bhagta hai.",
        "tu fishing rod se blaze se ladta hai.",
        "tu torch tod deta hai jab creeper saamne aata hai.",
        "tu inventory mein sirf dirt aur seeds rakhta hai.",
        "tera spawn point lava ke beech mein hota hai.",
        "tu beacon ke upar khud baith gaya shine lene.",
        "tu zombie farm banata hai jahan zombie hi nahi aate.",
        "tu firework launch karke khud ud jaata hai building se.",
        "tu totem use karne se pehle mar jaata hai.",
        "tera PvP spectator mode mein bhi boring lagta hai.",
        "tu crafting table bana ke bhool jaata hai kaise use karna hai.",
        "tu sugarcane farm mein wheat ugaane ki koshish karta hai.",
        "tu enchanting table se sirf curse nikalta hai.",
        "tu turtle ko boat mein daal ke bolta hai race jeet gaya.",
        "tu logon ko coal gift mein deta hai.",
        "tu command block se apne aap ko ban kar leta hai.",
        "tu respawn point ke bagal mein TNT laga deta hai.",
        "tu spawn hote hi skeleton se mar jaata hai.",
        "tu potion throw karta hai khud pe poison wala.",
        "tu parkour mein chadhte hi gir jaata hai.",
        "tu armor pe bane pattern ko enchantment samajhta hai.",
        "tu bed ke andar TNT laga ke test karta hai.",
        "tu chat mein spam karta hai 'give diamonds pls'.",
        "tera base ka darwaza ulta lagaya hua hai.",
        "tu trapdoor ko bed samajh leta hai.",
        "tu nether mein paani dalne ki koshish karta hai.",
        "tu fall damage se zyada embarrassment mein mar jaata hai.",
        "tu scoreboard mein sirf 'deaths' mein top karta hai.",
        "tu dog ko attack karta hai aur fir bhagta hai.",
        "tu command likhne se pehle grammar check karta hai.",
        "tu crafting karte waqt bhi tutorial dekhta hai.",
        "tu dirt blocks ko rename karke diamond kehta hai.",
        "tu skeleton se fight karte waqt arrows khud pe chalata hai.",
        "tu PvP fight mein rotten flesh use karta hai.",
        "tu enderman ko ghoorta hai aur fir bhagta hai.",
        "tu hardcore world mein bed banaana bhool gaya.",
        "tu piston ke sath redstone lagana bhool jaata hai.",
        "tu campfire pe khana pakane ki jagah jal jaata hai.",
        "tu snowball se wither se ladta hai.",
        "tu sugarcane ko bone meal deta hai.",
        "tu sand pe tower banata hai aur gir jaata hai.",
        "tu spectator mode mein bhi direction bhool jaata hai.",
        "tu bed ko decoration ke liye use karta hai nether mein.",
        "tu ice se bridge banata hai nether mein.",
        "tu obsidian todte todte thak jaata hai — fist se.",
        "tu phantom ke saath selfie lene gaya — hospital gaya.",
        "tu redstone se sirf doors open karta hai — kabhi band nahi.",
        "tu Minecraft mein bhi CTRL+Z dhundhta hai.",
        "tu glass pane ke saath fight karta hai.",
        "tu anvil ke neeche khud khada hota hai.",
        "tu hay bale ko cake samajh ke kha leta hai.",
        "tu cobblestone ke ghar pe sign lagata hai 'Diamond Base'.",
        "tu minecart se ride lete waqt lava mein jump kar deta hai.",
        "tu skeleton se fight karta hai aur apna bow tod deta hai.",
        "tu fireworks se blast karta hai par elytra bhool jaata hai.",
        "tu snow golem ko blaze ke samne spawn karta hai.",
        "tu fire resistance ke bina nether swimming karta hai.",
        "tu ender chest mein sirf rotten flesh rakhta hai.",
        "tu fence lagake usi mein phans jaata hai.",
        "tu spectator mode mein bhi mobs se darte ho.",
        "tu afk chhod ke gaya, mob farm tere upar hi spawn ho gaya.",
        "tu beacon banate waqt glass bhool gaya.",
        "tu bamboo se creeper ko rokne ki koshish karta hai.",
        "tu cactus ke upar chest rakh deta hai.",
        "tu soul sand pe sprint karne ki koshish karta hai.",
        "tu parrot ko bread khilata hai.",
        "tu jungle temple mein tripwire ka gift leke mar jaata hai.",
        "tu xp collect karne se pehle mar jaata hai.",
        "tu raid shuru karta hai aur khud hi ghar chhod deta hai.",
        "tu bookshelf ko jalata hai furnace mein.",
        "tu netherite sword se cow kill karta hai aur proud feel karta hai."
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
        "tu itlo noob asa ki creeper tujya sangata explosion karunk zata.",
        "tu TNT ke mining tool mhunn vicharta.",
        "tu aplea bed khallche lava pool bandta — genius idea re!",
        "tu ender pearl vaprun lava madhe teleport zata.",
        "tu obsidian haathani todpak gheta — patience level god!",
        "tu dirtachya ghara'k palace mhunn naav dita.",
        "tu foxak bone diun tame karunk zata.",
        "tu elytra naslem fireworks vapurta — udpak kiteak?",
        "tu piston door vapurta ani thavnch fasta.",
        "tu skeletonak fight korta ani khud aim’k jata.",
        "tu creative mode’m marunk koso zata, eka tu janna.",
        "tu redstone setup asa, bhitor toaster better kam korta.",
        "tu ghara’m nether portal bandta — borem idea!",
        "tu cactusacho side’m chest vapurta ani chirt zata.",
        "tu armor decorate korta, use korpak visroita.",
        "tu nether’m paani marunk zata — science fail!",
        "tu parrotak bread dita — health department shock jata.",
        "tu zombieak hug diun RIP zata.",
        "tu village raid start korta ani mage palta.",
        "tu furnace’m bookshelf jalta — kaim logic asa?",
        "tu spawn zata ani paila step’m void’m girta.",
        "tu potion khudachim head’k marta ani poison zata.",
        "tu wolfak attack korta ani maga sorry mhonta.",
        "tu redstone repeater dekhun 'frame' mhunn vapurta.",
        "tu beacon cobblestoneacho bandta ani proud feel korta.",
        "tu inventory full asa, but only dirt asa bhitor.",
        "tu creeperak hi five divpak zata.",
        "tu skeletonak avoid korta ani zombieak invite karta.",
        "tu afk farm’m fosto ani titlya mobs tuje head’m dance karta.",
        "tu hardcore mode’m peaceful set korta — safety first!",
        "tu turtleak boat’m vapurta ani race start korta.",
        "tu phantomak selfie divpak zata — hospital ready korta.",
        "tu skeletonak bow vapurta ani arrows khud’m lagta.",
        "tu bedrock mine korta fistani — strength level Hulk!",
        "tu door cactus’vor martalo asa — what a craftsman!",
        "tu shovelani diamonds mine korta.",
        "tu nether portal’k water vapurta — confusion max!",
        "tu chat’m spam korta: 'diamonds pls'.",
        "tu armor decorate korta ani enchant forget korta.",
        "tu zombie spawner’m spawn rate zero asa — tujem luck!",
        "tu TNT trap bandta ani khud’m phasto.",
        "tu snowball vapurta wither fight’m — bold move!",
        "tu spectate korta PvP fight’m — ani bored zata.",
        "tu hardcore world’m 1st night’m marun respawn wait korta.",
        "tu farm’m crop vagair soglle weed’che asa.",
        "tu sugarcane farm’m bone meal vapurta.",
        "tu nam ani fame two words confuse korta.",
        "tu ghara’k tor porch asa — ani titlya mobs welcome karta.",
        "tu totem hold korta ani toch marunk marta.",
        "tu minecart ride’m lava jump karta — borem stunt.",
        "tu spawn point lava madhe set korta.",
        "tu base decorate korta sand ani gravel vapurta.",
        "tu dog tujya command ignore korta — respect!",
        "tu skeleton fight’m bow todun kai mop vapurta.",
        "tu netherite sword use korta only animalsak.",
        "tu XP bottle vapurta ani te ek XP point dita.",
        "tu end portal 'gol bhaji' mhunn vicharta.",
        "tu glass pane break korta ani blockak blame karta.",
        "tu blazeak snowball marunk heat kam korta mhunta.",
        "tu soul sand flooring vapurta ani lag mhunta.",
        "tu Elytra vapurta but jata zain teleport na karta.",
        "tu redstone circuit build korta but switch forgot korta.",
        "tu AFK zain creeper tuka surprise dita.",
        "tu scoreboard’m top only deaths category’m.",
        "tu fence lavta ani khud phasta tyam.",
        "tu ender chest'm rotten flesh bharun rikta space korta.",
        "tu xp collect korchea adim mar zata.",
        "tu armor dhor zata ani elytra wear korta.",
        "tu TNT use korta house lighting’m.",
        "tu pickaxe vapurta PvP fight’m.",
        "tu nether portal build korta lava ani wood vapurta.",
        "tu anvil cha khalok ubho zata — kaboom time!",
        "tu trapdoor shield mhunn use korta.",
        "tu ghatta zaina, mobs despawn zata.",
        "tu resource collect korta ani void’m fankta.",
        "tu fall damage’m mar zata 3 block’m.",
        "tu jukebox ani crafting table confuse korta.",
        "tu Elytra vapurta ani head dive lava’m karta.",
        "tu fishing karun obsidian pakarta.",
        "tu snow golem build karta ani samor blaze vapurta.",
        "tu banner ghun PvP fight korta — creative strategy.",
        "tu nether ghara’m lightning summon korta — tujya head’m.",
        "tu fireworks chalu korta ani chimney vapurta.",
        "tu bookshelf ani furnace ekk veg veg samjota.",
        "tu golemak thapp marun bolta 'just kidding'.",
        "tu chicken jockey dekhta ani disconnect karta.",
        "tu light sabha kellya jage’m dark mobsak invite karta.",
        "tu gold armor wear korta ani diamond ditta villagerak.",
        "tu slime farm’m fasta ani movement par shutdown zata.",
        "tu turtleak hit korta ani teen minutes’m sorry mhonta.",
        "tu lightning rod lavta and then stand karta titlya.",
        "tu enchanted carrot flaunt korta.",
        "tu redstone torch lavta ani base phata.",
        "tu ghara chya roof’m water source block lavta.",
        "tu dirtachya tower’k castle mhunta.",
        "tu sheep’k skeleton arrow vapurta.",
        "tu wolfak rotten flesh dita full XP bar’m.",
        "tu campfire’m roast karta but self roast zata.",
        "tu diamond sword lava’m marun clean korta.",
        "tu ender dragonak boat vapurta fight’m.",
        "tu slime ke lag’n nether’k gheun zata.",
        "tu zombie’k trap korta and then opens the door himself.",
        "tu skyblock’m torch forgot korta ani mobs dance karta.",
        "tu spawn houn log out karta — fear max!"
    ]
}

SUPPORTED_LANGS = RESPONSE_MAP.keys()

def get_language(text: str) -> str:
    try:
        lang = detect(text)
        if lang == 'hi':
            return 'hin'
        elif lang == 'en':
            return 'en'
        elif lang == 'kok':
            return 'kok'
        else:
            return 'en'  # default fallback
    except:
        return 'en'  # fallback in case of errors

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
        lang = get_language(message.content)
        roast = generate_response(lang)
        await message.reply(roast)
        
try:
    client.run(TOKEN)
except Exception as e:
    print("Bot failed to start:", e)
