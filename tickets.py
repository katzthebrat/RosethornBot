import discord
import logging
import asyncio
from discord.ext import commands

CATEGORY_ID = 1300000000000000000  # Replace with your actual category ID
ADMIN_ROLE_ID = 1300000000000000000  # Replace with your admin role ID

class CloseForm(discord.ui.Modal, title="Rosethorn Ticket Closure"):
    resolution = discord.ui.TextInput(label="How was this resolved?", style=discord.TextStyle.paragraph)

    def __init__(self, member, opener, claimed_by, channel):
        super().__init__()
        self.member = member
        self.opener = opener
        self.claimed_by = claimed_by
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "✅ Ticket closed successfully. This chamber will vanish shortly.",
            ephemeral=True
        )

        embed = discord.Embed(
            title=f"🎟️ {self.channel.name} — CLOSED",
            color=discord.Color.dark_red(),
            description="This chamber has been sealed with wax."
        )
        embed.add_field(name="Opened By", value=self.opener.mention, inline=True)
        embed.add_field(name="Claimed By", value=self.claimed_by.mention if self.claimed_by else "Unclaimed", inline=True)
        embed.add_field(name="Resolution", value=self.resolution.value, inline=False)
        embed.set_footer(text="Rosethorn Bot | Case Closed")
        embed.set_thumbnail(url=self.opener.display_avatar.url)

        await self.channel.send(embed=embed)
        await self.channel.send("📎 Transcript attached. [Coming soon]")
        await asyncio.sleep(10)
        await self.channel.delete(reason="Rosethorn ticket closed")
        logging.info(f"Deleted ticket channel {self.channel.name} after closure.")

class TicketPanel(discord.ui.View):
    def __init__(self, member):
        super().__init__(timeout=None)
        self.member = member
        self.claimed_by = None
        self.opener = member

    @discord.ui.button(label="Permissions", style=discord.ButtonStyle.secondary, emoji="🛡️")
    async def permissions(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, self.member, "permissions")

    @discord.ui.button(label="General", style=discord.ButtonStyle.secondary, emoji="📜")
    async def general(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, self.member, "general")

    @discord.ui.button(label="Report", style=discord.ButtonStyle.secondary, emoji="⚠️")
    async def report(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, self.member, "report")

    @discord.ui.button(label="Review", style=discord.ButtonStyle.secondary, emoji="🧾")
    async def review(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, self.member, "review")

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="❌")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        if ADMIN_ROLE_ID not in [r.id for r in interaction.user.roles]:
            await interaction.response.send_message("⚠️ You lack the admin role required to close this ticket.", ephemeral=True)
            return
        await interaction.response.send_modal(CloseForm(self.member, self.opener, self.claimed_by, interaction.channel))

async def create_ticket(interaction, member, topic):
    guild = interaction.guild
    category = discord.utils.get(guild.categories, id=CATEGORY_ID)
    channel_name = f"🎟️│{member.name}-{topic}"
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    ticket_channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)
    modal = MemberForm(member, ticket_channel)
    await ticket_channel.send(f"Welcome {member.mention}.\nPlease fill out the form below so staff can assist you.")
    await interaction.response.send_modal(modal)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.tree.command(name="tickets", description="Post the Rosethorn ticket panel")
        async def tickets(interaction: discord.Interaction):
            embed = discord.Embed(
                title="🎟️ Rosethorn Ticket Panel",
                description=(
                    "**Choose your request type below** and a velvet chamber will be prepared:\n\n"
                    "🛡️ **Permissions** — Request entry to realms or roles locked behind thorns.\n"
                    "📜 **General** — Ask questions, seek guidance, or summon staff for general matters.\n"
                    "⚠️ **Report** — Raise concerns about member conduct or disruptions.\n"
                    "🧾 **Review** — Plead your case on a recent infraction or disciplinary action."
                ),
                color=discord.Color.from_rgb(113, 20, 23)
            )
            embed.set_footer(text="Rosethorn Bot | Ticket System")
            view = TicketPanel(interaction.user)
            await interaction.channel.send(embed=embed, view=view)
            await interaction.response.send_message("🕊️ Ticket panel posted in this channel.", ephemeral=True)

# ─── Extension Loader ───
async def setup(bot):
    await bot.add_cog(Tickets(bot))
    print("[Rosethorn] Tickets cog loaded.")

    # 🔒 Guild sync
    GUILD = discord.Object(id=1308904661578813540)
    bot.tree.copy_global_to(guild=GUILD)
    await bot.tree.sync(guild=GUILD)
