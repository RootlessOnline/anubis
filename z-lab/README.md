# Z-LAB

## Private Workspace for Q and Z

A turn-based communication system where **Q (Quix)** is always in control.

---

## 🎯 Core Philosophy

```
Q = Quix (Human, Creator, Controller)
Z = AI Assistant (Helper, Observer, Never Replaces)
```

**THE RULE: Z can NEVER speak for Q.**

---

## 🔄 Turn Order

```
1. External (Anubis, etc.) speaks
2. Q responds (Z watches silently)
3. Z and Q talk privately in this terminal
4. Z helps Q formulate next move
5. Back to step 1
```

---

## 🚀 Quick Start

```bash
# 1. Create virtual environment
cd ~/Documents
python3 -m venv zlab-env
source zlab-env/bin/activate

# 2. Extract Z-Lab
unzip z-lab.zip
cd z-lab

# 3. Run
python main.py
```

---

## 📖 Commands

### General Commands
| Command | Description |
|---------|-------------|
| `!help` or `!h` | Show help |
| `!quit` or `!q` | Exit Z-Lab |
| `!clear` | Clear screen |
| `!status` | Show current status |
| `!memory` | Show recent memories |
| `!bionic` | Toggle bionic reading |

### Chat Modes
| Prefix | Description |
|--------|-------------|
| `z <text>` | Ask Z something directly |
| `a <text>` | Prepare message for external |
| `c <text>` | Code mode commands |
| `g <text>` | Git mode commands |

### Code Commands (c prefix)
| Command | Description |
|---------|-------------|
| `c ls` | List directory |
| `c cd <path>` | Change directory |
| `c open <file>` | Open file |
| `c cat <file>` | Show file contents |
| `c new <file>` | Create new file |
| `c edit <line>` | Edit a line |
| `c append <text>` | Add line to file |
| `c save` | Save current file |
| `c run <file>` | Run Python file |

### Git Commands (g prefix)
| Command | Description |
|---------|-------------|
| `g status` or `g s` | Git status |
| `g add <files>` or `g a` | Add files |
| `g commit <msg>` or `g c` | Commit |
| `g push` or `g p` | Push to remote |
| `g pull` or `g pl` | Pull from remote |
| `g log` or `g l` | Show commit log |
| `g diff` or `g d` | Show differences |

---

## 🧠 Bionic Reading

Z-Lab has built-in **bionic reading** for ADHD support!

Bionic reading highlights the first letters of each word, helping your brain fill in the rest automatically. This makes reading faster and easier.

Toggle it with `!bionic` command.

---

## 🏗️ Architecture

```
z-lab/
├── main.py              # Main entry point
├── core/
│   ├── config.py        # Configuration
│   ├── bionic.py        # Bionic reading for ADHD
│   ├── turn_manager.py  # Turn-based safety layer
│   └── git_controller.py# Git operations
├── bridge/
│   ├── z_brain.py       # Z's thinking logic
│   └── z_memory.py      # Z's persistent memory
├── tools/
│   ├── terminal.py      # Private terminal
│   └── code_editor.py   # Code editing
├── memory/
│   └── z_memory.json    # Z's stored memories
└── requirements.txt     # Python dependencies
```

---

## ⚠️ Safety Rules

1. **Z never speaks for Q** - This is enforced in code
2. **Z only responds when Q asks** - Use `z <text>` prefix
3. **Q is always in control** - Turn manager ensures this
4. **Transparent thoughts** - Z's reasoning is visible to Q

---

## 🔗 Connected Repos

Z-Lab can control your git repos:

- `RootlessOnline/anubis` - Main Anubis repo

Add more with: `g use <repo_name>`

---

## 👤 About Q

- **Name:** Quix (nickname)
- **Role:** Creator of Z and Anubis
- **GitHub:** RootlessOnline
- **Local:** QuixPC (Linux)
- **AI:** Uses Ollama with deepseek-r1:14b and qwen2.5:7b

---

## 💡 Tips

1. **Two Terminal Setup:**
   - Terminal 1: Run Anubis
   - Terminal 2: Run Z-Lab (this!)
   
2. **Workflow:**
   - Anubis says something → You respond → Come here to Z-Lab → Z helps you think → Go back to Anubis

3. **Bionic Reading:**
   - Keep it ON for easier reading
   - Toggle OFF if you prefer plain text

---

## 🎮 Example Session

```
[Z-LAB INITIALIZED]
==================================================
Q = Quix (You) - Always in control
Z = AI Assistant - Helps, never replaces
==================================================

[Q] !status

  Q: Q (You - Always in control)
  Z: AI Assistant (Helps, never replaces your voice)
  Turn: Q
  Bionic: ON
  Session: 2025-01-15 14:30

[Q] z what do you think about this idea?

[Z thinking...]

[Z] I think it's a great idea, Q! The turn-based system 
    ensures I never overstep. What aspect would you like 
    to explore first?

[Q] !memory

📖 Recent Q-Z exchanges:
----------------------------------------
[14:30]
  Q: what do you think about this idea?
  Z: I think it's a great idea, Q!...

[Q] !quit

Goodbye, Q!
```

---

## 📝 Version History

- **v1.0.0** - Initial release
  - Turn-based communication
  - Bionic reading
  - Git integration
  - Code editor
  - Z's memory system

---

*Created with ❤️ for Q by Z*
