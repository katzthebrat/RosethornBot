"""
Free AI Service using lightweight libraries
No API keys required - completely free sentiment analysis and content moderation
"""

import logging
import asyncio
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

class HuggingFaceAI:
    """Free AI service using lightweight libraries."""
    
    def __init__(self):
        self.vader_analyzer = None
        self.toxic_words = None
        self.initialized = False
        
    async def initialize(self):
        """Initialize the AI models asynchronously."""
        if self.initialized:
            return
            
        try:
            logger.info("🤖 Initializing free AI models...")
            
            # Initialize VADER sentiment analyzer
            self.vader_analyzer = SentimentIntensityAnalyzer()
            
            # Initialize toxicity word list for content moderation
            self.toxic_words = {
                'hate', 'toxic', 'abuse', 'harassment', 'spam', 'scam', 'threat',
                'violence', 'harmful', 'offensive', 'inappropriate', 'nsfw'
                # Add more as needed - this is a basic starter set
            }
            
            self.initialized = True
            logger.info("🌹 Free AI models ready for Victorian manor management")
            
        except Exception as e:
            logger.error(f"🥀 Error initializing AI models: {e}")
            self.initialized = False
    
    async def analyze_sentiment(self, text):
        """Analyze sentiment of text using VADER and TextBlob."""
        if not self.initialized:
            await self.initialize()
            
        try:
            # Use VADER for social media style text
            vader_scores = self.vader_analyzer.polarity_scores(text)
            
            # Use TextBlob for additional analysis
            blob = TextBlob(text)
            blob_polarity = blob.sentiment.polarity
            
            # Combine both analyses for better accuracy
            compound_score = vader_scores['compound']
            
            # Determine sentiment based on scores
            if compound_score >= 0.05 or blob_polarity > 0.1:
                return 'positive'
            elif compound_score <= -0.05 or blob_polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
                
        except Exception as e:
            logger.error(f"🥀 Sentiment analysis error: {e}")
            return 'neutral'
    
    async def moderate_content(self, text):
        """Free content moderation using keyword detection and sentiment."""
        if not self.initialized:
            await self.initialize()
            
        try:
            text_lower = text.lower()
            flagged_categories = []
            
            # Check for toxic keywords
            toxic_found = any(word in text_lower for word in self.toxic_words)
            if toxic_found:
                flagged_categories.append('toxic')
            
            # Check for excessive caps (shouting)
            caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
            if caps_ratio > 0.7 and len(text) > 10:
                flagged_categories.append('caps')
            
            # Check for spam patterns (repeated characters)
            if re.search(r'(.)\1{4,}', text):  # 5+ repeated characters
                flagged_categories.append('spam')
            
            # Check sentiment for very negative content
            sentiment = await self.analyze_sentiment(text)
            if sentiment == 'negative':
                # Additional check for very negative sentiment
                vader_scores = self.vader_analyzer.polarity_scores(text)
                if vader_scores['compound'] < -0.8:  # Very negative
                    flagged_categories.append('very_negative')
            
            # Calculate confidence based on number of flags
            confidence = len(flagged_categories) * 0.3
            is_safe = len(flagged_categories) == 0
            
            return {
                'safe': is_safe,
                'confidence': min(confidence, 1.0),
                'categories': flagged_categories
            }
            
        except Exception as e:
            logger.error(f"🥀 Content moderation error: {e}")
            return {'safe': True, 'confidence': 0, 'categories': []}
    
    async def generate_welcome_message(self, username, guild_name):
        """Generate Victorian welcome message (rule-based since we want consistency)."""
        welcome_templates = [
            f"Welcome to our Gothic manor, {username}! May your stay in {guild_name} be filled with Victorian elegance and roses.",
            f"Greetings, {username}! The manor doors of {guild_name} open wide to embrace thee with thorns and grace.",
            f"A new soul graces our Victorian halls! Welcome, {username}, to the distinguished manor of {guild_name}.",
            f"Welcome, dear {username}! May the Gothic beauty of {guild_name} inspire thy journey through our rose-laden corridors.",
            f"Hark! {username} has arrived at our manor! Welcome to {guild_name}, where Victorian splendor meets Gothic mystery."
        ]
        
        import random
        return random.choice(welcome_templates)
    
    async def generate_response(self, prompt, context="", max_tokens=150):
        """Generate Victorian Gothic responses (rule-based for consistency)."""
        # For now, use predefined Victorian responses since free generative models
        # are much larger and would slow down the bot significantly
        
        victorian_responses = [
            "How delightfully intriguing! Pray tell, what manner of Victorian assistance might I provide?",
            "Indeed, most distinguished guest! Your inquiry brings joy to these Gothic halls.",
            "Ah, what a charming request! In the spirit of our manor's elegance, I shall assist thee.",
            "Most certainly! Like roses in our Gothic garden, I shall tend to your needs with care.",
            "By the thorns and petals of our manor! Your words grace these halls with purpose."
        ]
        
        if "help" in prompt.lower() or "assist" in prompt.lower():
            return "Fear not, dear soul! Lady Rosalind stands ready to guide thee through our Victorian manor's mysteries."
        elif "welcome" in prompt.lower():
            return "Welcome, cherished guest! May the Gothic beauty of our manor embrace thee with warmth."
        elif "thank" in prompt.lower():
            return "Your gratitude blooms like roses in our Gothic garden! 'Tis my honor to serve thee."
        else:
            import random
            return random.choice(victorian_responses)

# Global instance
free_ai = HuggingFaceAI()