import discord
from review_flow import ReviewButton  # 👈 Import staff review panel

STAFF_NOTIFICATION_CHANNEL_ID = 1320540890141556746  # Replace with your real channel ID

class AdminApplicationModal(discord.ui.Modal):
    def __init__(self, thread):
        super().__init__(title="Admin Application", timeout=None)
        self.thread = thread

        self.add_item(discord.ui.TextInput(
            label="Which responsibilities interest you?",
            placeholder="Moderation, events, mentoring, etc.",
            style=discord.TextStyle.paragraph
        ))
        self.add_item(discord.ui.TextInput(
            label="Your moderation or leadership experience?",
            placeholder="Tools, roles, conflict resolution...",
            style=discord.TextStyle.paragraph
        ))
        self.add_item(discord.ui.TextInput(
            label="Handling conflict between members?",
            placeholder="Your de-escalation approach...",
            style=discord.TextStyle.paragraph
        ))
        self.add_item(discord.ui.TextInput(
            label="Your active times or time zone?",
            placeholder="Let us know when you're available.",
            style=discord.TextStyle.short
        ))
        self.add_item(discord.ui.TextInput(
            label="Why do you want to support Rosethorn?",
            placeholder="Share your personal motivation.",
            style=discord.TextStyle.paragraph
        ))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="📝 Admin Application Submitted",
                description=f"{interaction.user.mention} has completed their application.",
                color=0x5865f2
            )
            for q in self.children:
                embed.add_field(name=q.label, value=q.value, inline=False)
            embed.set_footer(text="Rosethorn Bot | Admin Application")

            await self.thread.send(embed=embed)
            await self.thread.send("Staff Review:", view=ReviewButton(interaction.user, self.thread))
            await interaction.response.send_message("✅ Your admin application was posted!", ephemeral=True)

            staff_channel = interaction.client.get_channel(STAFF_NOTIFICATION_CHANNEL_ID)
            if staff_channel:
                await staff_channel.send(
                    f"📣 New Admin Application from {interaction.user.mention} in {self.thread.mention}"
                )
        except Exception as e:
            print(f"[Rosethorn Modal Error] Admin: {e}")

class RealmJobApplicationModal(discord.ui.Modal):
    def __init__(self, thread):
        super().__init__(title="Realm Job Application", timeout=None)
        self.thread = thread

        self.add_item(discord.ui.TextInput(
            label="Which realm job interests you most?",
            placeholder="Builder, lore crafter, gatherer, etc.",
            style=discord.TextStyle.short
        ))
        self.add_item(discord.ui.TextInput(
            label="Your creative experience or background?",
            placeholder="Projects, tools, preferred style...",
            style=discord.TextStyle.paragraph
        ))
        self.add_item(discord.ui.TextInput(
            label="Ideas or plans you'd bring to Rosethorn?",
            placeholder="Share any pitch or concept.",
            style=discord.TextStyle.paragraph
        ))
        self.add_item(discord.ui.TextInput(
            label="How do you prefer to collaborate?",
            placeholder="Team habits, communication style...",
            style=discord.TextStyle.paragraph
        ))
        self.add_item(discord.ui.TextInput(
            label="What inspires you to apply here?",
            placeholder="Describe your connection or motivation.",
            style=discord.TextStyle.paragraph
        ))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="📦 Realm Job Application Submitted",
                description=f"{interaction.user.mention} has completed their creative application.",
                color=0x2f3136
            )
            for q in self.children:
                embed.add_field(name=q.label, value=q.value, inline=False)
            embed.set_footer(text="Rosethorn Bot | Realm Job Form")

            await self.thread.send(embed=embed)
            await self.thread.send("Staff Review:", view=ReviewButton(interaction.user, self.thread))
            await interaction.response.send_message("✅ Your realm job application was posted!", ephemeral=True)

            staff_channel = interaction.client.get_channel(STAFF_NOTIFICATION_CHANNEL_ID)
            if staff_channel:
                await staff_channel.send(
                    f"✨ New Realm Job Application from {interaction.user.mention} in {self.thread.mention}"
                )
        except Exception as e:
            print(f"[Rosethorn Modal Error] Realm Job: {e}")
