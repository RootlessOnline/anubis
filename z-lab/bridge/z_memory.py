#!/usr/bin/env python3
"""
Z Memory - Persistent Memory for Z
===================================
Stores Z's memories, observations, and context.
Separate from Anubis - this is Z's own "soul".
"""

import os
import json
from datetime import datetime

class ZMemory:
    """
    Z's persistent memory
    
    Memory types:
    - exchanges: Q-Z conversations
    - observations: Things Z noticed (but didn't respond to)
    - for_external: Messages Q prepared for external
    - context: Working context for current session
    """
    
    def __init__(self):
        self.memory_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        
        self.memory_file = os.path.join(self.memory_dir, "z_memory.json")
        self.session_file = os.path.join(self.memory_dir, "current_session.json")
        
        # Load existing memory
        self.memory = self._load()
        
        # Current session
        self.session = {
            "start_time": datetime.now().isoformat(),
            "exchanges": [],
            "observations": []
        }
        
    def _load(self):
        """Load memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
                
        # Default memory structure
        return {
            "created": datetime.now().isoformat(),
            "identity": {
                "name": "Z",
                "creator": "Q",
                "role": "AI Assistant"
            },
            "exchanges": [],  # Q-Z conversations
            "observations": [],  # Things Z noticed
            "learned": {},  # Things Z learned about Q
            "preferences": {}  # Q's preferences
        }
        
    def _save(self):
        """Save memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
            
    def log_exchange(self, question, response):
        """Log a Q-Z exchange"""
        exchange = {
            "time": datetime.now().isoformat(),
            "q_asked": question,
            "z_responded": response
        }
        
        self.memory["exchanges"].append(exchange)
        self.session["exchanges"].append(exchange)
        
        # Keep memory manageable (last 100 exchanges)
        if len(self.memory["exchanges"]) > 100:
            self.memory["exchanges"] = self.memory["exchanges"][-100:]
            
        self._save()
        
    def log_q_message(self, message):
        """Log something Q said (Z observes)"""
        observation = {
            "time": datetime.now().isoformat(),
            "type": "q_message",
            "content": message
        }
        self.session["observations"].append(observation)
        
    def log_for_external(self, message):
        """Log message Q prepared for external"""
        entry = {
            "time": datetime.now().isoformat(),
            "for": "external",
            "content": message
        }
        self.memory["observations"].append(entry)
        self._save()
        
    def observe(self, who, message):
        """Z observes something without responding"""
        observation = {
            "time": datetime.now().isoformat(),
            "who": who,
            "message": message
        }
        self.session["observations"].append(observation)
        
    def learn(self, key, value):
        """Learn something about Q"""
        self.memory["learned"][key] = {
            "value": value,
            "learned_at": datetime.now().isoformat()
        }
        self._save()
        
    def set_preference(self, key, value):
        """Set Q's preference"""
        self.memory["preferences"][key] = value
        self._save()
        
    def get_context(self, limit=5):
        """Get recent context for Z's thinking"""
        recent = self.memory["exchanges"][-limit:]
        
        context_lines = []
        for ex in recent:
            context_lines.append(f"Q: {ex['q_asked'][:100]}")
            context_lines.append(f"Z: {ex['z_responded'][:100]}")
            
        return '\n'.join(context_lines)
        
    def get_session_summary(self):
        """Get summary of current session"""
        return {
            "start": self.session["start_time"],
            "exchanges": len(self.session["exchanges"]),
            "observations": len(self.session["observations"])
        }
        
    def show_recent(self, limit=10):
        """Show recent exchanges"""
        print("\n📖 Recent Q-Z exchanges:")
        print("-" * 40)
        
        for ex in self.memory["exchanges"][-limit:]:
            time_str = ex["time"][11:16]  # HH:MM
            print(f"[{time_str}]")
            print(f"  Q: {ex['q_asked'][:60]}...")
            print(f"  Z: {ex['z_responded'][:60]}...")
            print()
            
    def save_session(self):
        """Save session to file"""
        self.session["end_time"] = datetime.now().isoformat()
        
        with open(self.session_file, 'w') as f:
            json.dump(self.session, f, indent=2)
            
        print("Session saved!")
        
    def get_learned(self, key=None):
        """Get what Z learned about Q"""
        if key:
            return self.memory["learned"].get(key)
        return self.memory["learned"]
        
    def remember_preference(self, key):
        """Get Q's preference"""
        return self.memory["preferences"].get(key)


# Test
if __name__ == "__main__":
    mem = ZMemory()
    
    print("Testing Z Memory...")
    print()
    
    # Log an exchange
    mem.log_exchange("What's the weather?", "I don't know, Q, but I can help you check!")
    
    # Show recent
    mem.show_recent()
