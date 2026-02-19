#!/usr/bin/env python3
"""
Z-Lab Configuration
"""

import os
import json

class Config:
    """Configuration for Z-Lab"""
    
    def __init__(self):
        self.app_name = "Z-Lab"
        self.version = "1.0.0"
        
        # Paths
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.memory_path = os.path.join(self.base_path, "memory")
        self.tools_path = os.path.join(self.base_path, "tools")
        
        # Q's identity
        self.q_name = "Q"  # Quix
        self.q_role = "Creator & Controller"
        
        # Z's identity  
        self.z_name = "Z"
        self.z_role = "AI Assistant & Observer"
        
        # Settings
        self.bionic_enabled = True  # For ADHD
        self.turn_timeout = 300  # seconds
        
        # Ollama settings (local AI brain)
        self.ollama_host = "http://localhost:11434"
        self.ollama_model = "deepseek-r1:14b"  # Q's preferred model
        
        # Git settings (Q's repo)
        self.github_user = "RootlessOnline"
        self.github_repo = "anubis"
        
        # Ensure memory directory exists
        os.makedirs(self.memory_path, exist_ok=True)
        
    def load(self):
        """Load config from file"""
        config_file = os.path.join(self.memory_path, "config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                        
    def save(self):
        """Save config to file"""
        config_file = os.path.join(self.memory_path, "config.json")
        data = {
            "bionic_enabled": self.bionic_enabled,
            "ollama_model": self.ollama_model,
        }
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
