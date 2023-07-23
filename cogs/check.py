import disnake
from disnake.ext import commands
import json
import requests

class UpdateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /check a été chargé !')

    @commands.slash_command(name="check", description="Vérifier la version du robot")
    @commands.is_owner()
    async def check(self, inter):
        try:
            online_version_url = "https://raw.githubusercontent.com/Guillaume0001/g-pin./main/version.txt"
            response = requests.get(online_version_url)
            if response.status_code == 200:
                online_version = response.text.strip()
                local_version = self.get_local_version()  # Méthode pour obtenir la version locale

                embed = disnake.Embed(
                    title=f"Check of {self.bot.user.name}",
                    color=disnake.Color.random()
                )
                if online_version == local_version:
                    embed.description = "Le bot est à jour."
                else:
                    embed.description = "Une mise à jour est disponible."

                embed.add_field(name="Local Version", value=f"```{local_version}```", inline=True)
                embed.add_field(name="Online Version", value=f"```{online_version}```", inline=True)
                await inter.response.defer()
                await inter.send(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title=f"Erreur durant l'execution de la vérification",
                description=f"```{e}```",
                color=disnake.Color.red()
            )
            embed.set_footer(text=f'Command executed by {inter.author}', icon_url=inter.author.avatar.url)
            await inter.response.send_message(embed=embed)

    def get_local_version(self):
        with open("version.txt", "r") as version_file:
            local_version = version_file.read().strip()
        return local_version

def setup(bot):
    bot.add_cog(UpdateCommand(bot))