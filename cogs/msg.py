import disnake
from disnake.ext import commands
import os
import json

class FonctionnementCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /admin_msg a été chargé !')

    @commands.slash_command(name="a_msg", description="Admin Only; Send a message")
    @commands.has_permissions(manage_messages=True)
    async def admin_fonctionnement(self, inter, msg: int):
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        embed =  disnake.Embed()
        title = "Fonctionnement de GLM6 - Private IPv6 Network"
        color = disnake.Colour.random()
        if msg == 1:
            embed.title = title
            embed.description = "Pour accéder au différent service de GLM, il faut vous inscrire au service.\n \n Utiliser la commande /register pour vous inscrire au prorgamme, vous aurez en suite une suite de salon qui apparaîtra et celui-ci disparaîtra. Vous devrez suivre ces différents salons."
            embed.color = color
        else:
            embed.title = "Error !"
            embed.description = "The ID of the message isn't correct !"
            embed.color = disnake.Colour.red()
        
        embed.set_footer(
            text="©" + config["OWNER_NAME"] + " - " + config["PROJECT_NAME"],
            icon_url="https://cdn.discordapp.com/avatars/1132715398979141742/37077cb78bd9aed18926870d452447dd.webp?size=32",
        )
        await inter.channel.send(embed=embed)
        await inter.response.send_message(content="Le message n°" + str(msg) + " a bien été envoyé !", ephemeral=True)

def setup(bot):
    bot.add_cog(FonctionnementCommand(bot))
