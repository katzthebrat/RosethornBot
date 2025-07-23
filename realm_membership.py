import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

GUILD_ID = 1308904661578813540  # 👈 Replace with your guild ID

class MembershipCheckView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="See if you qualify to apply", style=discord.ButtonStyle.primary)
    async def check_eligibility(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user

        if member.joined_at is None:
            await interaction.response.send_message(
                "⛔ I can't detect your join date — please try again later or contact staff.",
                ephemeral=True
            )
            return

        join_time = member.joined_at.strftime("%B %d, %Y")
        days_in_server = (datetime.utcnow() - member.joined_at.replace(tzinfo=None)).days

        if days_in_server < 14:
            days_remaining = 14 - days_in_server
            await interaction.response.send_message(
                f"⛔ You joined **{join_time}**.\n"
                f"🕰️ You’ll qualify in **{days_remaining} day(s)** — thanks for your patience!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"✅ You joined **{join_time}** — and you're eligible to apply!\n🌸 The realm awaits you.",
                ephemeral=True
            )

class RealmMembership(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="membershipcheck", description="Check your eligibility to apply for Rosethorn staff")
    @app_commands.guilds(discord.Object(id=GUILD_ID))  # 👈 Instant sync for dev guild
    async def membershipcheck(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="🌒 Rosethorn Membership Eligibility",
                description="Click below to see if you qualify to apply for realm responsibilities or staff roles.",
                color=discord.Color.from_rgb(113, 20, 23)
            )
            embed.set_footer(text="Rosethorn Bot | Eligibility Check")

            # Step 1: Confirm to user
            await interaction.response.send_message(
                "🔍 Membership eligibility check posted to this channel.",
                ephemeral=True
            )

            # Step 2: Public standalone embed with button
            channel = interaction.channel
            await channel.send(
                embed=embed,
                view=MembershipCheckView(),
                allowed_mentions=discord.AllowedMentions.none()
            )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Failed to post eligibility check: `{e}`",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(RealmMembership(bot))
