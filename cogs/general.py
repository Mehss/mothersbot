"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.5.0
"""

import platform
import random

import aiohttp
import discord
import gspread
import json
import re
import pandas as pd
import asyncio
import d20
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from constants import *
from database import Character


class FeedbackForm(discord.ui.Modal, title="Feeedback"):
    feedback = discord.ui.TextInput(
        label="What do you think about this bot?",
        style=discord.TextStyle.long,
        placeholder="Type your answer here...",
        required=True,
        max_length=256,
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.answer = str(self.feedback)
        self.stop()

class ConditionView(discord.ui.View):
    def __init__(self, user_id: int, server_id: int, char_name: str, name: str, effect: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.server_id = server_id
        self.char_name = char_name
        self.name = name
        self.effect = effect

    @discord.ui.button(label="Add Condition", custom_id="cond")
    async def condition_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Only the character's owner may add the condition to their character
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "Only the owner of this character can add this condition.", ephemeral=True
            )
            return

        added = await interaction.client.database.add_condition(
            self.user_id, self.server_id, self.name, self.effect
        )
        if not added:
            await interaction.response.send_message(
                "This character no longer exists.", ephemeral=True
            )
            return

        button.disabled = True
        button.label = "Condition added"
        await interaction.response.edit_message(view=self)
        embed = discord.Embed(
            description=f"{self.char_name} gains the condition **{self.name}**.\n{self.effect}",
            color=0xBEBEFE,
        )
        await interaction.followup.send(embed=embed)
        self.stop()


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0xBEBEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Used [Krypton's](https://krypton.ninja) template",
            color=0xBEBEFE,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="Krypton#7331", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.bot_prefix} for normal commands",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        num_roles = len(roles)
        if num_roles > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying [50/{num_roles}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=0xBEBEFE
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="check",
        description="Make a check.",
    )
    @app_commands.describe(
        attribute="The attribute to check.",
        skill="The skill to check.",
        adv="Roll with advantage [+] or disadvantage [-].",
        mod="Add mod to your roll"
    )
    @app_commands.choices(
        attribute=[app_commands.Choice(name=a, value=a) for a in K_ATTRIBUTES],
        adv=[
            app_commands.Choice(name="Advantage [+]", value="adv"),
            app_commands.Choice(name="Disadvantage [-]", value="dis"),
        ],
    )
    async def check(
        self,
        context: Context,
        attribute: str,
        skill: str | None = None,
        adv: str | None = None,
        mod: str | None= None,
    ) -> None:
        # Prefix commands and typed-over autocomplete bypass the slash options, so validate here
        if attribute not in K_ATTRIBUTES:
            embed = discord.Embed(
                description=f"Unknown attribute `{attribute}`. Choose one of: {', '.join(K_ATTRIBUTES)}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        if skill is not None and skill not in K_SKILLS:
            embed = discord.Embed(
                description=f"Unknown skill `{skill}`.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        if adv is not None and adv not in ("adv", "dis"):
            embed = discord.Embed(
                description=f"Unknown option `{adv}`. Use `adv` or `dis`.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        if context.guild is None:
            embed = discord.Embed(
                description="This command can only be used in a server.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        char = await self.bot.database.get_character(context.author.id, context.guild.id)
        if char is None:
            embed = discord.Embed(
                description="You don't have a character yet, use `add` with your sheet link first.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        target_number = int(char['attr'][attribute]['value'])
        # The sheet marks known skills with a checkbox, which comes through as "TRUE"
        has_skill = skill is not None and str(char['skills'].get(skill)).upper() == "TRUE"
        if has_skill:
            if skill in K_TRAINED_SKILLS:
                target_number += 10
            elif skill in K_EXPERT_SKILLS:
                target_number += 15
            elif skill in K_MASTER_SKILLS:
                target_number += 20

        roll_string='1d100-1'
        if mod:
            roll_string += mod
        # Advantage/disadvantage rolls twice and keeps the better/worse outcome
        rolls = [d20.roll('1d100-1') for _ in range(2 if adv else 1)]

        def outcome(roll: d20.RollResult) -> tuple[int, int]:
            # Rank: critical failure < failure < success < critical success,
            # ties broken towards the lower roll
            success = roll.total < target_number
            crit = roll.total % 11 == 0
            rank = (2 if success else 1) + (1 if crit and success else -1 if crit else 0)
            return rank, -roll.total

        if adv == "dis":
            roll = min(rolls, key=outcome)
        else:
            roll = max(rolls, key=outcome)
        crit = roll.total % 11 == 0
        # mod_roll = d20.roll('d0')
        if mod:
            mod_roll = d20.roll(mod)
            success = roll.total + mod_roll.total < target_number
        else:
            success = roll.total < target_number

        result = "Success" if success else "Failure"
        if crit:
            result = f"Critical {result}"
        if adv:
            roll_line = f"Rolls ({'[+]' if adv == 'adv' else '[-]'}): " + ", ".join(
                f"**{r.total}**" if r is roll else r.total for r in rolls
            )
        else:
            if mod:
                roll_line = f"Roll: {roll.total} + {mod_roll.total}"
            else: roll_line = f"Roll: {roll.total}"
        attribute_value = int(char['attr'][attribute]['value'])
        attribute_line = f"{attribute}: {attribute_value}"
        if has_skill:
            attribute_line += f" + {target_number - attribute_value} ({skill}) = {target_number}"
        elif skill:
            attribute_line += f" (no {skill} skill)"

        embed = discord.Embed(
            description=(
                f"## {char['info']['name']} makes a {attribute} check!\n"
                f"# {result}\n"
                f"{roll_line}\n"
                f"{attribute_line}"
            ),
            color=0x57F287 if success else 0xE02B2B,
        )
        await context.send(embed=embed)
        # A Critical Failure forces a Panic Check
        if crit and not success:
            await self.handle_panic(context, char)

    @check.autocomplete("skill")
    async def skill_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        # Discord allows at most 25 choices, and there are more skills than that, so autocomplete instead
        return [
            app_commands.Choice(name=skill, value=skill)
            for skill in K_SKILLS
            if current.lower() in skill.lower()
        ][:25]

    @staticmethod
    def roll_panic(stress: int) -> tuple[d20.RollResult, list[tuple[d20.RollResult, str, str]]]:
        """
        Makes a Panic Check: roll 1d20, and if it is not greater than the current Stress,
        the character panics and that roll is looked up on the panic table.
        Compounding Problems rolls twice more on the table, so there can be more than one effect.

        :param stress: The character's current Stress.
        :return: The check roll, and a list of (roll, name, effect) for every effect (empty if no panic).
        """
        check_roll = d20.roll('1d20')
        if check_roll.total > stress:
            return check_roll, []

        results = []
        roll = check_roll
        pending = 0
        while True:
            name, effect = K_PANIC_EFFECT[roll.total]
            results.append((roll, name, effect))
            if name == 'Compounding Problems':
                pending += 2
            if not pending:
                break
            pending -= 1
            roll = d20.roll('1d20')
        return check_roll, results

    @commands.hybrid_command(
        name="panic",
        description="Make a Panic Check against your Stress.",
    )
    async def panic(self, context: Context) -> None:
        """
        Makes a Panic Check against the character's Stress and shows any panic effects.

        :param context: The hybrid command context.
        """
        if context.guild is None:
            embed = discord.Embed(
                description="This command can only be used in a server.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        char = await self.bot.database.get_character(context.author.id, context.guild.id)
        if char is None:
            embed = discord.Embed(
                description="You don't have a character yet, use `add` with your sheet link first.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        await self.handle_panic(context, char)

    @commands.hybrid_command(
        name="conditions",
        description="List all conditions of your character.",
    )
    async def conditions(self, context: Context) -> None:
        """
        Lists all conditions of the character with their effects.

        :param context: The hybrid command context.
        """
        if context.guild is None:
            embed = discord.Embed(
                description="This command can only be used in a server.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        char = await self.bot.database.get_character(context.author.id, context.guild.id)
        if char is None:
            embed = discord.Embed(
                description="You don't have a character yet, use `add` with your sheet link first.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        embed = discord.Embed(
            title=f"{char['info']['name']}'s conditions", color=0xBEBEFE
        )
        if not char['conditions']:
            embed.description = "No conditions."
        # Discord allows at most 25 fields per embed
        for name, effect in list(char['conditions'].items())[:25]:
            embed.add_field(name=name, value=effect, inline=False)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="removecondition",
        description="Remove a condition from your character.",
    )
    @app_commands.describe(
        name="The condition to remove",
    )
    async def removecondition(self, context: Context, name: str) -> None:
        """
        Removes a condition from the character.

        :param context: The hybrid command context.
        :param name: The name of the condition to remove.
        """
        if context.guild is None:
            embed = discord.Embed(
                description="This command can only be used in a server.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        char = await self.bot.database.get_character(context.author.id, context.guild.id)
        if char is None:
            embed = discord.Embed(
                description="You don't have a character yet, use `add` with your sheet link first.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        if name not in char['conditions']:
            embed = discord.Embed(
                description=f"{char['info']['name']} doesn't have the condition **{name}**.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        await self.bot.database.remove_condition(context.author.id, context.guild.id, name)
        embed = discord.Embed(
            description=f"{char['info']['name']} is no longer affected by **{name}**.",
            color=0x57F287,
        )
        await context.send(embed=embed)

    @removecondition.autocomplete("name")
    async def condition_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        # Suggest only the conditions the character currently has
        if interaction.guild is None:
            return []
        char = await self.bot.database.get_character(interaction.user.id, interaction.guild.id)
        if char is None:
            return []
        return [
            app_commands.Choice(name=condition, value=condition)
            for condition in char['conditions']
            if current.lower() in condition.lower()
        ][:25]

    @commands.hybrid_command(
        name="wound",
        description="Roll on the Wounds table.",
    )
    @app_commands.describe(
        wound_type="The type of wound.",
    )
    @app_commands.choices(
        wound_type=[app_commands.Choice(name=t, value=t) for t in K_WOUND_TYPES],
    )
    async def wound(self, context: Context, wound_type: str) -> None:
        """
        Rolls 1d10 on the Wounds table for the given wound type and offers to add it as a condition.

        :param context: The hybrid command context.
        :param wound_type: The type of wound, one of K_WOUND_TYPES.
        """
        # Prefix commands bypass the slash choices, so validate here
        if wound_type not in K_WOUNDS:
            embed = discord.Embed(
                description=f"Unknown wound type `{wound_type}`. Choose one of: {', '.join(K_WOUND_TYPES)}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        if context.guild is None:
            embed = discord.Embed(
                description="This command can only be used in a server.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        char = await self.bot.database.get_character(context.author.id, context.guild.id)
        if char is None:
            embed = discord.Embed(
                description="You don't have a character yet, use `add` with your sheet link first.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        # The table is numbered 0-9
        roll = d20.roll('1d10-1')
        severity = K_WOUND_SEVERITY[roll.total]
        effect = K_WOUNDS[wound_type][roll.total]
        embed = discord.Embed(
            description=(
                f"{char['info']['name']} takes a {wound_type} wound!\n"
                f"Roll: {roll.result}\n"
                f"# {severity}"
            ),
            color=0xE02B2B,
        )
        embed.add_field(name=f"{roll.total}. {wound_type.upper()}", value=effect, inline=False)
        # Name the condition after the wound's first sentence, e.g. "Gunshot: Broken rib"
        name = f"{wound_type}: {effect.split('.')[0]}"
        view = ConditionView(
            int(char['user_id']), int(char['server_id']), char['info']['name'], name, effect
        )
        await context.send(embed=embed, view=view)

    @commands.hybrid_command(
        name="rollchar",
        description="Roll on the Wounds table.",
    )
    @app_commands.describe(
        charname="name of your character",
    )
    async def rollchar(self, context: Context, charname: str) -> None:
        """
        roll for stats
        """
        # Prefix commands bypass the slash choices, so validate here
        
        # The table is numbered 0-9
        embed = discord.Embed(
            description=(
                f"## Mothership Character Roll for {charname}\n"
                f"# Stat\n"
                f"{d20.roll('2d10+25').result}\n"
                f"{d20.roll('2d10+25').result}\n"
                f"{d20.roll('2d10+25').result}\n"
                f"{d20.roll('2d10+25').result}\n"
                f"*Assign these to your character Stat.*\n"
                f"# Save\n"
                f"{d20.roll('2d10+10').result}\n"
                f"{d20.roll('2d10+10').result}\n"
                f"{d20.roll('2d10+10').result}\n"
                f"*Assign these to your character Saves.*\n"
                f"# Max HP\n"
                f"{d20.roll('1d10+10').result}\n\n"
                f"__Don't forget to add your class bonus__"
            ),
            color=0xE02B2B,
        )
        await context.send(embed=embed)

    async def handle_panic(self, context: Context, char: Character) -> None:
        """
        Makes a Panic Check for the character and sends the result, one message per panic effect.

        :param context: The hybrid command context to send the result to.
        :param char: The character, as returned by get_character.
        """
        stress = int(char['attr']['Stress']['value'])
        check_roll, effects = self.roll_panic(stress)
        header = (
            f"{char['info']['name']} makes a Panic Check!\n"
            f"Roll: {check_roll.result} vs Stress {stress}\n"
        )
        if not effects:
            embed = discord.Embed(
                description=f"{header}# Keeps it together",
                color=0x57F287,
            )
            await context.send(embed=embed)
            return

        for roll, name, effect in effects:
            embed = discord.Embed(description=f"{header}# Panic!", color=0xE02B2B)
            embed.add_field(
                name=f"{roll.total}. {name.upper()}",
                value=effect,
                inline=False,
            )
            view = ConditionView(
                int(char['user_id']), int(char['server_id']), char['info']['name'], name, effect
            )
            await context.send(embed=embed, view=view)

    @staticmethod
    def get_df(spreadsheet_id: str, sheet_name: str):
        creds = None
        with open("credentials.json") as f:
            creds = json.load(f)
        gc = gspread.service_account_from_dict(creds)
        sheet = gc.open_by_key(spreadsheet_id)
        worksheet = sheet.worksheet(sheet_name)

        data = worksheet.get_all_records()
        return pd.DataFrame(data)

    @staticmethod
    def get_spreadsheet_id(url: str):
        # Regular expression to match the spreadsheet ID in the URL
        pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
        match = re.search(pattern, url)

        # Check if a match was found
        if match:
            return match.group(1)
        else:
            return ""

    async def fetch_and_save_character(self, context: Context, link: str) -> None:
        """
        Fetches the character data from the Google Sheet and saves it to the database.

        :param context: The hybrid command context.
        :param link: The link to the character's Google Sheet.
        """
        spreadsheet_id = self.get_spreadsheet_id(link)
        attr_df = await asyncio.to_thread(self.get_df, spreadsheet_id, 'attr')
        skills_df = await asyncio.to_thread(self.get_df, spreadsheet_id, 'skills')
        info_df = await asyncio.to_thread(self.get_df, spreadsheet_id, 'info')
        # attr: {attribute: {"value": value, "minmax": minmax}}
        attr = attr_df.set_index('attribute')[['value', 'minmax']].to_dict(orient='index')
        skills = skills_df.set_index('attribute')['value'].to_dict()
        info = info_df.set_index('attribute')['value'].to_dict()

        await self.bot.database.set_character(
            user_id=context.author.id,
            server_id=context.guild.id,
            gsheet_link=link,
            attr=attr,
            skills=skills,
            info=info,
        )
        embed = discord.Embed(
            title="**Character saved**",
            description=f"Loaded {len(attr)} attributes, {len(skills)} skills and {len(info)} other categories from the sheet.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="add",
        description="add a gsheet data",
    )
    @app_commands.describe(
        link="Sheet link",
    )
    async def add(
        self,
        context: Context,
        link: str,
    ) -> None:
        """
        Loads a character from a Google Sheet and saves it.

        :param context: The hybrid command context.
        :param link: The link to the character's Google Sheet.
        """
        if context.guild is None:
            embed = discord.Embed(
                description="This command can only be used in a server.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        await context.defer()
        await self.fetch_and_save_character(context, link)

    @commands.hybrid_command(
        name="update",
        description="update a gsheet data",
    )
    async def update(
        self,
        context: Context,
    ) -> None:
        """
        Re-fetches the character from its saved Google Sheet link.

        :param context: The hybrid command context.
        """
        if context.guild is None:
            embed = discord.Embed(
                description="This command can only be used in a server.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        char = await self.bot.database.get_character(context.author.id, context.guild.id)
        if char is None or not char["gsheet_link"]:
            embed = discord.Embed(
                description="You don't have a character yet, use `add` with your sheet link first.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        await context.defer()
        await self.fetch_and_save_character(context, char["gsheet_link"])


async def setup(bot) -> None:
    await bot.add_cog(General(bot))
