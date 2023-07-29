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
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        embed.set_footer(
            text="©" + config["OWNER_NAME"] + " - " + config["PROJECT_NAME"],
            icon_url="https://cdn.discordapp.com/avatars/1132715398979141742/37077cb78bd9aed18926870d452447dd.webp?size=32",
        )
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
        conn.close()
    
    @commands.slash_command(name="a_warn", description="Admin Only; Warn a user.")
    async def warn(self, inter, user: disnake.User, reason: str):
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        embed = disnake.Embed()
        embed.set_footer(
            text="©" + config["OWNER_NAME"] + " - " + config["PROJECT_NAME"],
            icon_url="https://cdn.discordapp.com/avatars/1132715398979141742/37077cb78bd9aed18926870d452447dd.webp?size=32",
        )
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
            cur.execute("INSERT INTO moderation(user, reason, type, date, secret) VALUES (?, ?, ?, ?, ?)", (str(user.id), str(reason), str("WARN"), str(today), str(secret)))
            conn.commit()
            try:
                embed.title = "Oh Oh"
                embed.description = "You have been warned by moderator ! For the reason following: ``" + str(reason) + "``."
                embed.colour = disnake.Colour.red()
                await user_msg.send(embed=embed)
                try:
                    embed.title = "Success"
                    embed.description = "User: " + user.display_name + " (a.k.a " + user.name + ") has been succesfuly warned !"
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
                except Exception as e:
                    embed.title = "Error"
                    embed.description = "An error occurred while sending your message."
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
        conn.close()

    @commands.slash_command(name="a_unwarn", description="Admin Only; Delete a warn from a user.")
    async def unwarn(self, inter, user: disnake.User, id: int):
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        embed = disnake.Embed()
        embed.set_footer(
            text="©" + config["OWNER_NAME"] + " - " + config["PROJECT_NAME"],
            icon_url="https://cdn.discordapp.com/avatars/1132715398979141742/37077cb78bd9aed18926870d452447dd.webp?size=32",
        )
        conn = sqlite3.connect('bdd.db')
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM moderation WHERE user = ?", (str(user.id),))
            result = cur.fetchall()
            if not result:
                embed.title = "Error"
                embed.description = "This user haven't any warning."
                embed.colour = disnake.Colour.red()
                await inter.response.send_message(embed=embed, ephemeral=True) 
            else:
                try:
                    cur.execute("SELECT * FROM moderation WHERE user = ? AND id = ?", (str(user.id), int(id)))
                    result = cur.fetchall()
                    if not result:
                        embed.title = "Error"
                        embed.description = "This user haven't any warn with ID: ``" + id + "``."
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    else:
                        try:
                            cur.execute("DELETE FROM moderation WHERE user = ? AND id = ?", (str(user.id), int(id)))
                            conn.commit()
                            try:
                                embed.title = "Success"
                                embed.description = "User: " + user.display_name + " (a.k.a " + user.name + ") has been succesfuly unwarned !"
                                embed.colour = disnake.Colour.green()
                                await inter.response.send_message(embed=embed, ephemeral=True)
                            except Exception as e:
                                embed.title = "Error"
                                embed.description = "An error occurred while sending your message."
                                embed.colour = disnake.Colour.red()
                                await inter.response.send_message(embed=embed, ephemeral=True)
                        except Exception as e:
                            embed.title = "Error"
                            embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
                            embed.colour = disnake.Colour.red()
                            await inter.response.send_message(embed=embed, ephemeral=True)
                except Exception as e:
                    embed.title = "Error"
                    embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
           embed.title = "Error"
           embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
           embed.colour = disnake.Colour.red()
           await inter.response.send_message(embed=embed, ephemeral=True)
        conn.close()

    @commands.slash_command(name="a_kick", description="Admin_only; Kick a user of the guild.")
    async def kick(self, inter, user: disnake.User, reason: str):
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        embed = disnake.Embed()
        embed.set_footer(
            text="©" + config["OWNER_NAME"] + " - " + config["PROJECT_NAME"],
            icon_url="https://cdn.discordapp.com/avatars/1132715398979141742/37077cb78bd9aed18926870d452447dd.webp?size=32",
        )
        conn = sqlite3.connect('bdd.db')
        cur = conn.cursor()
        user_msg = self.bot.get_user(user.id)
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
            cur.execute("INSERT INTO moderation(user, reason, type, date, secret) VALUES (?, ?, ?, ?, ?)", (str(user.id), str(reason), str("KICK"), str(today), str(secret)))
            conn.commit()
            try:
                embed.title = "Oh Oh"
                embed.description = "You were kicked from GLM6 - Private IPv6 Network ! You can join the server with the folowing address: **https://discord.glm6.fr/** .\n\nKings regards."
                embed.colour = disnake.Colour.red()
                await user_msg.send(embed=embed)
                try:
                    await inter.guild.kick(user, reason=reason)
                    try:
                        embed.title = "Success"
                        embed.description = "User: " + user.display_name + " (a.k.a " + user.name + ") has been succesfuly kicked !"
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.title = "Error"
                        embed.description = "An error occurred while sending your message."
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True) 
                except Exception as e:
                    embed.title = "Error"
                    embed.description = "An error occurred while kicking user."
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
        conn.close()

def setup(bot):
    bot.add_cog(moderationCommands(bot))