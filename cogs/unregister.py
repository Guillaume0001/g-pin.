import disnake
from disnake.ext import commands
import sqlite3

class unregisterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /unregister has been loaded') 

    @commands.slash_command(name='unregister', description="Supprimer votre compte au programme.")
    async def delwarn(self, inter):
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
            if result:
                if role in inter.author.roles:
                    try:
                        cur.execute("DELETE FROM users WHERE client_id = " + str(inter.author.id))
                        conn.commit()
                        await inter.author.remove_roles(role)
                        embed.description = "Tu as bien été désincrit du programme, GLM6 est déçu de te voir partir et te souhaite une bonne continuation !"
                        embed.colour = 0x00FF00
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.description = "Une erreur est survenue lors de la communication avec la base de donnée, veuillez contacter un administrateur au plus vite: ```" + str(e) + "```"
                        embed.colour = 0xFF0000
                        inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        cur.execute("DELETE FROM users WHERE client_id = " + str(inter.author.id))
                        conn.commit()
                        embed.description = "Tu es sur la base de donnée mais tu n'as pas le rôle, pas de soucis, tu ne fais plus parti de l'équipe..."
                        embed.colour = 0xFF0000
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.description = "Une erreur est survenue lors de la communication avec la base de donnée, veuillez contacter un administrateur au plus vite: ```" + str(e) + "```"
                        embed.colour = 0xFF0000
                        inter.response.send_message(embed=embed, ephemeral=True)
            else:
                if role in inter.author.roles:
                    await inter.author.remove_roles(role)
                    embed.description = "Tu n'es pas sur la base de donnée mais tu as rôle, pas de soucis, tu ne fais plus parti de l'équipe..."
                    embed.colour = 0xFF0000
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed.description = "Tu ne peux pas te désincrire si tu ne fais pas partie du programme."
                    embed.colour = 0xFF0000
                    await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed.description = "Une erreur est survenue lors de la vérification de votre compte, veuillez contacter un administrateur au plus vite: ```" + str(e) + "```"
            embed.colour = 0xFF0000
            await inter.response.send_message(embed=embed, ephemeral=True)
        conn.close()

def setup(bot):
    bot.add_cog(unregisterCommand(bot))