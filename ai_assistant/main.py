import sys
import os
import threading
import logging
from pathlib import Path

# ── Logging ────────────────────────────────────────────────────────────────
DATA_DIR = Path.home() / ".ai_assistant"
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler(DATA_DIR / "assistant.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.assistant import AIAssistant
from core.tray import TrayApp
from core.hotkey_listener import HotkeyListener


def main():
    logger.info("=" * 60)
    logger.info("  AI Desktop Assistant starting (100%% local / free)")
    logger.info("=" * 60)

    assistant = AIAssistant()

    # Hotkey thread (Ctrl+Alt+A)
    hotkey = HotkeyListener(assistant)
    threading.Thread(target=hotkey.listen, daemon=True, name="Hotkey").start()

    # Voice loop thread
    threading.Thread(target=assistant.start_voice_listener, daemon=True, name="VoiceLoop").start()

    logger.info("All background threads started.")
    logger.info("Hotkey: Ctrl+Alt+A  |  Tray: right-click for menu")

    # Tray is blocking — keeps process alive
    TrayApp(assistant).run()


if __name__ == "__main__":
    main()
