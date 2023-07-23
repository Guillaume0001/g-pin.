import disnake
from disnake.ext import commands
import sqlite3

class registerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /register has been loaded') 

    @commands.slash_command(name='register', description='Inscription au système.')
    async def register(self, inter, email: str, password: str):
        role_id = 1130975208061288450
        role = disnake.utils.get(inter.guild.roles, id=role_id)
        embed = disnake.Embed(
            title="Inscription au programme",
        )
        conn = sqlite3.connect('bdd.db')
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE client_id = " + str(inter.author.id))
            result = cur.fetchall()
        except Exception as e:
            embed.description = "Une erreur est survenue lors de la communication avec la base de donnée, veuillez contacter un administrateur au plus vite: ```" + str(e) + "```"
            embed.colour = 0xFF0000
            await inter.response.send_message(embed=embed, ephemeral=True)
        if results:
            try:
                if role in inter.author.roles:
                    embed.description = "Tu ne peux pas t'inscrire si tu l'es déjà."
                    embed.colour = 0xFF0000
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    await inter.author.add_roles(role)
                    embed.description = "Tu es sur la base de donnée mais tu n'as pas le rôle, désormais, tu l'as !"
                    embed.colour = 0x00FF00
                    await inter.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                embed.description = "Une erreur est survenue lors de la vérification de vos informations, veuillez contacter un administrateur au plus vite: ```" + str(e) + "```"
                embed.colour = 0xFF0000
                await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                if role in inter.author.roles:
                    await inter.author.remove_roles(role)
                    embed.description = "Tu n'es pas sur la base de donnée mais tu as le rôle, désormais, tu n'es plus sur la base de donnée !"
                    embed.colour = 0xFF0000
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        cur.execute("INSERT INTO users(client_id, email, password) VALUES (?, ?, ?)", (str(inter.author.id), email, password))
                        conn.commit()
                        await inter.author.add_roles(role)
                        embed.description = "Ton inscription au programme est validé ! Tu peux désaprésent commander des services et gagner des points !"
                        embed.colour = 0x00FF00
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.description = "Une erreur est survenue lors de la communication avec la base de donnée, veuillez contacter un administrateur au plus vite: ```" + str(e) + "```"
                        embed.colour = 0xFF0000
                        await inter.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                embed.description = "Une erreur est survenue lors de la vérification de vos informations, veuillez contacter un administrateur au plus vite: ```" + str(e) + "```"
                embed.colour = 0xFF0000
                await inter.response.send_message(embed=embed, ephemeral=True)
        conn.close()

def setup(bot):
    bot.add_cog(registerCommand(bot))