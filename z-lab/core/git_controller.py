#!/usr/bin/env python3
"""
Git Controller - Repository Management for Z-Lab
=================================================
Allows Q and Z to control git repos together.
"""

import os
import subprocess
from datetime import datetime

class GitController:
    """
    Git operations for Z-Lab
    
    Q's repos:
    - RootlessOnline/anubis (main Anubis repo)
    - Can add more repos
    """
    
    def __init__(self):
        self.repos = {}
        self.current_repo = None
        
        # Default repo (Q's Anubis)
        self.add_repo("anubis", os.path.expanduser("~/Documents/anubis"))
        
    def add_repo(self, name, path):
        """Add a repository"""
        if os.path.exists(path):
            self.repos[name] = path
            if not self.current_repo:
                self.current_repo = name
            return True
        return False
        
    def run_git(self, command, repo=None):
        """Run a git command"""
        repo_name = repo or self.current_repo
        if not repo_name or repo_name not in self.repos:
            return "Error: No repo selected"
            
        repo_path = self.repos[repo_name]
        
        try:
            result = subprocess.run(
                f"cd {repo_path} && git {command}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout or result.stderr
        except subprocess.TimeoutExpired:
            return "Error: Git command timed out"
        except Exception as e:
            return f"Error: {e}"
            
    def status(self):
        """Get git status"""
        output = self.run_git("status -s")
        branch = self.run_git("branch --show-current").strip()
        
        print(f"\n📦 Repo: {self.current_repo}")
        print(f"🌿 Branch: {branch}")
        print(f"📝 Changes:\n{output or '  (clean)'}")
        
    def handle(self, command):
        """Handle git commands from terminal"""
        cmd = command.lower().strip()
        parts = cmd.split()
        
        if not parts:
            self.status()
            return
            
        action = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if action in ["status", "s"]:
            self.status()
            
        elif action in ["add", "a"]:
            files = args[0] if args else "."
            print(self.run_git(f"add {files}"))
            
        elif action in ["commit", "c"]:
            if not args:
                print("Usage: g commit <message>")
                return
            msg = " ".join(args)
            print(self.run_git(f'commit -m "{msg}"'))
            
        elif action in ["push", "p"]:
            print("Pushing...")
            print(self.run_git("push"))
            
        elif action in ["pull", "pl"]:
            print("Pulling...")
            print(self.run_git("pull"))
            
        elif action in ["log", "l"]:
            count = args[0] if args else "5"
            print(self.run_git(f"log --oneline -{count}"))
            
        elif action in ["diff", "d"]:
            print(self.run_git("diff"))
            
        elif action in ["branch", "b"]:
            if args:
                print(self.run_git(f"branch {args[0]}"))
            else:
                print(self.run_git("branch"))
                
        elif action in ["checkout", "co"]:
            if not args:
                print("Usage: g checkout <branch>")
                return
            print(self.run_git(f"checkout {args[0]}"))
            
        elif action in ["repos", "r"]:
            print("\n📚 Known repos:")
            for name, path in self.repos.items():
                marker = " ← current" if name == self.current_repo else ""
                print(f"  {name}: {path}{marker}")
                
        elif action == "use":
            if not args:
                print("Usage: g use <repo_name>")
                return
            if args[0] in self.repos:
                self.current_repo = args[0]
                print(f"Switched to repo: {args[0]}")
            else:
                print(f"Unknown repo: {args[0]}")
                
        elif action == "init":
            if not args:
                print("Usage: g init <path>")
                return
            path = os.path.expanduser(args[0])
            os.makedirs(path, exist_ok=True)
            subprocess.run(f"cd {path} && git init", shell=True)
            print(f"Initialized new repo at: {path}")
            
        else:
            # Pass through to git
            print(self.run_git(cmd))
            
    def quick_save(self, message="Auto-save from Z-Lab"):
        """Quick add, commit, push"""
        self.run_git("add .")
        self.run_git(f'commit -m "{message}"')
        result = self.run_git("push")
        return "Saved and pushed!" if "error" not in result.lower() else result


# Test
if __name__ == "__main__":
    git = GitController()
    git.status()
