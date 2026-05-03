# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec — builds single-file Windows EXE
# Run: pyinstaller assistant.spec --clean --noconfirm

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets/*',  'assets'),
    ],
    hiddenimports=[
        # LlamaIndex
        'llama_index.core',
        'llama_index.core.storage',
        'llama_index.core.storage.docstore',
        'llama_index.core.storage.index_store',
        'llama_index.core.vector_stores',
        'llama_index.llms.ollama',
        'llama_index.embeddings.huggingface',
        # Sentence transformers
        'sentence_transformers',
        'transformers',
        'torch',
        # Speech
        'pyttsx3',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'speech_recognition',
        'pyaudio',
        'vosk',
        # Tray / UI
        'pystray',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        # System
        'keyboard',
        'psutil',
        'requests',
        'mss',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['openai', 'anthropic', 'tkinter.test'],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AIAssistant',
    debug=False,
    strip=False,
    upx=True,
    console=False,           # Silent — no console window
    icon='assets/icon.ico',
    version='version_info.txt',
)
