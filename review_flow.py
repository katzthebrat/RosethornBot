import discord
import asyncio
from discord.ext import commands
from discord import app_commands

STAFF_ROLE_ID = 1308905911489921124
STAFF_LOG_CHANNEL_ID = 1364281652150272201
ADMIN_ROLE_ID = 1320538700656148541
REALM_JOB_ROLE_ID = 1394853894437343422

class DenialReasonModal(discord.ui.Modal, title="Denial Reason"):
    def __init__(self, applicant: discord.Member, thread: discord.Thread):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.thread = thread

        self.add_item(discord.ui.TextInput(
            label="Why is this application being denied?",
            placeholder="Lack of experience, missing details, inactive...",
            style=discord.TextStyle.paragraph
        ))

    async def on_submit(self, interaction: discord.Interaction):
        reason = self.children[0].value

        # DM applicant
        try:
            await self.applicant.send(
                f"❌ Your application to Rosethorn was not accepted.\n\n**Reason:** {reason}"
            )
        except:
            print(f"[Rosethorn] Could not DM {self.applicant}")

        # Log to staff channel
        staff_log = interaction.client.get_channel(STAFF_LOG_CHANNEL_ID)
        if staff_log:
            embed = discord.Embed(
                title="❌ Application Denied",
                description=f"{self.applicant.mention} was denied.\n\n**Reason:** {reason}",
                color=0xaa3333
            )
            embed.set_footer(text=f"Handled by {interaction.user}")
            await staff_log.send(embed=embed)

        # ✅ Delete thread after submission
        try:
            await self.thread.delete()
        except:
            print(f"[Rosethorn] Could not delete thread {self.thread}")

class ReviewPanel(discord.ui.View):
    def __init__(self, applicant: discord.Member, thread: discord.Thread):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.thread = thread

    @discord.ui.button(label="✅ Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Detect role based on thread name
        if "Admin" in self.thread.name:
            role_id = ADMIN_ROLE_ID
        elif "Realm Job" in self.thread.name:
            role_id = REALM_JOB_ROLE_ID
        else:
            await interaction.response.send_message("⚠️ Couldn't determine role for this thread.", ephemeral=True)
            return

        role = discord.utils.get(interaction.guild.roles, id=role_id)
        if role:
            await self.applicant.add_roles(role)
            await self.applicant.send(f"🌸 Your application was approved — you've been granted the role: {role.name}!")

        staff_log = interaction.client.get_channel(STAFF_LOG_CHANNEL_ID)
        if staff_log:
            embed = discord.Embed(
                title="✅ Application Approved",
                description=f"{self.applicant.mention} was approved.\nRole: {role.name}",
                color=0x3ba55d
            )
            embed.set_footer(text=f"Approved by {interaction.user}")
            await staff_log.send(embed=embed)

        await interaction.response.send_message("✅ Applicant approved and role assigned.", ephemeral=True)

        await asyncio.sleep(10)
        try:
            await self.thread.delete()
        except:
            print(f"[Rosethorn] Could not delete thread {self.thread}")

    @discord.ui.button(label="❌ Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DenialReasonModal(self.applicant, self.thread))

class ReviewButton(discord.ui.View):
    def __init__(self, applicant: discord.Member, thread: discord.Thread):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.thread = thread

    @discord.ui.button(label="📝 Review Application", style=discord.ButtonStyle.primary)
    async def review_app(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Choose an option below:",
            view=ReviewPanel(self.applicant, self.thread),
            ephemeral=True
        )

class ReviewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="review_buttons", description="Drop review buttons into a thread")
    @app_commands.checks.has_role(STAFF_ROLE_ID)
    async def review_buttons(self, interaction: discord.Interaction):
        applicant = interaction.channel.members[0] if interaction.channel.members else None

        if not isinstance(interaction.channel, discord.Thread) or not applicant:
            await interaction.response.send_message("⚠️ This must be used inside an application thread.", ephemeral=True)
            return

        await interaction.channel.send("Staff Review:", view=ReviewButton(applicant, interaction.channel))
        await interaction.response.send_message("✅ Review button sent to thread.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReviewCog(bot))
    print("[Rosethorn] review cog loaded.")

    # 🔒 Guild sync
    GUILD = discord.Object(id=1308904661578813540)
    bot.tree.copy_global_to(guild=GUILD)
    await bot.tree.sync(guild=GUILD)
