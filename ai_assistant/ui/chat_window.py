"""
Dark-themed chat window (Tkinter — built into Python, no extra install).
Click the tray icon to open. Type or click  to speak.
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import logging

logger = logging.getLogger(__name__)


class ChatWindow:
    def __init__(self, assistant):
        self.assistant = assistant
        self.root = None
        self._open = False

    def show(self):
        if self._open and self.root:
            self.root.lift()
            self.root.focus_force()
            return
        threading.Thread(target=self._build, daemon=True, name="ChatUI").start()

    def _build(self):
        self._open = True
        self.root = tk.Tk()
        self.root.title("AI Assistant  — Local & Free")
        self.root.geometry("500x640")
        self.root.configure(bg="#0D0D1A")
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.attributes("-topmost", False)

        # ── Header ──────────────────────────────────────────────────────
        hdr = tk.Frame(self.root, bg="#1E1333", pady=10)
        hdr.pack(fill=tk.X)
        tk.Label(
            hdr, text=" AI Assistant  •  100% Local",
            font=("Segoe UI", 13, "bold"), fg="#C4B5FD", bg="#1E1333"
        ).pack(side=tk.LEFT, padx=16)
        self._status_var = tk.StringVar(value="● Ready")
        tk.Label(
            hdr, textvariable=self._status_var,
            font=("Segoe UI", 9), fg="#6EE7B7", bg="#1E1333"
        ).pack(side=tk.RIGHT, padx=16)

        # ── Chat log ────────────────────────────────────────────────────
        self.log = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED,
            bg="#0D0D1A", fg="#E5E7EB",
            font=("Segoe UI", 10), relief=tk.FLAT,
            bd=0, padx=12, pady=10,
            selectbackground="#3730A3",
        )
        self.log.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 2))

        self.log.tag_config("you",    foreground="#60A5FA", font=("Segoe UI", 10, "bold"))
        self.log.tag_config("ai",     foreground="#C4B5FD")
        self.log.tag_config("sys",    foreground="#4B5563", font=("Segoe UI", 8, "italic"))
        self.log.tag_config("err",    foreground="#F87171")

        self._print("sys", "Chat with your local AI. Everything runs on your PC.\n")
        llm_ok = self.assistant.llm._available
        if not llm_ok:
            self._print("err",
                "  Ollama is not running. Basic commands work, but full AI needs Ollama.\n"
                "    Start it: open a terminal and run:  ollama serve\n"
                f"   Then pull a model:  ollama pull {self.assistant.llm.model}\n"
            )

        # ── Memory bar ──────────────────────────────────────────────────
        mem_bar = tk.Frame(self.root, bg="#1E1333", pady=3)
        mem_bar.pack(fill=tk.X)
        self._mem_var = tk.StringVar()
        self._refresh_mem_label()
        tk.Label(
            mem_bar, textvariable=self._mem_var,
            font=("Segoe UI", 8), fg="#7C3AED", bg="#1E1333"
        ).pack(side=tk.LEFT, padx=12)

        # ── Input row ───────────────────────────────────────────────────
        row = tk.Frame(self.root, bg="#1E1333", pady=8, padx=8)
        row.pack(fill=tk.X)

        self.var = tk.StringVar()
        self.entry = tk.Entry(
            row, textvariable=self.var,
            bg="#2D1F4E", fg="#E5E7EB",
            insertbackground="#C4B5FD",
            font=("Segoe UI", 11),
            relief=tk.FLAT, bd=0,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=7, padx=(0, 6))
        self.entry.bind("<Return>", lambda e: self._send())
        self.entry.focus_set()

        tk.Button(
            row, text=" ", command=self._mic,
            bg="#4C1D95", fg="white", font=("Segoe UI", 12),
            relief=tk.FLAT, bd=0, padx=10, cursor="hand2",
            activebackground="#5B21B6",
        ).pack(side=tk.LEFT, padx=(0, 4))

        tk.Button(
            row, text="Send  ➤", command=self._send,
            bg="#5B21B6", fg="white", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, bd=0, padx=14, cursor="hand2",
            activebackground="#6D28D9",
        ).pack(side=tk.LEFT)

        self.root.mainloop()
        self._open = False

    # ── Helpers ────────────────────────────────────────────────────────────
    def _print(self, tag: str, text: str):
        prefix = {"you": "You: ", "ai": "AI:  ", "sys": "", "err": ""}.get(tag, "")
        self.log.config(state=tk.NORMAL)
        if prefix:
            self.log.insert(tk.END, prefix, tag)
        self.log.insert(tk.END, text + "\n")
        self.log.config(state=tk.DISABLED)
        self.log.see(tk.END)

    def _refresh_mem_label(self):
        n = self.assistant.memory.count()
        from core.assistant import CONFIG
        self._mem_var.set(f" Memory: {n} / {CONFIG['max_memory']} records")

    def _send(self):
        text = self.var.get().strip()
        if not text:
            return
        self.var.set("")
        self._print("you", text)
        self._status_var.set("Thinking...")
        threading.Thread(target=self._respond, args=(text,), daemon=True).start()

    def _mic(self):
        self._status_var.set("● Listening...")
        def go():
            heard = self.assistant.listen_once()
            if heard:
                if self.root:
                    self.root.after(0, self._print, "you", heard)
                self._respond(heard)
            else:
                if self.root:
                    self.root.after(0, self._status_var.set, " Ready")
                    self.root.after(0, self._print, "sys", "(nothing heard — try again)")
        threading.Thread(target=go, daemon=True).start()

    def _respond(self, text: str):
        reply = self.assistant.process_command(text)
        if self.root:
            self.root.after(0, self._print, "ai", reply)
            self.root.after(0, self._status_var.set, "● Ready")
            self.root.after(0, self._refresh_mem_label)
        self.assistant.speak(reply)

    def _on_close(self):
        self._open = False
        self.root.destroy()
        self.root = None
