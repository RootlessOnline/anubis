#!/usr/bin/env python3
"""
Private Terminal - Q and Z's Private Communication Channel
===========================================================
This is where Q and Z talk privately, away from external entities.
"""

import os
import sys
import subprocess
from datetime import datetime

class PrivateTerminal:
    """
    Private terminal for Q-Z communication
    
    This terminal is SEPARATE from:
    - External terminal (where Anubis talks)
    - System terminal (bash, etc)
    
    It's a safe space for Q and Z.
    """
    
    def __init__(self, zlab):
        self.zlab = zlab
        self.bionic = zlab.bionic
        self.brain = zlab.brain
        self.memory = zlab.memory
        
        # Terminal state
        self.mode = "chat"  # chat, code, git
        self.history = []
        
    def clear(self):
        """Clear the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(self.bionic.render("Z-LAB - Private Terminal"))
        print("=" * 40)
        
    def show_prompt(self):
        """Show the terminal prompt"""
        if self.mode == "chat":
            prompt = f"[{self.zlab.Q}] "
        elif self.mode == "code":
            prompt = "[CODE] "
        elif self.mode == "git":
            prompt = "[GIT] "
        else:
            prompt = "> "
            
        print(prompt, end="", flush=True)
        
    def execute_shell(self, command):
        """Execute a shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout or result.stderr
            print(output)
            return output
        except subprocess.TimeoutExpired:
            print("Command timed out")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
            
    def show_banner(self):
        """Show welcome banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ███████╗██╗   ██╗ ██████╗ ██████╗███████╗            ║
║     ╚══███╔╝██║   ██║██╔═══██╗██╔══██║██╔════╝            ║
║       ███╔╝ ██║   ██║██║   ██║██║  ██║█████╗              ║
║      ███╔╝  ██║   ██║██║   ██║██║  ██║██╔══╝              ║
║     ███████╗╚██████╔╝╚██████╔╝██████╔╝███████╗            ║
║     ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝            ║
║                                                           ║
║           P R I V A T E   T E R M I N A L                 ║
║                                                           ║
║     Q (Quix) ◄──────────────────► Z (AI Assistant)        ║
║                                                           ║
║     RULE: Z can NEVER speak for Q. Q is in control.       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(self.bionic.render(banner))
        
    def show_thinking(self):
        """Show that Z is thinking"""
        print(self.bionic.dim("[Z thinking...]"))
        
    def show_response(self, response):
        """Show Z's response with bionic reading"""
        print()
        print(self.bionic.render(f"[Z] {response}"))
        print()
