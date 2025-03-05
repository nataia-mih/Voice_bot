# bot.py
import os
import requests
import logging
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters
)
import uuid

from config import Config
from audio_utils import AudioProcessor

class LMStudioTelegramBot:
    def __init__(self, config):
        self.config = config
        self.audio_processor = AudioProcessor(config)
        
        # Configure logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
    
    async def start_command(self, update: Update, context):
        """Handle /start command"""
        await update.message.reply_text(
            "Welcome! Send me a text or voice message, and I'll respond using LM Studio."
        )
    
    async def handle_message(self, update: Update, context):
        """Handle text messages"""
        try:
            # Get user message
            message_text = update.message.text
            
            # Generate LM Studio response
            ai_response = self.get_llm_response(message_text)
            
            # Create unique filename for audio
            audio_filename = os.path.join(
                self.config.AUDIO_OUTPUT_DIR, 
                f"{uuid.uuid4()}.wav"
            )
            
            # Generate TTS response
            self.audio_processor.text_to_speech(ai_response, audio_filename)
            
            # Send both text and audio responses
            await update.message.reply_text(ai_response)
            await update.message.reply_voice(
                voice=open(audio_filename, 'rb')
            )
        
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            await update.message.reply_text("Sorry, something went wrong.")
    
    async def handle_voice(self, update: Update, context):
        """Handle voice messages"""
        try:
            # Download voice file
            voice_file = await update.message.voice.get_file()
            voice_path = os.path.join(
                self.config.AUDIO_DOWNLOAD_DIR, 
                f"{uuid.uuid4()}.ogg"
            )
            await voice_file.download(voice_path)
            
            # Transcribe voice to text
            transcribed_text = self.audio_processor.transcribe_audio(voice_path)
            
            if not transcribed_text:
                await update.message.reply_text("Sorry, could not transcribe the audio.")
                return
            
            # Generate LM Studio response
            ai_response = self.get_llm_response(transcribed_text)
            
            # Create unique filename for audio
            audio_filename = os.path.join(
                self.config.AUDIO_OUTPUT_DIR, 
                f"{uuid.uuid4()}.wav"
            )
            
            # Generate TTS response
            self.audio_processor.text_to_speech(ai_response, audio_filename)
            
            # Send both text and audio responses
            await update.message.reply_text(ai_response)
            await update.message.reply_voice(
                voice=open(audio_filename, 'rb')
            )
        
        except Exception as e:
            self.logger.error(f"Error processing voice message: {e}")
            await update.message.reply_text("Sorry, something went wrong.")
    
    def get_llm_response(self, prompt):
        """
        Send request to LM Studio local API
        :param prompt: User's text input
        :return: AI-generated response
        """
        try:
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 150
            }
            
            response = requests.post(
                self.config.LMSTUDIO_API_URL, 
                json=payload, 
                headers={'Content-Type': 'application/json'}
            )
            
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"LM Studio API error: {e}")
            return "Sorry, I'm having trouble connecting to the AI service."
    
    def run(self):
        """Start the Telegram bot"""
        app = Application.builder().token(self.config.TELEGRAM_BOT_TOKEN).build()
        
        # Register handlers
        app.add_handler(CommandHandler('start', self.start_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        app.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        
        # Start the bot
        self.logger.info("Bot started...")
        app.run_polling(drop_pending_updates=True)

def main():
    config = Config()
    bot = LMStudioTelegramBot(config)
    bot.run()

if __name__ == '__main__':
    main()