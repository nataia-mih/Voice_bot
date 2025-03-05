# Voice_Bot

## Prerequisites
- Python 3.8+
- LM Studio running locally
- Telegram Bot Token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nataia-mih/Voice_bot.git
cd Voice_bot
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export TELEGRAM_BOT_TOKEN='your_telegram_bot_token'
export LMSTUDIO_API_URL='http://localhost:1234/v1/chat/completions'
```

5. Run the bot:
```bash
python bot.py
```

## Configuration

Modify `config.py` to customize:
- Telegram Bot Token
- LM Studio API URL
- Whisper Model
- TTS Engine

## Notes
- Ensure LM Studio is running and API is accessible
- First-time Whisper model download may take time
