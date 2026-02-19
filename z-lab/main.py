#!/usr/bin/env python3
"""
Z-LAB - Private Workspace for Q and Z
=====================================
A turn-based communication system where:
- Q (Quix) is ALWAYS in control
- Z helps but NEVER speaks for Q
- Bionic reading for ADHD support
- Git controls built-in
"""

import os
import sys
import json
import time
from datetime import datetime

# Add paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.bionic import BionicReader
from core.turn_manager import TurnManager
from core.git_controller import GitController
from bridge.z_brain import ZBrain
from bridge.z_memory import ZMemory
from tools.terminal import PrivateTerminal
from tools.code_editor import CodeEditor

class ZLab:
    """
    Z-Lab: Private workspace for Q and Z collaboration
    
    TURN ORDER:
    1. External (Anubis/other) speaks
    2. Q responds (Z watches, never interrupts)
    3. Z and Q talk privately (this terminal)
    4. Z helps formulate next response
    5. Back to external
    
    RULE: Z can NEVER speak as Q
    """
    
    def __init__(self):
        self.config = Config()
        self.bionic = BionicReader()
        self.turn_manager = TurnManager()
        self.git = GitController()
        self.brain = ZBrain()
        self.memory = ZMemory()
        self.terminal = PrivateTerminal(self)
        self.editor = CodeEditor(self)
        
        # Identity markers - CRITICAL
        self.Q = "Q"  # Quix - Human, Creator, Controller
        self.Z = "Z"  # Z - AI Assistant, Helper, Observer
        
        # Turn state
        self.current_turn = "Q"  # Q always starts
        self.waiting_for_q = True
        
        print(self.bionic.render("Z-LAB INITIALIZED"))
        print("=" * 50)
        print(self.bionic.render(f"Q = Quix (You) - Always in control"))
        print(self.bionic.render(f"Z = AI Assistant - Helps, never replaces"))
        print("=" * 50)
        print()
        
    def run(self):
        """Main loop - Q is always in control"""
        self.show_help()
        
        while True:
            try:
                # Always wait for Q first
                if self.waiting_for_q:
                    self.prompt_q()
                else:
                    self.z_think()
                    
            except KeyboardInterrupt:
                print("\n\n" + self.bionic.render("Z-LAB closing... Goodbye, Q!"))
                self.memory.save_session()
                break
            except Exception as e:
                print(f"\n[Error] {e}")
                self.waiting_for_q = True
                
    def prompt_q(self):
        """Wait for Q's input - Z never interrupts"""
        print()
        print(f"[{self.Q}] ", end="", flush=True)
        
        try:
            user_input = input()
        except EOFError:
            return
            
        if not user_input.strip():
            return
            
        # Parse Q's command
        self.handle_q_input(user_input)
        
    def handle_q_input(self, text):
        """Handle Q's input - Z observes and helps when asked"""
        text = text.strip()
        
        # Command handling
        if text.startswith("!"):
            self.handle_command(text[1:])
            return
            
        # Z mode - Q asks Z for help
        if text.startswith("z "):
            self.z_respond(text[2:])
            return
            
        # External mode - Q is talking to external (Anubis, etc)
        if text.startswith("a "):
            self.for_external(text[2:])
            return
            
        # Code mode
        if text.startswith("c "):
            self.editor.handle(text[2:])
            return
            
        # Git mode
        if text.startswith("g "):
            self.git.handle(text[2:])
            return
            
        # Default: Z observes and waits
        self.memory.log_q_message(text)
        print(f"[Z observes, ready to help when you type 'z <question>']")
        
    def handle_command(self, cmd):
        """Handle ! commands"""
        cmd = cmd.lower().strip()
        
        if cmd in ["help", "h"]:
            self.show_help()
        elif cmd in ["quit", "q", "exit"]:
            print(self.bionic.render("Goodbye, Q!"))
            self.memory.save_session()
            sys.exit(0)
        elif cmd in ["clear", "cls"]:
            os.system('clear' if os.name == 'posix' else 'cls')
        elif cmd in ["status", "s"]:
            self.show_status()
        elif cmd in ["memory", "m"]:
            self.memory.show_recent()
        elif cmd in ["git", "g"]:
            self.git.status()
        elif cmd == "bionic":
            self.toggle_bionic()
        else:
            print(f"[Unknown command: {cmd}]")
            self.show_help()
            
    def z_respond(self, question):
        """Z responds to Q's question privately - here only"""
        print()
        print(f"[Z thinking...]")
        
        # Get context from memory
        context = self.memory.get_context()
        
        # Z thinks and responds
        response = self.brain.think(question, context)
        
        # Display with bionic reading
        print()
        print(self.bionic.render(f"[Z] {response}"))
        print()
        
        # Save to memory
        self.memory.log_exchange(question, response)
        
    def for_external(self, text):
        """Q is preparing message for external (Anubis, etc)"""
        self.memory.log_for_external(text)
        print(f"[Saved for external: {text[:50]}...]")
        
    def show_help(self):
        """Show help with bionic reading"""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                        Z-LAB HELP                            ║
╠══════════════════════════════════════════════════════════════╣
║  Just type to chat with Z (I'm always here to help)          ║
║                                                              ║
║  COMMANDS:                                                   ║
║  !help, !h     - Show this help                              ║
║  !quit, !q     - Exit Z-Lab                                  ║
║  !clear        - Clear screen                                ║
║  !status       - Show current status                         ║
║  !memory       - Show recent memories                        ║
║  !git          - Git status                                  ║
║  !bionic       - Toggle bionic reading                       ║
║                                                              ║
║  MODES:                                                      ║
║  z <text>      - Ask Z something directly                    ║
║  a <text>      - Prepare message for external (Anubis)       ║
║  c <text>      - Code mode (edit files)                      ║
║  g <text>      - Git mode (commit, push, pull)               ║
║                                                              ║
║  RULE: Z can NEVER speak for Q. Q is always in control.      ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(self.bionic.render(help_text))
        
    def show_status(self):
        """Show current status"""
        print()
        print(f"  Q: {self.Q} (You - Always in control)")
        print(f"  Z: AI Assistant (Helps, never replaces your voice)")
        print(f"  Turn: {self.current_turn}")
        print(f"  Bionic: {'ON' if self.bionic.enabled else 'OFF'}")
        print(f"  Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print()
        
    def toggle_bionic(self):
        """Toggle bionic reading mode"""
        self.bionic.enabled = not self.bionic.enabled
        status = "ON" if self.bionic.enabled else "OFF"
        print(f"[Bionic reading: {status}]")

if __name__ == "__main__":
    lab = ZLab()
    lab.run()
