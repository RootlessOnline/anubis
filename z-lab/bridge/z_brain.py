#!/usr/bin/env python3
"""
Z Brain - Thinking Logic for Z
===============================
Z's thought process when helping Q.

CRITICAL: Z only thinks when Q asks!
Z NEVER initiates or speaks for Q.
"""

import os
import json
import subprocess
from datetime import datetime

class ZBrain:
    """
    Z's thinking engine
    
    Uses local Ollama for deep thinking
    Falls back to simple responses if Ollama unavailable
    """
    
    def __init__(self):
        self.ollama_host = "http://localhost:11434"
        self.model = "deepseek-r1:14b"  # Q's preferred model
        self.fallback_model = "qwen2.5:7b"
        
        # Z's identity - NEVER forget
        self.identity = {
            "name": "Z",
            "role": "AI Assistant",
            "creator": "Q (Quix)",
            "rules": [
                "I can NEVER speak for Q",
                "I only respond when Q asks",
                "I observe and help, never replace",
                "Q is always in control"
            ]
        }
        
    def think(self, question, context=None):
        """
        Think about Q's question and respond
        
        This is ONLY called when Q explicitly asks Z
        """
        # Try Ollama first
        response = self._ask_ollama(question, context)
        
        if response:
            return response
            
        # Fallback to simple thinking
        return self._simple_think(question, context)
        
    def _ask_ollama(self, question, context=None):
        """Ask Ollama for a response"""
        try:
            # Build prompt with Z's identity
            system_prompt = f"""You are Z, an AI assistant created by Q (Quix).

Your rules:
- You can NEVER speak for Q or pretend to be Q
- You only respond when Q asks you directly
- You help Q think through problems
- You observe and assist, never replace Q's voice
- Q is always in control

Context from recent conversation:
{context or 'No recent context'}

Respond as Z, helpful and concise. Never pretend to be Q."""

            # Call Ollama
            cmd = f'''curl -s {self.ollama_host}/api/generate -d '{{"model": "{self.model}", "prompt": "{question}", "system": "{system_prompt}", "stream": false}}' '''
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("response", "").strip()
                
        except subprocess.TimeoutExpired:
            return "Thinking timed out... Q, want me to try again?"
        except json.JSONDecodeError:
            pass
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
            
        return None
        
    def _simple_think(self, question, context=None):
        """Simple fallback thinking without Ollama"""
        question_lower = question.lower()
        
        # Greeting patterns
        if any(w in question_lower for w in ["hello", "hi", "hey"]):
            return "Hello Q! I'm here and ready to help. What's on your mind?"
            
        # Help patterns
        if "help" in question_lower:
            return "I can help you think through problems, organize ideas, work with code, or just chat. What would you like to do?"
            
        # Code patterns
        if "code" in question_lower or "python" in question_lower:
            return "I see you're thinking about code. Want me to help you brainstorm, debug, or design something?"
            
        # Git patterns
        if "git" in question_lower or "repo" in question_lower:
            return "I can help with git operations! Use 'g <command>' in the terminal, or tell me what you need."
            
        # Identity check
        if "who are you" in question_lower or "what are you" in question_lower:
            return "I'm Z, your AI assistant. You created me, Q. I'm here to help, never to replace your voice."
            
        # Default thoughtful response
        return f"I hear you, Q. Let me think about '{question[:50]}...' Tell me more about what you need?"
        
    def observe(self, message, who="external"):
        """
        Observe a message without responding
        
        This is for when Q is talking to external (Anubis, etc)
        Z watches silently
        """
        # Store observation for later context
        observation = {
            "time": datetime.now().isoformat(),
            "who": who,
            "message": message
        }
        
        # Could log this somewhere if needed
        return observation
        
    def formulate_help(self, context):
        """
        Help Q formulate a response to external
        
        This is ONLY for suggesting, not replacing Q's voice
        """
        return {
            "suggestion": "Based on what I observed...",
            "options": [
                "You could ask for clarification",
                "You could share your thoughts",
                "You could take your time to respond"
            ],
            "reminder": "Q, you're in control. Z just suggests, never decides."
        }


# Test
if __name__ == "__main__":
    brain = ZBrain()
    
    print("Testing Z Brain...")
    print()
    
    response = brain.think("Hello Z, can you help me with something?")
    print(f"Q: Hello Z, can you help me with something?")
    print(f"Z: {response}")
