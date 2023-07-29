import disnake
from disnake.ext import commands
import sqlite3
import requests
import os
import json

class registerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 registration extension has been loaded') 
    @commands.slash_command(name='register', description='System registration.')
    async def registerCommand(self, inter, email: str, name: str, surname: str):
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)

        role_id = 1130975208061288450
        role = disnake.utils.get(inter.guild.roles, id=role_id)
        user_id = inter.author.id
        embed = disnake.Embed()
        embed.set_footer(
            text="©" + config["OWNER_NAME"] + " - " + config["PROJECT_NAME"],
            icon_url="https://cdn.discordapp.com/avatars/1132715398979141742/37077cb78bd9aed18926870d452447dd.webp?size=32",
        )
        conn = sqlite3.connect('bdd.db')
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE client_id = " + str(inter.author.id))
            results = cur.fetchall()
        except Exception as e:
            embed.title = "Error"
            embed.description = "An error occurred while communicating with the database, please contact an administrator as soon as possible: ```" + str(e) + "```"
            embed.colour = disnake.Colour.red()
            await inter.response.send_message(embed=embed, ephemeral=True)
        if results:
            try:
                if role in inter.author.roles:
                    embed.title = "Error"
                    embed.description = "You cannot register if you already are."
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    await inter.author.add_roles(role)
                    embed.title = "Error"
                    embed.description = "You are on the database but you don't have the role, now you have it!"
                    embed.colour = disnake.Colour.green()
                    await inter.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                embed.title = "Error"
                embed.description = "An error occurred while verifying your information, please contact an administrator as soon as possible: ```" + str(e) + "```"
                embed.colour = disnake.Colour.red()
                await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                if role in inter.author.roles:
                    await inter.author.remove_roles(role)
                    embed.title = "Error"
                    embed.description = "You are not on the database but you have the role, now you are no longer have the role!"
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed.title="User request: " + inter.author.display_name + " (a.k.a "+ inter.author.name + ")"
                    embed.description="User " + inter.author.display_name + " (a.k.a "+ inter.author.name + ") want to create an account for join the GLM6's program."
                    embed.color=disnake.Colour.green()

                    embed.add_field(
                      name="Name:",
                      value="``" + name + "``",
                      inline=True,  
                    )

                    embed.add_field(
                        name="Surname:",
                        value="``" + surname + "``",
                        inline=True,
                    )

                    embed.add_field(
                        name="Email:",
                        value="``" + email + "``",
                        inline=True,
                    )

                    try:
                        registration_channel = self.bot.get_channel(int(config["REGISTRATION_ID"]))
                        if registration_channel is not None:
                            try:
                                cur.execute("INSERT INTO requests(client_id, name, surname, email) VALUEs (?, ?, ?, ?)", (str(inter.author.id), name, surname, email))
                                conn.commit()
                                await registration_channel.send(embed=embed)
                                embed.title = "Success"
                                embed.description = "Your request have been correctly sent"
                                embed.color = disnake.Colour.green()
                                await inter.response.send_message(embed=embed, ephemeral=True)
                            except Exception as e:
                               await inter.response.send_message(content="An error occurred while sending your request: ```" + str(e) + "```.", ephemeral=True) 
                        else:
                            embed.title = "Error"
                            embed.description = "No room found"
                            embed.color = disnake.Colour.red()
                            await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        print(f"Une erreur s'est produite : {e}")
                        await inter.response.send_message(content="An error occurred while sending the message.", ephemeral=True)
            except Exception as e:
                embed.title = "Error"
                embed.description = "An error occurred while verifying your information, please contact an administrator as soon as possible: ```" + str(e) + "```"
                embed.colour = disnake.Colour.red()
                await inter.response.send_message(embed=embed, ephemeral=True)
        conn.close()


    @commands.slash_command(name="a_register", description="Admin Only; Accept or reject a request.")
    async def reponse(self, inter, user: disnake.User, status: int):
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)

        role_id = config["REGISTRATION_ID"]
        role = disnake.utils.get(inter.guild.roles, id=role_id)
        user_msg = self.bot.get_user(user.id)
        embed = disnake.Embed()
        embed.set_footer(
            text="©" + config["OWNER_NAME"] + " - " + config["PROJECT_NAME"],
            icon_url="https://cdn.discordapp.com/avatars/1132715398979141742/37077cb78bd9aed18926870d452447dd.webp?size=32",
        )
        conn = sqlite3.connect('bdd.db')
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM requests WHERE client_id = " + str(user.id))
            results = cur.fetchall()
        except Exception as e:
            embed.title = "Error"
            embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
            embed.colour = disnake.Colour.red()
            await inter.response.send_message(embed=embed, ephemeral=True)
        if not results:
            embed.title = "Error"
            embed.description = "This user haven't any request on the database."
            embed.colour = disnake.Colour.red()
            await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            if status == 1:
                cur.execute("SELECT * FROM requests WHERE client_id = ?", (int(user.id),))
                result = cur.fetchall()
                if result is None:
                    embed.title = "Error"
                    embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    if result:
                        infos = result[0]
                        name = infos[2]
                        surname = infos[3]
                        email = infos[4]
                
                    api_passwd = requests.get("https://api.motdepasse.xyz/create/?include_digits&include_lowercase&include_uppercase&include_special_characters&password_length=16&quantity=1")

                    passwd_data = api_passwd.json()
                    if api_passwd.status_code == 200:
                        passwd = passwd_data['passwords']
                    else:
                        embed.title = "Error"
                        embed.description = "An error occurred while communicating with motdepasse.xyz api."
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)        
                    try:
                        cur.execute("INSERT INTO users(client_id, name, surname, email, password) VALUES (?, ?, ?, ?, ?)", (str(user.id), str(name), str(surname), str(email), str(passwd)))
                        conn.commit()
                        try:
                            cur.execute("DELETE FROM requests WHERE client_id = ?", (str(user.id),))
                            conn.commit()
                        except Exception as e:
                            embed.title = "Error"
                            embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
                            embed.colour = disnake.Colour.red()
                            await inter.response.send_message(embed=embed, ephemeral=True)
                        try:
                            await inter.author.add_roles(role)
                            try:
                                embed.title = "Success"
                                embed.description = "The client account of" + user.display_name + " (a.k.a " + user.name + ") has been successfuly created !"
                                embed.colour = disnake.Colour.green()
                                await inter.response.send_message(embed=embed)
                            except Exception as e:
                                embed.title = "Error"
                                embed.description = "An error occurred when sending message: ```" + str(e) + "```"
                                embed.colour = disnake.Colour.red()
                                await inter.response.send_message(embed=embed, ephemeral=True)
                            try:
                                embed.title = "Your request has been accepted !"
                                embed.description = "Our staff has review your request and we've accepted your requets ! Now, you have access to a new category, you can earn point and buy product with your point."
                                embed.colour = disnake.Colour.green()
                                await user_msg.send(embed=embed)
                            except Exception as e:
                                embed.title = "Error"
                                embed.description = "An error occurred when sending message to the user: ```" + str(e) + "```"
                                embed.colour = disnake.Colour.red()
                                await inter.response.send_message(embed=embed, ephemeral=True)
                        except Exception as e:
                            embed.title = "Error"
                            embed.description = "An error occurred when adding role to the user: ```" + str(e) + "```"
                            embed.colour = disnake.Colour.red()
                            await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.title = "Error"
                        embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)
            else:
                try:
                    cur.execute("DELETE FROM requests WHERE client_id = ?", (str(user.id),))
                    conn.commit()
                    try:
                        embed.title = "Success"
                        embed.description = "The client account of" + user.display_name + " (a.k.a " + user.name + ") has been successfuly rejected !"
                        embed.colour = disnake.Colour.green()
                        await inter.response.send_message(embed=embed)
                    except Exception as e:
                        embed.title = "Error"
                        embed.description = "An error occurred when sending message: ```" + str(e) + "```"
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    try:
                        embed.title = "Your request has been rejected !"
                        embed.description = "Our staff has review your request and we've rejected your requets ! You can do an appeal if you think it's isn't normal."
                        embed.colour = disnake.Colour.red()
                        await user_msg.send(embed=embed)
                    except Exception as e:
                        embed.title = "Error"
                        embed.description = "An error occurred when sending message to the user: ```" + str(e) + "```"
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)
                except Exception as e:
                    embed.title = "Error"
                    embed.description = "An error occurred while communicating with the database: ```" + str(e) + "```"
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
            conn.close()
            
            

def setup(bot):
    bot.add_cog(registerCommands(bot))