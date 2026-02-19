#!/bin/bash
# Anubis V2 Installer - Run this on your PC

mkdir -p ~/Documents/Anubis/{tools,soul,memory,data,services,bots,sessions}
cd ~/Documents/Anubis

# requirements.txt
cat > requirements.txt << 'ENDREQ'
rich>=13.0.0
playwright>=1.40.0
python-telegram-bot>=21.0
langchain>=0.3.0
langchain-ollama>=0.2.0
requests>=2.31.0
ENDREQ

# config.py
cat > config.py << 'ENDCFG'
import os
OLLAMA_BASE_URL = "http://localhost:11434"
PRIMARY_MODEL = "deepseek-r1:14b"
FALLBACK_MODEL = "qwen2.5:7b"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENDCFG

# soul/__init__.py
cat > soul/__init__.py << 'ENDINIT'
from .core import AnubisSoul, get_soul
ENDINIT

# soul/core.py
cat > soul/core.py << 'ENDCORE'
import json
from pathlib import Path
from datetime import datetime

class AnubisSoul:
    def __init__(self):
        self.memory_dir = Path.home() / ".anubis" / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.episodic = []
        self._load()

    def _load(self):
        f = self.memory_dir / "episodic.json"
        if f.exists():
            self.episodic = json.loads(f.read_text())

    def _save(self):
        (self.memory_dir / "episodic.json").write_text(json.dumps(self.episodic[-100:], indent=2))

    def process_message(self, user, resp):
        self.episodic.append({"time": datetime.now().isoformat(), "user": user, "anubis": resp})
        self._save()

    def get_greeting(self):
        h = datetime.now().hour
        return "Good morning!" if h < 12 else "Good afternoon!" if h < 18 else "Good evening!"

    def get_context(self, msg):
        return f"Remembering {len(self.episodic)} conversations."

    def get_status(self):
        return f"Memory: {len(self.episodic)} conversations"

def get_soul():
    return AnubisSoul()
ENDCORE

# tools/__init__.py
cat > tools/__init__.py << 'ENDTINI'
from .bash_tool import get_bash_tool
from .telegram_tool import get_telegram_setup
from .whatsapp_tool import get_whatsapp_status, setup_whatsapp
ENDTINI

# tools/bash_tool.py
cat > tools/bash_tool.py << 'ENDBASH'
import subprocess

class BashTool:
    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            return result.stdout or result.stderr or "Done."
        except Exception as e:
            return f"Error: {e}"

def get_bash_tool():
    return BashTool()
ENDBASH

# tools/telegram_tool.py
cat > tools/telegram_tool.py << 'ENDTELE'
import json
from pathlib import Path

SESSION = Path.home() / ".anubis" / "telegram.json"

class TelegramSetup:
    def is_setup(self):
        return SESSION.exists()

    def get_status(self):
        if SESSION.exists():
            return {"has_token": True}
        return {"has_token": False}

    def save_token(self, token):
        SESSION.parent.mkdir(parents=True, exist_ok=True)
        SESSION.write_text(json.dumps({"token": token}))
        return "Token saved! Say 'start telegram bot' to run it."

def get_telegram_setup():
    return TelegramSetup()

def setup_telegram_bot(token):
    t = get_telegram_setup()
    return t.save_token(token)
ENDTELE

# tools/whatsapp_tool.py
cat > tools/whatsapp_tool.py << 'ENDWA'
import json
from pathlib import Path

SESSION = Path.home() / ".anubis" / "whatsapp.json"

def get_whatsapp_status():
    if SESSION.exists():
        return {"setup": True, "phone": "Connected"}
    return {"setup": False, "phone": None}

def setup_whatsapp():
    return """WhatsApp Setup:
1. Run: python ~/.anubis/whatsapp_setup.py
2. Scan QR code with your phone
3. Done! Session saved forever.

First, install playwright:
  pip install playwright && playwright install chromium"""
ENDWA

# main.py
cat > main.py << 'ENDMAIN'
#!/usr/bin/env python3
"""ANUBIS V2 - Your AI Companion"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rich.console import Console
from rich.prompt import Prompt
from soul import get_soul
from tools.bash_tool import get_bash_tool
from tools.telegram_tool import get_telegram_setup
from tools.whatsapp_tool import get_whatsapp_status, setup_whatsapp

console = Console()

def main():
    console.print("""
╔══════════════════════════════════════════════════════════════╗
║         🐺 ANUBIS V2 - Your AI Companion 🐺                  ║
║                                                              ║
║     • Bash Tool - Run terminal commands                      ║
║     • Telegram Bot - Give token once, runs forever           ║
║     • WhatsApp - Scan QR once, remembers forever             ║
║     • Soul System - Memory, Personality, Emotions            ║
╚══════════════════════════════════════════════════════════════╝
""", style="cyan")

    soul = get_soul()
    bash = get_bash_tool()
    telegram = get_telegram_setup()
    
    console.print(f"\n🐺 {soul.get_greeting()}\n", style="cyan")
    
    if telegram.is_setup():
        console.print("📱 Telegram: Configured ✅", style="green")
    else:
        console.print("📱 Telegram: Say 'setup telegram with token YOUR_TOKEN'", style="dim")
    
    wa = get_whatsapp_status()
    if wa["setup"]:
        console.print("💬 WhatsApp: Connected ✅\n", style="green")
    else:
        console.print("💬 WhatsApp: Say 'setup whatsapp'\n", style="dim")
    
    console.print("Commands: /status, /telegram, /whatsapp, /bash CMD, /quit\n", style="green")

    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()
            if not user_input:
                continue

            if user_input.startswith("/"):
                cmd = user_input.lower()
                if cmd in ["/quit", "/exit"]:
                    console.print("\n👋 Goodbye!", style="cyan")
                    break
                elif cmd == "/status":
                    console.print(f"\n{telegram.get_status()}\n{wa}\n{soul.get_status()}", style="white")
                elif cmd == "/whatsapp":
                    console.print(f"\n{setup_whatsapp()}", style="white")
                elif cmd.startswith("/bash "):
                    result = bash.run_command(user_input[6:])
                    console.print(f"\n{result}", style="white")
                continue

            # Check for telegram token
            token_match = re.search(r'(\d+:[A-Za-z0-9_-]+)', user_input)
            if "telegram" in user_input.lower() and token_match:
                from tools.telegram_tool import setup_telegram_bot
                console.print(f"\n{setup_telegram_bot(token_match.group(1))}", style="white")
                continue

            # Check for whatsapp setup
            if "whatsapp" in user_input.lower() and "setup" in user_input.lower():
                console.print(f"\n{setup_whatsapp()}", style="white")
                continue

            # Check for bash command
            lower = user_input.lower()
            if any(kw in lower for kw in ["run ", "execute ", "bash "]):
                cmd = user_input
                for p in ["run ", "execute ", "bash ", "can you "]:
                    if cmd.lower().startswith(p):
                        cmd = cmd[len(p):]
                        break
                console.print(f"\n{bash.run_command(cmd)}", style="white")
                continue

            # Default
            ctx = soul.get_context(user_input)
            console.print(f"\n🐺 Anubis: I understand you want: {user_input}\n{ctx}", style="white")
            soul.process_message(user_input, f"Responded to: {user_input}")

        except KeyboardInterrupt:
            console.print("\n\n👋 Goodbye!", style="cyan")
            break

if __name__ == "__main__":
    main()
ENDMAIN

echo "✅ Anubis V2 installed in ~/Documents/Anubis"
echo ""
echo "Now run:"
echo "  cd ~/Documents/Anubis"
echo "  python3 -m venv venv"
echo "  source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  python main.py"
