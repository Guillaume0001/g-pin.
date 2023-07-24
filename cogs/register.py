import disnake
from disnake.ext import commands
import sqlite3

class registerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /register has been loaded') 

    @commands.slash_command(name='register', description='System registration.')
    async def register(self, inter, email: str, password: str):
        role_id = 1130975208061288450
        role = disnake.utils.get(inter.guild.roles, id=role_id)
        embed = disnake.Embed(
            title="Creating your account",
        )
        conn = sqlite3.connect('bdd.db')
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE client_id = " + str(inter.author.id))
            results = cur.fetchall()
        except Exception as e:
            embed.description = "An error occurred while communicating with the database, please contact an administrator as soon as possible: ```" + str(e) + "```"
            embed.colour = disnake.Colour.red()
            await inter.response.send_message(embed=embed, ephemeral=True)
        if results:
            try:
                if role in inter.author.roles:
                    embed.description = "You cannot register if you already are."
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    await inter.author.add_roles(role)
                    embed.description = "You are on the database but you don't have the role, now you have it!"
                    embed.colour = disnake.Colour.green()
                    await inter.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                embed.description = "An error occurred while verifying your information, please contact an administrator as soon as possible: ```" + str(e) + "```"
                embed.colour = disnake.Colour.red()
                await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                if role in inter.author.roles:
                    await inter.author.remove_roles(role)
                    embed.description = "You are not on the database but you have the role, now you are no longer on the database!"
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        cur.execute("INSERT INTO users(client_id, email, password) VALUES (?, ?, ?)", (str(inter.author.id), email, password))
                        conn.commit()
                        await inter.author.add_roles(role)
                        embed.description = "Your registration for the program is validated! Now you can order services and earn points!"
                        embed.colour = disnake.Colour.green()
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.description = "An error occurred while communicating with the database, please contact an administrator as soon as possible: ```" + str(e) + "```"
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                embed.description = "An error occurred while verifying your information, please contact an administrator as soon as possible: ```" + str(e) + "```"
                embed.colour = disnake.Colour.red()
                await inter.response.send_message(embed=embed, ephemeral=True)
        conn.close()

def setup(bot):
    bot.add_cog(registerCommand(bot))