import disnake
from disnake.ext import commands
import json
import os
import platform
import requests

config_file_path = "config.json"
online_version = "https://raw.githubusercontent.com/Guillaume0001/g-pin./main/version.txt"

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        token = input("Enter the bot's token: ")
        prefix = input("Enter the bot's prefix: ")
        log_id = input("Enter the log's channel ID: ")
        registration_id = input("Enter the registration's channel ID: ")
        id_client = input("Enter your discord ID: ")
        config_data = {
            "TOKEN": token,
            "PREFIX": prefix,
            "LOG_ID": log_id,
            "REGISTRATION_ID": registration_id,
            "OWNER_ID": id_client,
            "DEL_TIME": 3
        }
        json.dump(config_data, config_file, indent=4)
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
else:
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)

token = config["TOKEN"]
prefix = config["PREFIX"]
log = config["LOG_ID"]
owner = config["OWNER_ID"]
time_del = config["DEL_TIME"]

activity = disnake.Activity(
    name="the GLM6's server",
    type=disnake.ActivityType.watching,
)

bot = commands.Bot(
    command_prefix=prefix,
    intents=disnake.Intents.all(),
    activity=activity,
    case_insensitive=True
)

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        nbot = bot.user.name
    else:
        nbot = bot.user.name + "#" + bot.user.discriminator

    response = requests.get(online_version)
    if response.status_code == 200:
        bot_repo_version = response.text.strip()
    else:
        bot_repo_version = "Unknown"
    with open('version.txt', 'r') as version_file:
        bot_version = version_file.read().strip()
    if bot_version != bot_repo_version:
        print('===============================================')
        print('🛑 ATTENTION')
        print('🛑 You are not using the latest version !')
        print('🛑 Please update the bot with "git fetch && git pull".')
    print('===============================================')    
    print(f"🔱 Your bot is ready !")
    print(f'🔱 Logged in as {nbot} | {bot.user.id}')
    print(f'🔱 Local version: {bot_version}')
    print(f'🔱 Online version: {bot_repo_version}')
    print(f"🔱 Disnake version: {disnake.__version__}")
    print(f"🔱 Running on {platform.system()} {platform.release()} {os.name}")
    print(f"🔱 Python version: {platform.python_version()}")
    print('===============================================')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog_name = filename[:-3]
        try:
            bot.load_extension(f'cogs.{cog_name}')
        except Exception as e:
            print(f"🌪️  Error when loading extension '{cog_name}':\n\n{e}")

bot.run(token)