import disnake
from disnake.ext import commands
import json
import time
import requests
import sqlite3
import os
import datetime

class moneyExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 Money extension has been loaded !')

    @commands.slash_command(name="earn", description="Win money")
    async def check(self, inter):
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        current_time = int(time.time())
        cooldown_time = 60 * 60 * 2
        embed = disnake.Embed()
        embed.set_footer(
            text="© " + config["OWNER_NAME"] + " - " + config["PROJECT_NAME"],
            icon_url="https://cdn.discordapp.com/avatars/1132715398979141742/37077cb78bd9aed18926870d452447dd.webp?size=32",
        )
        conn = sqlite3.connect('bdd.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE client_id = ?", (str(inter.author.id),))
        result = cur.fetchall()
        if result:
            infos = result[0]
            actual_money = int(infos[6])
            last_earning_time = int(infos[7])

            letct = last_earning_time + cooldown_time
    
            if letct <= current_time:
                new_money = actual_money + 10
                try:
                    cur.execute("UPDATE users SET money = ? AND last_earn = ? WHERE client_id = ?", (new_money, current_time, inter.author.id))
                    conn.commit()
                    try:
                        embed.title = "Success"
                        embed.description = "You've earned 10 point ! If you wan't more point, buy a minor !"
                        embed.colour = disnake.Colour.green()
                        await inter.response.send_message(embed=embed, ephemeral=True) 
                    except Exception as e:
                        embed.title = "Error"
                        embed.description = "An error occurred while sending message."
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True) 
                except Exception as e:
                    embed.title = "Error"
                    embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
            else:
                remaining_time = cooldown_time - (current_time - last_earning_time)
                remaining_time_delta = datetime.timedelta(seconds=remaining_time)
                remaining_time_str = str(remaining_time_delta)
                embed.title = "Error"
                embed.description = "Hey, calm down ! Wait again " + remaining_time_str + " before earn money."
                embed.colour = disnake.Colour.red()
                await inter.response.send_message(embed=embed, ephemeral=True) 
        else:
            embed.title = "Error"
            embed.description = "You can't earn money if you haven't any account !"
            embed.colour = disnake.Colour.red()
            await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(moneyExtension(bot))