import discord
from discord import app_commands
from discord.ext import commands
import asyncio

STAFF_ROLE_ID = 1308905911489921124
STAFF_LOG_CHANNEL_ID = 1320540890141556746

# ─── Admin Modal ───
class AdminApplicationModal(discord.ui.Modal, title="Admin Application"):
    def __init__(self, thread):
        super().__init__(timeout=None)
        self.thread = thread

        self.add_item(discord.ui.TextInput(label="What responsibilities interest you?", style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label="Do you have experience with moderation or leadership?", style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label="How would you handle conflict between members?", style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label="When are you most active?", style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Why do you want to help lead this community?", style=discord.TextStyle.paragraph))

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📝 Admin Application Submitted",
            description=f"{interaction.user.mention} has completed their application.",
            color=0x5865f2
        )
        for field in self.children:
            embed.add_field(name=field.label, value=field.value, inline=False)
        embed.set_footer(text="Rosethorn Bot | Admin Form")

        await self.thread.send(content=f"<@&{STAFF_ROLE_ID}>", embed=embed, view=ReviewPanel(interaction.user, self.thread, "Admin"))

        staff_channel = interaction.client.get_channel(STAFF_LOG_CHANNEL_ID)
        if staff_channel:
            await staff_channel.send(f"📣 New Admin application from {interaction.user.mention} in {self.thread.mention}")

        await interaction.response.send_message("✅ Your admin application was posted!", ephemeral=True)

# ─── Realm Modal ───
class RealmJobApplicationModal(discord.ui.Modal, title="Realm Job Application"):
    def __init__(self, thread):
        super().__init__(timeout=None)
        self.thread = thread

        self.add_item(discord.ui.TextInput(label="Which realm job interests you most?", style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Tell us about your creative experience or skills.", style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label="Do you have any specific ideas you'd bring?", style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label="How do you prefer to collaborate?", style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label="What about Rosethorn inspires you?", style=discord.TextStyle.paragraph))

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📦 Realm Job Application Submitted",
            description=f"{interaction.user.mention} has submitted their creative application.",
            color=0x2f3136
        )
        for field in self.children:
            embed.add_field(name=field.label, value=field.value, inline=False)
        embed.set_footer(text="Rosethorn Bot | Realm Form")

        await self.thread.send(content=f"<@&{STAFF_ROLE_ID}>", embed=embed, view=ReviewPanel(interaction.user, self.thread, "Realm Job"))

        staff_channel = interaction.client.get_channel(STAFF_LOG_CHANNEL_ID)
        if staff_channel:
            await staff_channel.send(f"✨ New Realm Job application from {interaction.user.mention} in {self.thread.mention}")

        await interaction.response.send_message("✅ Your realm job application was posted!", ephemeral=True)

# ─── Review Panel ───
class ReviewPanel(discord.ui.View):
    def __init__(self, applicant, thread, role_name):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.thread = thread
        self.role_name = role_name

    @discord.ui.button(label="✅ Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.applicant.send(f"✅ Your application for **{self.role_name}** was approved! Welcome aboard.")
        except:
            print(f"[Rosethorn] Could not DM {self.applicant}")

        staff_channel = interaction.client.get_channel(STAFF_LOG_CHANNEL_ID)
        if staff_channel:
            await staff_channel.send(f"✅ {self.applicant.mention}'s {self.role_name} application was **approved** by {interaction.user} in {self.thread.mention}")

        await interaction.response.send_message("✅ Approved.", ephemeral=True)
        await asyncio.sleep(10)
        await self.thread.delete()

    @discord.ui.button(label="❌ Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DenialReasonModal(self.applicant, self.thread, self.role_name, interaction.user))

# ─── Denial Modal ───
class DenialReasonModal(discord.ui.Modal, title="Denial Reason"):
    def __init__(self, applicant, thread, role_name, reviewer):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.thread = thread
        self.role_name = role_name
        self.reviewer = reviewer

        self.add_item(discord.ui.TextInput(label="Why was this application denied?", style=discord.TextStyle.paragraph))

    async def on_submit(self, interaction: discord.Interaction):
        reason = self.children[0].value

        try:
            await self.applicant.send(f"❌ Your application for **{self.role_name}** was denied.\n\n**Reason:** {reason}")
        except:
            print(f"[Rosethorn] Could not DM {self.applicant}")

        staff_channel = interaction.client.get_channel(STAFF_LOG_CHANNEL_ID)
        if staff_channel:
            await staff_channel.send(f"❌ {self.applicant.mention}'s {self.role_name} application was **denied** by {self.reviewer} in {self.thread.mention}\n**Reason:** {reason}")

        await interaction.response.send_message("❌ Denied.", ephemeral=True)
        await asyncio.sleep(10)
        await self.thread.delete()

# ─── Application Selector ───
class ApplicationTypeView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

    @discord.ui.select(
        placeholder="Choose your application type",
        options=[
            discord.SelectOption(label="Admin", description="Moderation, leadership, systems"),
            discord.SelectOption(label="Realm Job", description="Roleplay, creativity, community support")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.defer(ephemeral=True)

        thread = await interaction.channel.create_thread(
            name=f"{self.member.name} – {select.values[0]} Application",
            type=discord.ChannelType.public_thread
        )

        if select.values[0] == "Admin":
            await interaction.followup.send_modal(AdminApplicationModal(thread))
        else:
            await interaction.followup.send_modal(RealmJobApplicationModal(thread))

# ─── Slash Command ───
class ApplicationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="apply", description="Start a Rosethorn staff application")
    async def apply(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌸 Apply to Join Rosethorn Staff",
            description="Choose which role you're applying for:",
            color=discord.Color.from_rgb(113, 20, 23)
        )
        await interaction.response.send_message(embed=embed, view=ApplicationTypeView(interaction.user), ephemeral=True)

async def setup(bot):
    await bot.add_cog(ApplicationCog(bot))
