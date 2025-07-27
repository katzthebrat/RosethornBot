"""
Custom Modal Form Service for RosethornBot
Creates dynamic modal forms with custom questions and handles responses
"""

import discord
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class CustomModalForm(discord.ui.Modal):
    """Dynamic modal form with custom questions"""
    
    def __init__(self, form_config: Dict[str, Any]):
        self.form_config = form_config
        self.form_id = form_config['id']
        self.responses = {}
        
        super().__init__(
            title=form_config.get('title', 'Custom Form'),
            timeout=form_config.get('timeout', 300)
        )
        
        # Add text inputs based on configuration
        for i, question in enumerate(form_config.get('questions', [])):
            if i >= 5:  # Discord modal limit
                break
                
            text_input = discord.ui.TextInput(
                label=question.get('label', f'Question {i+1}'),
                placeholder=question.get('placeholder', ''),
                default=question.get('default', ''),
                required=question.get('required', True),
                max_length=question.get('max_length', 1024),
                style=discord.TextStyle.long if question.get('multiline', False) else discord.TextStyle.short
            )
            
            # Store the question ID for response mapping
            text_input.question_id = question.get('id', f'q{i+1}')
            self.add_item(text_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission"""
        # Collect responses
        for item in self.children:
            if hasattr(item, 'question_id'):
                self.responses[item.question_id] = item.value
        
        # Store response in modal service
        modal_service.store_response(self.form_id, interaction.user.id, self.responses)
        
        # Send confirmation
        embed = discord.Embed(
            title="📝 Form Submitted Successfully",
            description=f"Thank you for completing **{self.form_config.get('title', 'the form')}**",
            color=0x711417
        )
        
        # Add response summary if configured
        if self.form_config.get('show_summary', True):
            summary = ""
            for question in self.form_config.get('questions', []):
                q_id = question.get('id', f'q{self.form_config["questions"].index(question)+1}')
                if q_id in self.responses:
                    label = question.get('label', f'Question {self.form_config["questions"].index(question)+1}')
                    response = self.responses[q_id]
                    # Truncate long responses for summary
                    if len(response) > 100:
                        response = response[:97] + "..."
                    summary += f"**{label}:** {response}\n"
            
            if summary:
                embed.add_field(name="📋 Your Responses", value=summary[:1024], inline=False)
        
        embed.set_footer(text="Response recorded • Rosewood Manor")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Send to configured channel if specified
        if self.form_config.get('log_channel_id'):
            await self._send_to_log_channel(interaction)
    
    async def _send_to_log_channel(self, interaction: discord.Interaction):
        """Send form response to configured log channel"""
        try:
            channel = interaction.guild.get_channel(self.form_config['log_channel_id'])
            if not channel:
                return
            
            embed = discord.Embed(
                title=f"📝 {self.form_config.get('title', 'Form Response')}",
                color=0x711417,
                timestamp=datetime.now()
            )
            
            embed.add_field(name="👤 Submitted By", value=interaction.user.mention, inline=True)
            embed.add_field(name="🆔 User ID", value=str(interaction.user.id), inline=True)
            embed.add_field(name="📅 Submitted", value=discord.utils.format_dt(datetime.now(), style='f'), inline=True)
            
            # Add all responses
            for question in self.form_config.get('questions', []):
                q_id = question.get('id', f'q{self.form_config["questions"].index(question)+1}')
                if q_id in self.responses:
                    label = question.get('label', f'Question {self.form_config["questions"].index(question)+1}')
                    response = self.responses[q_id]
                    
                    # Handle long responses
                    if len(response) > 1024:
                        # Split into multiple fields if too long
                        embed.add_field(name=f"📝 {label} (Part 1)", value=response[:1024], inline=False)
                        if len(response) > 1024:
                            embed.add_field(name=f"📝 {label} (Part 2)", value=response[1024:2048], inline=False)
                    else:
                        embed.add_field(name=f"📝 {label}", value=response or "*No response*", inline=False)
            
            embed.set_footer(text=f"Form ID: {self.form_id} • Rosewood Manor")
            await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error sending form response to log channel: {e}")

class ModalFormService:
    """Service to manage custom modal forms"""
    
    def __init__(self):
        self.forms: Dict[str, Dict] = {}  # form_id -> form_config
        self.responses: Dict[str, List[Dict]] = {}  # form_id -> list of responses
        self.user_responses: Dict[int, Dict] = {}  # user_id -> {form_id: response_data}
    
    def create_form(self, form_id: str, config: Dict[str, Any]) -> bool:
        """Create a new custom form"""
        try:
            # Validate configuration
            if not config.get('title'):
                config['title'] = f"Custom Form {form_id}"
            
            if not config.get('questions'):
                return False
            
            # Limit to 5 questions (Discord modal limit)
            if len(config['questions']) > 5:
                config['questions'] = config['questions'][:5]
            
            # Ensure each question has required fields
            for i, question in enumerate(config['questions']):
                if not question.get('id'):
                    question['id'] = f'q{i+1}'
                if not question.get('label'):
                    question['label'] = f'Question {i+1}'
            
            config['id'] = form_id
            config['created_at'] = datetime.now()
            
            self.forms[form_id] = config
            if form_id not in self.responses:
                self.responses[form_id] = []
            
            logger.info(f"Created custom form: {form_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating form {form_id}: {e}")
            return False
    
    def get_form(self, form_id: str) -> Optional[Dict]:
        """Get form configuration"""
        return self.forms.get(form_id)
    
    def list_forms(self) -> List[str]:
        """List all available forms"""
        return list(self.forms.keys())
    
    def delete_form(self, form_id: str) -> bool:
        """Delete a form and all its responses"""
        if form_id in self.forms:
            del self.forms[form_id]
            if form_id in self.responses:
                del self.responses[form_id]
            logger.info(f"Deleted form: {form_id}")
            return True
        return False
    
    def create_modal(self, form_id: str) -> Optional[CustomModalForm]:
        """Create a modal instance for a form"""
        config = self.get_form(form_id)
        if not config:
            return None
        
        return CustomModalForm(config)
    
    def store_response(self, form_id: str, user_id: int, responses: Dict[str, str]):
        """Store a form response"""
        response_data = {
            'user_id': user_id,
            'responses': responses,
            'submitted_at': datetime.now(),
            'form_id': form_id
        }
        
        if form_id not in self.responses:
            self.responses[form_id] = []
        
        self.responses[form_id].append(response_data)
        
        # Store user response for quick lookup
        if user_id not in self.user_responses:
            self.user_responses[user_id] = {}
        
        self.user_responses[user_id][form_id] = response_data
        
        logger.info(f"Stored response for form {form_id} from user {user_id}")
    
    def get_responses(self, form_id: str) -> List[Dict]:
        """Get all responses for a form"""
        return self.responses.get(form_id, [])
    
    def get_user_response(self, form_id: str, user_id: int) -> Optional[Dict]:
        """Get a specific user's response to a form"""
        user_responses = self.user_responses.get(user_id, {})
        return user_responses.get(form_id)
    
    def export_responses(self, form_id: str) -> Optional[str]:
        """Export form responses as formatted text"""
        form_config = self.get_form(form_id)
        responses = self.get_responses(form_id)
        
        if not form_config or not responses:
            return None
        
        export_text = f"# {form_config['title']} - Response Export\n"
        export_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        export_text += f"Total Responses: {len(responses)}\n\n"
        
        for i, response in enumerate(responses, 1):
            export_text += f"## Response #{i}\n"
            export_text += f"User ID: {response['user_id']}\n"
            export_text += f"Submitted: {response['submitted_at'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for question in form_config['questions']:
                q_id = question['id']
                label = question['label']
                answer = response['responses'].get(q_id, 'No response')
                export_text += f"**{label}**\n{answer}\n\n"
            
            export_text += "---\n\n"
        
        return export_text

# Global service instance
modal_service = ModalFormService()