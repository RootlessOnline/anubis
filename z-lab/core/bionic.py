#!/usr/bin/env python3
"""
Bionic Reading Module for ADHD Support
======================================
Makes reading easier by highlighting the first part of each word.
This helps ADHD brains focus and read faster.
"""

import re

class BionicReader:
    """
    Bionic Reading implementation for ADHD support
    
    How it works:
    - Highlights the first few letters of each word (bold/color)
    - Your brain fills in the rest automatically
    - Reduces eye strain and improves focus
    """
    
    def __init__(self, enabled=True):
        self.enabled = enabled
        
        # ANSI color codes for terminal
        self.BOLD = '\033[1m'
        self.CYAN = '\033[96m'
        self.YELLOW = '\033[93m'
        self.GREEN = '\033[92m'
        self.RESET = '\033[0m'
        
        # Bionic highlight style
        self.highlight_start = self.BOLD + self.CYAN
        self.highlight_end = self.RESET
        
    def render(self, text):
        """Render text with bionic reading highlights"""
        if not self.enabled:
            return text
            
        words = text.split()
        highlighted = []
        
        for word in words:
            highlighted.append(self._highlight_word(word))
            
        return ' '.join(highlighted)
        
    def _highlight_word(self, word):
        """Highlight the first part of a word"""
        # Skip very short words
        if len(word) <= 2:
            return word
            
        # Skip code blocks and special formatting
        if word.startswith('```') or word.startswith('[') or word.startswith('('):
            return word
        if word.startswith('!') or word.startswith('#'):
            return word
            
        # Calculate how much to highlight (about 40% of word)
        highlight_len = max(1, len(word) // 3)
        
        # Handle punctuation at end
        punctuation = ""
        core_word = word
        
        if word[-1] in '.,!?;:)"]}>':
            punctuation = word[-1]
            core_word = word[:-1]
            highlight_len = max(1, len(core_word) // 3)
            
        # Apply highlight
        if len(core_word) > 1:
            highlighted = (
                self.highlight_start + 
                core_word[:highlight_len] + 
                self.highlight_end + 
                core_word[highlight_len:] + 
                punctuation
            )
        else:
            highlighted = word
            
        return highlighted
        
    def render_box(self, text, style="single"):
        """Render text in a box with bionic reading"""
        lines = text.split('\n')
        max_len = max(len(line) for line in lines)
        
        if style == "double":
            tl, tr, bl, br, h, v = "╔", "╗", "╚", "╝", "═", "║"
        else:
            tl, tr, bl, br, h, v = "┌", "┐", "└", "┘", "─", "│"
            
        top = tl + h * (max_len + 2) + tr
        bottom = bl + h * (max_len + 2) + br
        
        result = [top]
        for line in lines:
            padded = line.ljust(max_len)
            result.append(v + " " + self.render(padded) + " " + v)
        result.append(bottom)
        
        return '\n'.join(result)
        
    def emphasis(self, text, level=1):
        """Add emphasis to important text"""
        if not self.enabled:
            return text
            
        if level == 1:
            return f"{self.BOLD}{text}{self.RESET}"
        elif level == 2:
            return f"{self.BOLD}{self.YELLOW}{text}{self.RESET}"
        else:
            return f"{self.BOLD}{self.GREEN}{text}{self.RESET}"
            
    def dim(self, text):
        """Dim less important text"""
        if not self.enabled:
            return text
        return f"\033[90m{text}{self.RESET}"
        
    def success(self, text):
        """Success message style"""
        if not self.enabled:
            return f"✓ {text}"
        return f"{self.GREEN}✓ {text}{self.RESET}"
        
    def warning(self, text):
        """Warning message style"""
        if not self.enabled:
            return f"⚠ {text}"
        return f"{self.YELLOW}⚠ {text}{self.RESET}"
        
    def error(self, text):
        """Error message style"""
        if not self.enabled:
            return f"✗ {text}"
        return f"\033[91m✗ {text}{self.RESET}"


# Quick test function
def test_bionic():
    """Test bionic reading"""
    br = BionicReader()
    
    test_text = "Hello Q! This is Z-Lab with bionic reading for ADHD support."
    
    print("Normal:")
    print(test_text)
    print()
    print("Bionic:")
    print(br.render(test_text))
    print()
    print("Boxed:")
    print(br.render_box("Z-LAB\nPrivate workspace for Q and Z"))


if __name__ == "__main__":
    test_bionic()
