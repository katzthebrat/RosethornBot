import discord
import logging

# Modal form
class ThornForm(discord.ui.Modal, title="Rosethorn | Member Form"):
    preferred_name = discord.ui.TextInput(label="Preferred Name", required=True, placeholder="e.g. Enchanted")
    gamertag = discord.ui.TextInput(label="Gamertag", required=True, placeholder="e.g. Enchanted547")
    birthdate = discord.ui.TextInput(label="Birthdate", required=True, placeholder="DD-MM-YYYY")

    def __init__(self, member: discord.Member):
        super().__init__()
        self.member = member

    async def on_submit(self, interaction: discord.Interaction):
        log_channel = interaction.client.get_channel(1311529665348767835)

        embed = discord.Embed(
            title="📥 Member Info Submitted",
            description=f"{self.member.mention} submitted info via Thorn DM.",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Preferred Name", value=self.preferred_name.value, inline=True)
        embed.add_field(name="Gamertag", value=self.gamertag.value, inline=True)
        embed.add_field(name="Birthdate", value=self.birthdate.value, inline=True)
        embed.set_footer(text="Rosethorn Bot | Awaiting admin review")
        embed.set_thumbnail(url=self.member.display_avatar.url)

        view = AdminReviewView(self.member, self.preferred_name.value, self.gamertag.value)

        await log_channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Your info has been sent to admins!", ephemeral=True)

# Admin review buttons
class AdminReviewView(discord.ui.View):
    def __init__(self, member, name, gamertag):
        super().__init__(timeout=None)
        self.member = member
        self.name = name
        self.gamertag = gamertag

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        required_role_id = 1308905911489921124
        approver = interaction.user
        guild = interaction.guild
        required_role = guild.get_role(required_role_id)

        if required_role not in approver.roles:
            await interaction.response.send_message(
                f"⚠️ You need the **{required_role.name}** role to approve submissions.",
                ephemeral=True
            )
            logging.warning(f"{approver} tried to approve without required role.")
            return

        new_name = f"{self.name} [{self.gamertag}]"
        try:
            await self.member.edit(nick=new_name)
            embed = interaction.message.embeds[0]
            embed.color = discord.Color.green()
            embed.set_footer(text="✅ Approved | Nickname Updated")
            await interaction.message.edit(content=f"✅ Approved by {approver.mention}", embed=embed, view=None)
            logging.info(f"Nickname updated for {self.member.name} to {new_name}")
        except Exception as e:
            logging.error(f"Failed to update nickname: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ Error updating nickname", ephemeral=True)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.red()
        embed.set_footer(text="❌ Denied | No changes made")
        await interaction.message.edit(content=f"❌ Denied by {interaction.user.mention}", embed=embed, view=None)
        logging.info(f"Form denied for {self.member.name}")

# DM button view
class ThornStarter(discord.ui.View):
    def __init__(self, member):
        super().__init__(timeout=None)
        self.member = member

    @discord.ui.button(label="Start Form", style=discord.ButtonStyle.primary)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ThornForm(self.member))

# Setup DM listener
async def setup_thorn(bot):
    @bot.event
    async def on_message(message):
        if message.guild or message.author == bot.user:
            return

        if message.content.strip().lower() == "thorn":
            logging.info(f"'Thorn' DM received from {message.author}")

            member = None
            for guild in bot.guilds:
                m = guild.get_member(message.author.id)
                if m:
                    member = m
                    break

            if member:
                view = ThornStarter(member)
                await message.author.send("📋 Click below to begin your Rosethorn onboarding:", view=view)
            else:
                await message.author.send("⚠️ You're not in a mutual server with Rosethorn. Please join the server first.")
