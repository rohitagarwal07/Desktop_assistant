# 🤖 AI Desktop Assistant
### 100% Free  •  100% Local  •  No API Keys  •  No Internet

A background AI assistant for Windows that talks like a human, executes desktop tasks,
and remembers up to **20 records** using **LlamaIndex + local embeddings**.

---

## 🏗️ Tech Stack (all free & local)

| Component | Technology | Cost |
|---|---|---|
| 🧠 LLM (AI brain) | **Ollama** — runs Llama 3, Mistral, Phi-3 locally | Free |
| 💾 Memory index | **LlamaIndex** + sentence-transformers embeddings | Free |
| 🔊 Voice output | **pyttsx3** → Windows SAPI5 (built into Windows) | Free |
| 🎙️ Voice input | **SpeechRecognition** + **Vosk** (offline) | Free |
| 🖥️ System tray | **pystray** | Free |
| ⌨️ Hotkeys | **keyboard** library | Free |

**Nothing phones home. Everything runs on your PC.**

---

## 🚀 Setup (Windows)

### Step 1 — Install Python 3.10+
Download from: https://www.python.org/downloads/  
✅ Check "Add Python to PATH" during install.

### Step 2 — Install Ollama
Download from: **https://ollama.com/download** (Windows installer)

After installing, open a terminal and pull a model:
```cmd
ollama pull llama3
```
> Other free models: `ollama pull mistral` | `ollama pull phi3` | `ollama pull gemma2`  
> Llama 3 (~4GB) is the best balance of speed and quality.

### Step 3 — Build the EXE
Double-click **`build_windows.bat`**

This will:
1. Install all Python packages
2. Pull the Llama 3 model (if not already done)
3. Build `dist\AIAssistant.exe`

### Step 4 — Run
```
dist\AIAssistant.exe
```

> **Before running**: Make sure Ollama is running in the background.  
> Open a terminal and run: `ollama serve`

The assistant starts silently. Look for the 🟣 icon in your system tray.

---

## ⌨️ Controls

| Action | How |
|---|---|
| Toggle voice on/off | **Ctrl + Alt + A** |
| Open chat window | Left-click tray icon |
| View memory | Right-click → Show Memory |
| Check status | Right-click → Status |
| Quit | Right-click → Quit |

---

## 🗣️ What You Can Say

### Open Applications
> "Open Notepad"  
> "Launch Chrome"  
> "Open Calculator"  
> "Start File Explorer"  
> "Open Terminal"  
> "Open PowerShell"

### Web Search
> "Search for Python tutorials"  
> "Look up the weather in Delhi"  
> "Google latest news"

### Memory (LlamaIndex — max 20 records)
> "Remember that my meeting is at 3pm Friday"  
> "Save that the WiFi password is abc123"  
> "Note that I need to call Rahul tomorrow"  
> "What do you remember?"  
> "Show my notes"  
> "Forget everything"

### Timed Reminders
> "Remind me to drink water in 30 minutes"  
> "Remind me to check email in 2 hours"  
> "Remind me to take medicine in 45 minutes"

### System
> "What time is it?"  
> "What's today's date?"  
> "Take a screenshot"  
> "Mute"  
> "Volume up"

### General AI Conversation
> Anything else → goes to Ollama (Llama 3 running locally)

---

## 🧠 Memory System (LlamaIndex)

- **Engine**: LlamaIndex with `all-MiniLM-L6-v2` embeddings (runs on CPU)
- **Max records**: 20 (oldest dropped automatically when full)
- **Search**: Semantic vector search — finds relevant memories even with different wording
- **Persistence**: Saved to `C:\Users\<you>\.ai_assistant\memory\`
- **Fallback**: Plain JSON keyword search if LlamaIndex is unavailable

---

## 🔇 Fully Offline STT (Optional — No Internet for Voice)

By default, voice recognition uses Google's online service as fallback.  
For **fully offline** voice (no internet needed at all):

1. Install Vosk: `pip install vosk`
2. Download an English model from: https://alphacephei.com/vosk/models
   - Recommended: `vosk-model-en-us-0.22` (~1.8GB, accurate)
   - Or light: `vosk-model-small-en-us-0.15` (~40MB, faster)
3. Extract the folder to: `C:\Users\<you>\.ai_assistant\vosk_model\`

The assistant automatically uses Vosk if the folder exists.

---

## 🔄 Changing the AI Model

Edit `C:\Users\<you>\.ai_assistant\config.json`:
```json
{
  "ollama_model": "mistral",
  "tts_rate": 170,
  "max_memory": 20
}
```

Available models (run `ollama list` to see installed ones):
- `llama3` — Best quality (~4GB)
- `mistral` — Fast, good quality (~4GB)  
- `phi3` — Very fast, smaller (~2GB)
- `gemma2` — Google's model (~5GB)

---

## 🔧 Auto-Start with Windows

Run **`install_startup.bat`** — adds the EXE to Windows startup registry.  
No admin needed.

---

## 📁 Files

```
ai_assistant/
├── main.py                  ← Entry point
├── build_windows.bat        ← One-click build
├── install_startup.bat      ← Windows auto-start
├── requirements.txt         ← Python packages
├── assistant.spec           ← PyInstaller EXE config
├── version_info.txt         ← EXE metadata
├── core/
│   ├── assistant.py         ← AI brain (Ollama + LlamaIndex memory)
│   ├── tray.py              ← System tray icon
│   ├── hotkey_listener.py   ← Ctrl+Alt+A hotkey
└── ui/
    └── chat_window.py       ← Dark chat GUI (Tkinter)
```

**Memory & config stored at:** `C:\Users\<you>\.ai_assistant\`

---

## ❓ Troubleshooting

**"Ollama isn't responding"**  
→ Open a terminal and run: `ollama serve`  
→ Leave it running in the background.

**PyAudio fails to install:**
```cmd
pip install pipwin
pipwin install pyaudio
```

**No voice output:**
```cmd
python -c "import pyttsx3; e=pyttsx3.init(); e.say('Hello'); e.runAndWait()"
```

**LlamaIndex slow on first run:**  
→ It's downloading the `all-MiniLM-L6-v2` model (~90MB). Only happens once.

---

*Everything on your PC. No data leaves your machine.*
