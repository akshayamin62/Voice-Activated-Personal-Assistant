# Windows Voice Assistant

A voice-controlled personal assistant for Windows 11, powered by Groq LLM (Llama 3) for smart responses. Activate with a hotkey, control your PC, set reminders, play music/videos, and more—all with your voice!

## Features
- Voice activation (Ctrl+Shift+J)
- Smart conversational AI (Groq Llama 3)
- Open Notepad, Calculator, websites
- Web search
- System control: volume, mute, lock, shutdown, restart
- Reminders and alarms
- Play local music/video files or YouTube
- Extensible modular command system

## Setup

1. **Clone the repository**
2. **Install Python 3.8+ (recommended: 3.10 or 3.11)**
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Create a `.env` file in the project root:**
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
5. **Run the assistant:**
   ```sh
   python assistant.py
   ```

## Usage
- Press **Ctrl+Shift+J** to activate listening.
- Try commands like:
  - "open notepad"
  - "open calculator"
  - "open website"
  - "search for Python tutorials"
  - "volume up", "mute", "lock", "shutdown"
  - "remind me" (set reminders)
  - "play music" or "play on YouTube"
  - Or just ask anything for a smart AI response!
- Say **"help"** for a list of supported commands.

## Customization
- Add or modify commands in `assistant.py` (see the modular command functions and routing).
- To enable news or weather, add your API keys to `.env` and update the placeholders in the code.

## Security
- Your `.env` file (with API keys) is excluded from git by `.gitignore`.

## License
MIT License 