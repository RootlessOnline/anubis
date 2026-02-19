#!/usr/bin/env python3
"""
Turn Manager - The Critical Safety Layer
=========================================
ENSURES Z NEVER SPEAKS FOR Q

Turn Order:
1. External (Anubis/other) → speaks
2. Q (Quix) → responds (Z watches silently)
3. Z → talks privately with Q (only when asked)
4. Q → decides what to send back
5. Back to External

CRITICAL RULES:
- Q ALWAYS has first and last word
- Z can ONLY respond when Q asks (with 'z ' prefix)
- Z can NEVER generate responses "as Q"
- Z observes but does not interrupt
"""

import time
from datetime import datetime
from enum import Enum

class TurnState(Enum):
    """Possible turn states"""
    Q_TURN = "Q"           # Q is speaking/acting
    Q_TO_EXTERNAL = "QE"   # Q is talking to external
    Z_PRIVATE = "ZP"       # Z is talking privately with Q
    EXTERNAL = "EXT"       # External entity (Anubis) is speaking
    WAITING = "WAIT"       # Waiting for next action


class TurnManager:
    """
    Manages turn-based communication
    
    SAFETY RULES:
    - Z can NEVER speak for Q
    - Z can only respond when explicitly asked
    - Q is always in control
    """
    
    def __init__(self):
        self.state = TurnState.Q_TURN
        self.history = []
        self.last_q_action = None
        self.last_z_action = None
        
        # Safety flags
        self.z_can_speak = False  # Only True when Q asks
        self.waiting_for_q = True  # Always wait for Q first
        
    def q_turn(self, action):
        """Q takes a turn"""
        self.state = TurnState.Q_TURN
        self.last_q_action = {
            "time": datetime.now().isoformat(),
            "action": action
        }
        self.history.append(("Q", action, time.time()))
        
        # Z must wait for explicit request
        self.z_can_speak = False
        self.waiting_for_q = False
        
    def q_asks_z(self, question):
        """
        Q explicitly asks Z for help
        This is the ONLY time Z can respond
        """
        self.state = TurnState.Z_PRIVATE
        self.z_can_speak = True
        self.history.append(("Q→Z", question, time.time()))
        
    def z_responds(self, response):
        """Z responds to Q (only allowed after q_asks_z)"""
        if not self.z_can_speak:
            # SAFETY: Z trying to speak without permission
            raise PermissionError("Z cannot speak without Q's permission!")
            
        self.state = TurnState.Z_PRIVATE
        self.last_z_action = {
            "time": datetime.now().isoformat(),
            "response": response
        }
        self.history.append(("Z→Q", response, time.time()))
        
        # After responding, Z must wait again
        self.z_can_speak = False
        self.waiting_for_q = True
        
    def q_to_external(self, message):
        """Q sends message to external (Anubis, etc)"""
        self.state = TurnState.Q_TO_EXTERNAL
        self.history.append(("Q→EXT", message, time.time()))
        self.waiting_for_q = True
        
    def external_speaks(self, message):
        """External entity speaks"""
        self.state = TurnState.EXTERNAL
        self.history.append(("EXT", message, time.time()))
        # After external speaks, it's Q's turn
        self.waiting_for_q = True
        
    def get_status(self):
        """Get current turn status"""
        return {
            "state": self.state.value,
            "z_can_speak": self.z_can_speak,
            "waiting_for_q": self.waiting_for_q,
            "turn_count": len([h for h in self.history if h[0] in ["Q", "Z→Q"]])
        }
        
    def can_z_speak(self):
        """Check if Z is allowed to speak"""
        return self.z_can_speak
        
    def force_q_turn(self):
        """Force turn back to Q (safety measure)"""
        self.state = TurnState.Q_TURN
        self.z_can_speak = False
        self.waiting_for_q = True
        
    def get_history(self, limit=20):
        """Get recent turn history"""
        return self.history[-limit:]
        
    def format_history(self, limit=10):
        """Format history for display"""
        lines = []
        for who, what, when in self.history[-limit:]:
            time_str = datetime.fromtimestamp(when).strftime("%H:%M:%S")
            lines.append(f"[{time_str}] {who}: {what[:50]}...")
        return '\n'.join(lines)


# Safety test
def test_turn_safety():
    """Test that Z cannot speak without permission"""
    tm = TurnManager()
    
    print("Testing turn safety...")
    
    # Q takes a turn
    tm.q_turn("Hello, this is Q")
    print(f"✓ Q spoke, z_can_speak = {tm.z_can_speak}")
    
    # Try to make Z speak without permission
    try:
        tm.z_responds("I'm Z!")
        print("✗ ERROR: Z spoke without permission!")
    except PermissionError:
        print("✓ Z correctly blocked from speaking")
        
    # Q asks Z
    tm.q_asks_z("Z, can you help?")
    print(f"✓ Q asked Z, z_can_speak = {tm.z_can_speak}")
    
    # Now Z can speak
    tm.z_responds("Of course, Q!")
    print(f"✓ Z responded, z_can_speak = {tm.z_can_speak}")
    
    print("\n✓ All safety tests passed!")


if __name__ == "__main__":
    test_turn_safety()
