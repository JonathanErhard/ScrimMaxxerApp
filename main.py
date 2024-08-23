import discord
from discord import app_commands

import UI

import lawbook

import re

#region main Client setup
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(
            self,
            allowed_contexts=app_commands.AppCommandContext(private_channel=True),
            allowed_installs=app_commands.AppInstallationType(user=True),
        )
    async def setup_hook(self):
        await self.tree.sync()

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
#endregion

#region commands
@client.tree.command()
@app_commands.describe(
    criminals='List of Criminals seperated by an empty space'
)
#bans list of players. Input is a 
async def ban(interaction: discord.Interaction, criminals: str):
    names=criminals.split(" ")
    await interaction.response.send_message("Choose punishment!", view=UI.CriminalJudgementView(convicts=names),ephemeral=lawbook.ephemeral)
#endregion

#region context menues
@client.tree.context_menu(name='Analyse')
async def analyse(interaction: discord.Interaction, message: discord.Message):
    text = message.content
    dict = lawbook.read_dic()
    convicts = list(dict.keys())
    found = False
    message = "Message contained:"
    for convict in convicts:
        if text.__contains__(convict):
            found = True
            message += f"\n\t{convict}: {dict[convict]}"
    if not found:
        message = "Nothing found :) save to scrim!"
    await interaction.response.send_message(message,ephemeral=lawbook.ephemeral)

@client.tree.context_menu(name='Ban') #TODO
async def ban(interaction: discord.Interaction, message: discord.Message):
    battletags = list[str](re.findall(r"[^[\s:,;()-]+#[0-9]+",message.content)) 
    await interaction.response.send_message("Choose convicts!", view=UI.CriminalSelectionView(names=battletags), ephemeral=lawbook.ephemeral)
#endregion

#run client
client.run('TOKEN') #enter bot token here