#!/usr/bin/env python3
"""
Code Editor - Edit Code Together
=================================
Q and Z can edit code together in this private space.
"""

import os
import json
from datetime import datetime

class CodeEditor:
    """
    Simple code editor for Z-Lab
    
    Features:
    - View files
    - Edit files (line by line)
    - Create new files
    - List directory
    """
    
    def __init__(self, zlab):
        self.zlab = zlab
        self.bionic = zlab.bionic
        self.memory = zlab.memory
        
        # Working directory (default to Anubis repo)
        self.work_dir = os.path.expanduser("~/Documents/anubis")
        self.current_file = None
        self.file_content = []
        
    def handle(self, command):
        """Handle code commands"""
        parts = command.strip().split(maxsplit=1)
        action = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        if action in ["help", "h"]:
            self.show_help()
            
        elif action in ["ls", "l", "list"]:
            self.list_dir(args or self.work_dir)
            
        elif action in ["cd", "chdir"]:
            self.change_dir(args)
            
        elif action in ["open", "o", "read", "r"]:
            self.open_file(args)
            
        elif action in ["cat", "show"]:
            self.show_file(args)
            
        elif action in ["new", "create"]:
            self.create_file(args)
            
        elif action in ["edit", "e"]:
            self.edit_line(args)
            
        elif action in ["append", "a"]:
            self.append_line(args)
            
        elif action in ["save", "s"]:
            self.save_file()
            
        elif action in ["close"]:
            self.close_file()
            
        elif action in ["pwd", "where"]:
            print(f"Working dir: {self.work_dir}")
            if self.current_file:
                print(f"Current file: {self.current_file}")
                
        elif action in ["run", "execute"]:
            self.run_file(args)
            
        else:
            print(f"Unknown code command: {action}")
            self.show_help()
            
    def show_help(self):
        """Show code editor help"""
        help_text = """
📝 CODE EDITOR COMMANDS:
────────────────────────
  c ls [path]     - List directory
  c cd <path>     - Change directory
  c pwd           - Show current directory
  
  c open <file>   - Open a file
  c cat <file>    - Show file contents
  c close         - Close current file
  
  c new <file>    - Create new file
  c edit <line>   - Edit a line (interactive)
  c append <text> - Add line to file
  c save          - Save current file
  
  c run <file>    - Run a Python file
  c help          - Show this help
"""
        print(self.bionic.render(help_text))
        
    def list_dir(self, path):
        """List directory contents"""
        target = os.path.join(self.work_dir, path) if path else self.work_dir
        
        if not os.path.exists(target):
            print(f"Path not found: {target}")
            return
            
        if os.path.isfile(target):
            print(f"File: {target}")
            return
            
        print(f"\n📁 {target}/")
        print("─" * 40)
        
        try:
            items = sorted(os.listdir(target))
            for item in items:
                item_path = os.path.join(target, item)
                if os.path.isdir(item_path):
                    print(f"  📂 {item}/")
                else:
                    size = os.path.getsize(item_path)
                    print(f"  📄 {item} ({size} bytes)")
        except PermissionError:
            print("Permission denied")
            
    def change_dir(self, path):
        """Change working directory"""
        if not path:
            print("Usage: c cd <path>")
            return
            
        # Handle ~ expansion
        path = os.path.expanduser(path)
        
        # Make absolute if relative
        if not os.path.isabs(path):
            path = os.path.join(self.work_dir, path)
            
        if os.path.exists(path) and os.path.isdir(path):
            self.work_dir = path
            print(f"Changed to: {path}")
        else:
            print(f"Directory not found: {path}")
            
    def open_file(self, filename):
        """Open a file for editing"""
        if not filename:
            print("Usage: c open <filename>")
            return
            
        filepath = os.path.join(self.work_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            print("Use 'c new <filename>' to create a new file")
            return
            
        try:
            with open(filepath, 'r') as f:
                self.file_content = f.read().splitlines()
            self.current_file = filepath
            print(f"Opened: {filepath}")
            print(f"Lines: {len(self.file_content)}")
            print("Use 'c cat' to view, 'c edit <line>' to edit")
        except Exception as e:
            print(f"Error opening file: {e}")
            
    def show_file(self, filename=None):
        """Show file contents with line numbers"""
        if filename:
            filepath = os.path.join(self.work_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    lines = f.read().splitlines()
                self._display_lines(lines)
            else:
                print(f"File not found: {filename}")
        elif self.current_file and self.file_content:
            self._display_lines(self.file_content)
        else:
            print("No file open. Use 'c open <filename>'")
            
    def _display_lines(self, lines, start=1):
        """Display lines with numbers"""
        for i, line in enumerate(lines, start):
            # Highlight current line if editing
            print(f"{i:4d} │ {line}")
            
    def create_file(self, filename):
        """Create a new file"""
        if not filename:
            print("Usage: c new <filename>")
            return
            
        filepath = os.path.join(self.work_dir, filename)
        
        if os.path.exists(filepath):
            print(f"File already exists: {filepath}")
            return
            
        self.current_file = filepath
        self.file_content = []
        print(f"Created new file: {filepath}")
        print("Use 'c append <text>' to add lines")
        print("Use 'c save' to save")
        
    def append_line(self, text):
        """Append a line to the current file"""
        if not self.current_file:
            print("No file open. Use 'c new' or 'c open'")
            return
            
        self.file_content.append(text)
        print(f"Added line {len(self.file_content)}: {text}")
        
    def edit_line(self, args):
        """Edit a specific line"""
        if not self.current_file:
            print("No file open")
            return
            
        parts = args.split(maxsplit=1)
        if not parts:
            print("Usage: c edit <line_number> [new_text]")
            return
            
        try:
            line_num = int(parts[0])
            new_text = parts[1] if len(parts) > 1 else None
        except ValueError:
            print("Line number must be an integer")
            return
            
        if line_num < 1 or line_num > len(self.file_content):
            print(f"Line number out of range (1-{len(self.file_content)})")
            return
            
        if new_text:
            # Direct edit
            old = self.file_content[line_num - 1]
            self.file_content[line_num - 1] = new_text
            print(f"Changed line {line_num}:")
            print(f"  Old: {old}")
            print(f"  New: {new_text}")
        else:
            # Show line and prompt
            print(f"Line {line_num}: {self.file_content[line_num - 1]}")
            print("Enter new text (or press Enter to keep):")
            try:
                new = input("Edit> ")
                if new:
                    self.file_content[line_num - 1] = new
                    print("Line updated")
            except EOFError:
                pass
                
    def save_file(self):
        """Save the current file"""
        if not self.current_file:
            print("No file open")
            return
            
        try:
            with open(self.current_file, 'w') as f:
                f.write('\n'.join(self.file_content))
                if self.file_content:
                    f.write('\n')
            print(f"Saved: {self.current_file}")
        except Exception as e:
            print(f"Error saving: {e}")
            
    def close_file(self):
        """Close the current file"""
        if self.current_file:
            print(f"Closed: {self.current_file}")
            self.current_file = None
            self.file_content = []
        else:
            print("No file open")
            
    def run_file(self, filename=None):
        """Run a Python file"""
        if filename:
            filepath = os.path.join(self.work_dir, filename)
        elif self.current_file:
            filepath = self.current_file
        else:
            print("No file to run. Specify a filename.")
            return
            
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return
            
        print(f"Running: {filepath}")
        print("─" * 40)
        
        import subprocess
        result = subprocess.run(
            ["python3", filepath],
            capture_output=True,
            text=True,
            cwd=self.work_dir
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
