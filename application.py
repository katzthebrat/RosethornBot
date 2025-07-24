import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import asyncio
from datetime import datetime

class ApplicationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Apply for Admin', style=discord.ButtonStyle.primary, emoji='🛡️')
    async def admin_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ApplicationModal('admin')
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label='Apply for Realm Job', style=discord.ButtonStyle.secondary, emoji='⚒️')
    async def realm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ApplicationModal('realm')
        await interaction.response.send_modal(modal)

class ApplicationModal(discord.ui.Modal):
    def __init__(self, application_type):
        self.application_type = application_type
        title = f"Application for {'Admin' if application_type == 'admin' else 'Realm Job'}"
        super().__init__(title=title)
        
        # Common questions for both positions
        self.add_item(discord.ui.TextInput(
            label='What is your Discord username and age?',
            placeholder='Username#0000, Age: XX',
            max_length=100,
            required=True
        ))
        
        self.add_item(discord.ui.TextInput(
            label='Why do you want this position?',
            style=discord.TextStyle.paragraph,
            placeholder='Explain your motivation and goals...',
            max_length=500,
            required=True
        ))
        
        self.add_item(discord.ui.TextInput(
            label='What relevant experience do you have?',
            style=discord.TextStyle.paragraph,
            placeholder='Previous roles, skills, achievements...',
            max_length=500,
            required=True
        ))
        
        if application_type == 'admin':
            self.add_item(discord.ui.TextInput(
                label='How would you handle rule violations?',
                style=discord.TextStyle.paragraph,
                placeholder='Describe your moderation approach...',
                max_length=400,
                required=True
            ))
        else:
            self.add_item(discord.ui.TextInput(
                label='What realm projects interest you most?',
                style=discord.TextStyle.paragraph,
                placeholder='Building, events, community projects...',
                max_length=400,
                required=True
            ))
        
        self.add_item(discord.ui.TextInput(
            label='How many hours can you dedicate weekly?',
            placeholder='X hours per week, available times...',
            max_length=200,
            required=True
        ))

    async def on_submit(self, interaction: discord.Interaction):
        # Create private thread
        admin_role = interaction.guild.get_role(1308905911489921124)
        
        thread_name = f"{self.application_type.title()} Application - {interaction.user.display_name}"
        thread = await interaction.channel.create_thread(
            name=thread_name,
            type=discord.ChannelType.private_thread,
            reason=f"Application thread for {interaction.user}"
        )
        
        # Add admin role and applicant to thread
        await thread.add_user(interaction.user)
        
        # Create application embed
        embed = discord.Embed(
            title=f"📋 {self.application_type.title()} Application",
            description=f"**Applicant:** {interaction.user.mention}\n**Position:** {self.application_type.title()}",
            color=0x2ecc71 if self.application_type == 'admin' else 0x3498db,
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        
        # Add answers to embed
        questions = [
            "What is your Discord username and age?",
            "Why do you want this position?",
            "What relevant experience do you have?",
            "How would you handle rule violations?" if self.application_type == 'admin' else "What realm projects interest you most?",
            "How many hours can you dedicate weekly?"
        ]
        
        for i, (question, answer) in enumerate(zip(questions, [child.value for child in self.children])):
            embed.add_field(
                name=f"**Q{i+1}:** {question}",
                value=answer[:1000] + "..." if len(answer) > 1000 else answer,
                inline=False
            )
        
        embed.set_footer(text=f"Application ID: {thread.id}")
        
        # Send application in thread with admin mention
        review_view = ApplicationReviewView(self.application_type, interaction.user.id, thread.id)
        await thread.send(f"{admin_role.mention}", embed=embed, view=review_view)
        
        # Send notification to staff channel
        staff_channel = interaction.guild.get_channel(1320540890141556746)
        if staff_channel:
            notification_embed = discord.Embed(
                title="🔔 New Application Submitted",
                description=f"**{interaction.user.mention}** applied for **{self.application_type.title()}**",
                color=0xf39c12,
                timestamp=datetime.utcnow()
            )
            notification_embed.add_field(
                name="Thread", 
                value=f"[Click here to review]({thread.jump_url})",
                inline=False
            )
            notification_embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
            
            # Store message for later updates
            notification_msg = await staff_channel.send(embed=notification_embed)
            
            # Save application data for tracking
            app_data = {
                'applicant_id': interaction.user.id,
                'application_type': self.application_type,
                'thread_id': thread.id,
                'notification_msg_id': notification_msg.id,
                'status': 'pending',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Save to JSON file
            applications_file = 'data/applications.json'
            if not os.path.exists('data'):
                os.makedirs('data')
            
            applications = {}
            if os.path.exists(applications_file):
                with open(applications_file, 'r') as f:
                    applications = json.load(f)
            
            applications[str(thread.id)] = app_data
            
            with open(applications_file, 'w') as f:
                json.dump(applications, f, indent=2)
        
        # Respond to interaction
        await interaction.response.send_message(
            f"✅ Your {self.application_type} application has been submitted! Click here to view: {thread.mention}",
            ephemeral=True
        )

class ApplicationReviewView(discord.ui.View):
    def __init__(self, application_type, applicant_id, thread_id):
        super().__init__(timeout=None)
        self.application_type = application_type
        self.applicant_id = applicant_id
        self.thread_id = thread_id
    
    @discord.ui.button(label='Start Review', style=discord.ButtonStyle.primary, emoji='📝')
    async def start_review(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Update status to under review
        await self.update_application_status('under_review', interaction.user)
        
        # Send review message
        embed = discord.Embed(
            title="🔍 Application Under Review",
            description=f"This application is now being reviewed by {interaction.user.mention}",
            color=0xf39c12,
            timestamp=datetime.utcnow()
        )
        await interaction.response.send_message(embed=embed)
        
        # Replace buttons with approve/deny
        decision_view = ApplicationDecisionView(self.application_type, self.applicant_id, self.thread_id)
        await interaction.edit_original_response(view=decision_view)
    
    async def update_application_status(self, status, reviewer=None):
        applications_file = 'data/applications.json'
        if os.path.exists(applications_file):
            with open(applications_file, 'r') as f:
                applications = json.load(f)
            
            if str(self.thread_id) in applications:
                app_data = applications[str(self.thread_id)]
                app_data['status'] = status
                if reviewer:
                    app_data['reviewer_id'] = reviewer.id
                    app_data['reviewer_name'] = str(reviewer)
                
                with open(applications_file, 'w') as f:
                    json.dump(applications, f, indent=2)
                
                # Update notification in staff channel
                guild = reviewer.guild if reviewer else None
                if guild:
                    staff_channel = guild.get_channel(1320540890141556746)
                    if staff_channel and 'notification_msg_id' in app_data:
                        try:
                            msg = await staff_channel.fetch_message(app_data['notification_msg_id'])
                            embed = msg.embeds[0]
                            
                            if status == 'under_review':
                                embed.color = 0xf39c12
                                embed.title = "🔍 Application Under Review"
                                embed.add_field(
                                    name="Reviewer",
                                    value=reviewer.mention,
                                    inline=True
                                )
                            elif status == 'approved':
                                embed.color = 0x2ecc71
                                embed.title = "✅ Application Approved"
                            elif status == 'denied':
                                embed.color = 0xe74c3c
                                embed.title = "❌ Application Denied"
                            
                            await msg.edit(embed=embed)
                        except:
                            pass

class ApplicationDecisionView(discord.ui.View):
    def __init__(self, application_type, applicant_id, thread_id):
        super().__init__(timeout=None)
        self.application_type = application_type
        self.applicant_id = applicant_id
        self.thread_id = thread_id
    
    @discord.ui.button(label='Approve', style=discord.ButtonStyle.success, emoji='✅')
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin role
        if not any(role.id == 1308905911489921124 for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don't have permission to approve applications.", ephemeral=True)
            return
        
        applicant = interaction.guild.get_member(self.applicant_id)
        if not applicant:
            await interaction.response.send_message("❌ Applicant not found in server.", ephemeral=True)
            return
        
        # Give appropriate role
        role_id = 1320538700656148541 if self.application_type == 'admin' else 1394853894437343422
        role = interaction.guild.get_role(role_id)
        
        if role:
            await applicant.add_roles(role, reason=f"Approved for {self.application_type} by {interaction.user}")
        
        # Send DM to applicant
        try:
            dm_embed = discord.Embed(
                title="🎉 Application Approved!",
                description=f"Congratulations! Your application for **{self.application_type.title()}** has been approved.",
                color=0x2ecc71,
                timestamp=datetime.utcnow()
            )
            dm_embed.add_field(
                name="What's Next?",
                value=f"You have been given the {role.mention if role else self.application_type} role. Welcome to the team!",
                inline=False
            )
            dm_embed.set_footer(text="Welcome to the Rosewood Paradise team!")
            
            await applicant.send(embed=dm_embed)
        except:
            pass
        
        # Update status
        review_view = ApplicationReviewView(self.application_type, self.applicant_id, self.thread_id)
        await review_view.update_application_status('approved', interaction.user)
        
        # Send confirmation
        embed = discord.Embed(
            title="✅ Application Approved",
            description=f"{applicant.mention}'s application has been approved by {interaction.user.mention}",
            color=0x2ecc71,
            timestamp=datetime.utcnow()
        )
        await interaction.response.send_message(embed=embed)
        
        # Wait and delete thread
        await asyncio.sleep(10)
        thread = interaction.guild.get_thread(self.thread_id)
        if thread:
            await thread.delete()
    
    @discord.ui.button(label='Deny', style=discord.ButtonStyle.danger, emoji='❌')
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin role
        if not any(role.id == 1308905911489921124 for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don't have permission to deny applications.", ephemeral=True)
            return
        
        # Show reason modal
        modal = DenyReasonModal(self.application_type, self.applicant_id, self.thread_id)
        await interaction.response.send_modal(modal)

class DenyReasonModal(discord.ui.Modal):
    def __init__(self, application_type, applicant_id, thread_id):
        super().__init__(title="Application Denial Reason")
        self.application_type = application_type
        self.applicant_id = applicant_id
        self.thread_id = thread_id
        
        self.add_item(discord.ui.TextInput(
            label='Reason for denial',
            style=discord.TextStyle.paragraph,
            placeholder='Please provide a constructive reason...',
            max_length=500,
            required=True
        ))
    
    async def on_submit(self, interaction: discord.Interaction):
        reason = self.children[0].value
        
        applicant = interaction.guild.get_member(self.applicant_id)
        if not applicant:
            await interaction.response.send_message("❌ Applicant not found in server.", ephemeral=True)
            return
        
        # Send DM to applicant
        try:
            dm_embed = discord.Embed(
                title="📋 Application Update",
                description=f"Thank you for your interest in the **{self.application_type.title()}** position.",
                color=0xe74c3c,
                timestamp=datetime.utcnow()
            )
            dm_embed.add_field(
                name="Application Status",
                value="Unfortunately, your application was not approved at this time.",
                inline=False
            )
            dm_embed.add_field(
                name="Feedback",
                value=reason,
                inline=False
            )
            dm_embed.add_field(
                name="Future Applications",
                value="You're welcome to apply again in the future after addressing the feedback provided.",
                inline=False
            )
            dm_embed.set_footer(text="Thank you for your interest in Rosewood Paradise!")
            
            await applicant.send(embed=dm_embed)
        except:
            pass
        
        # Update status
        review_view = ApplicationReviewView(self.application_type, self.applicant_id, self.thread_id)
        await review_view.update_application_status('denied', interaction.user)
        
        # Send confirmation
        embed = discord.Embed(
            title="❌ Application Denied",
            description=f"{applicant.mention}'s application has been denied by {interaction.user.mention}",
            color=0xe74c3c,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
        
        # Wait and delete thread
        await asyncio.sleep(10)
        thread = interaction.guild.get_thread(self.thread_id)
        if thread:
            await thread.delete()

def ensure_data_files():
    """Ensure application data files exist"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    application_file = 'data/application.json'
    if not os.path.exists(application_file):
        with open(application_file, 'w') as f:
            json.dump({}, f)

@bot.tree.command(name="apply", description="Create application buttons for admin and realm job positions")
async def apply_command(interaction: discord.Interaction):
    # Check if user has the required role
    if not any(role.id == 1308905911489921124 for role in interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    
    # Create application embed - exactly as requested
    embed = discord.Embed(
        title="🌹 Applications 🌹",
        description="**Apply here for admin:** Moderate server and enforce rules, help manage community events, support other staff members, handle player reports and appeals\n\n**Realm job:** Assist with realm projects, help organize community builds, support realm events and activities, maintain realm infrastructure",
        color=0x9b59b6,
        timestamp=datetime.utcnow()
    )
    
    # Create view with application buttons
    view = ApplicationView()
    
    # Send as a public message (not ephemeral)
    await interaction.response.send_message(embed=embed, view=view)

# Initialize data files when module loads
ensure_data_files()
