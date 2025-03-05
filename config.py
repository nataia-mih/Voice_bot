# config.py
import os

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'your-telegram-token')
    
    # LM Studio API Configuration
    LMSTUDIO_API_URL = os.environ.get('LMSTUDIO_API_URL', 'http://localhost:1234/v1/chat/completions')
    
    # Audio Configuration
    AUDIO_DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
    AUDIO_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
    
    # Make sure directories exist
    os.makedirs(AUDIO_DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    
    # Whisper Model Configuration
    WHISPER_MODEL = 'base'  # Can be 'tiny', 'base', 'small', 'medium', 'large'
    
    # TTS Configuration
    TTS_ENGINE = 'coqui'  # Options: 'coqui', 'google', 'elevenlabs'
