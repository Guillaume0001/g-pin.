import disnake
from disnake.ext import commands
import sqlite3
from datetime import date
import requests
import os
import json

#today = date.today()
#print("Today's date:", today)

class moderationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 moderation extension has been loaded') 

    @commands.slash_command(name="a_ban", description="Admin Only; Ban a member")
    async def ban(self, inter, user: disnake.User, reason: str):
        embed = disnake.Embed()
        conn = sqlite3.connect('bdd.db')
        user_msg = self.bot.get_user(user.id)
        cur = conn.cursor()
        today = date.today()
        request = requests.get("https://api.motdepasse.xyz/create/?include_digits&include_lowercase&include_uppercase&password_length=8&quantity=1")

        result = request.json()
        if request.status_code == 200:
            secret = result['passwords']
        else:
            embed.title = "Error"
            embed.description = "An error occurred while communicating with motdepasse.xyz api."
            embed.colour = disnake.Colour.red()
            await inter.response.send_message(embed=embed, ephemeral=True) 
        try:
            cur.execute("INSERT INTO moderation(user, reason, type, date, secret) VALUES (?, ?, ?, ?, ?)", (str(user.id), str(reason), str("BAN"), str(today), str(secret)))
            conn.commit()
            try:
                embed.title = "Oh Oh"
                embed.description = "You were banned from GLM6 - Private IPv6 Network ! You can do an appeal by contacting owner: ``guillaume0001``.\n\nKings regards."
                embed.colour = disnake.Colour.red()
                await user_msg.send(embed=embed)
                try:
                    await inter.guild.ban(user, reason=reason)
                    try:
                        embed.title = "Success"
                        embed.description = "User: " + user.display_name + " (a.k.a " + user.name + ") has been succesfuly banned !"
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.title = "Error"
                        embed.description = "An error occurred while sending your message."
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True) 
                except Exception as e:
                    embed.title = "Error"
                    embed.description = "An error occurred while banning user."
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True) 
            except Exception as e:
                embed.title = "Error"
                embed.description = "An error occurred while sending the message to the user."
                embed.colour = disnake.Colour.red()
                await inter.response.send_message(embed=embed, ephemeral=True) 
        except Exception as e:
            embed.title = "Error"
            embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
            embed.colour = disnake.Colour.red()
            await inter.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(moderationCommands(bot))