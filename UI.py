from typing import Any
import discord
import lawbook

#region UI
# menu to select which crime the criminals comitted
class CriminalJudgementMenu(discord.ui.Select):
    def __init__(self, name:str):
        self.name = name
        # set possible
        num_crimes = 0
        optionz = []
        for crime in lawbook.Crime:
            num_crimes += 1
            optionz.append(discord.SelectOption(label=crime.name))

        super(CriminalJudgementMenu, self).__init__(
            placeholder=name,
            min_values=1,
            max_values=1,
            options=optionz
        )

    async def callback(self, interaction: discord.Interaction):
        lawbook.condemn_subject(lawbook.Criminal(self.name,self.values[0]))
        await interaction.response.send_message(f"You have convicted {self.name} ({self.values[0]})",ephemeral=lawbook.ephemeral)

class CriminalJudgementView(discord.ui.View):
    def __init__(self, convicts):
        super().__init__()
        for convict in convicts:
            self.add_item(CriminalJudgementMenu(convict))

# selection Menu, that lets you select convicts from a list of recognized names (Battletags)
class CriminalSelectMenu(discord.ui.Select):
    def __init__(self,names:list[str]):
        self.names = names
        self.additional_names:list[str] = []
        # set every name as a possible option
        optionz = []
        for name in names:
            optionz.append(discord.SelectOption(label=name))

        super(CriminalSelectMenu, self).__init__(
            placeholder="Select whom to convict",
            min_values=0,
            max_values=len(names),
            options=optionz
        )

        self.response = 0

    async def callback(self, interaction: discord.Interaction):
        for name in self.additional_names:
            self.values.append(name)
        if self.response == 0:
            self.response = interaction.response.send_message(content="select punishment!", view=CriminalJudgementView(self.values),ephemeral=lawbook.ephemeral)
            await self.response
        else:
            await self.response.edit_message(content="select punishment!", view=CriminalJudgementView(self.values))
    
class AddCriminalModal(discord.ui.Modal, title="Add Criminals Here c:"):

    def __init__(self, selectionMenu):
        self.selectionMenu = selectionMenu
        super().__init__()

    textbox = discord.ui.TextInput(placeholder="Add criminals here :)",required=False,label="TestLabel")
    
    async def on_submit(self, interaction: discord.Interaction):
        value=self.children[0].value
        print(value)
        self.selectionMenu.additional_names = value.split(" ")
        reply = "You have added "
        for name in self.selectionMenu.additional_names:
            reply += f"{name}, "
        await interaction.response.send_message(f"{reply[:len(reply)-2]}. Load conviction menu by updating the dropdown menu :D")

class AddCriminalButton(discord.ui.Button):
    def __init__(self,selectionMenu:CriminalJudgementMenu):
        self.selectionMenu=selectionMenu
        super(AddCriminalButton, self).__init__(
            label="click to add convicts :3"
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddCriminalModal(self.selectionMenu))

class CriminalSelectionView(discord.ui.View):
    def __init__(self, names):
        super().__init__()
        menu = CriminalSelectMenu(names)
        self.add_item(menu)
        self.add_item(AddCriminalButton(menu))
#endregion
