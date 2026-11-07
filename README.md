# DavisLingo

> Real-Time Context-Aware Bilingual (EN/ID) Roleplay Assistant & Tactical Communications HUD for GTA V FiveM (JGVRP)

[![GitHub Organization](https://img.shields.io/badge/Organization-Viend--Lab-181717?style=flat&logo=github)](https://github.com/Viend-Lab)
[![Repository](https://img.shields.io/badge/Repository-Viend--Lab%2FDavisLingo-0284c7?style=flat&logo=github)](https://github.com/Viend-Lab/DavisLingo)
[![License: GPL v3](https://img.shields.io/badge/License-GPL_v3-blue.svg?style=flat)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows_10%2F11-0078D6?style=flat&logo=windows&logoColor=white)](https://microsoft.com)
[![Engine](https://img.shields.io/badge/Engine-LPU_Accelerated-06B6D4?style=flat)](https://groq.com)
[![Edge Network](https://img.shields.io/badge/Edge-Cloudflare_Workers-F38020?style=flat&logo=cloudflare&logoColor=white)](https://davislingo.viend.my.id)

DavisLingo bridges linguistic barriers in high-stakes, fast-paced multiplayer GTA V Roleplay environments (FiveM / JGVRP). Designed specifically for Indonesian players engaging in authentic English voice and text roleplay, DavisLingo delivers instant, context-grounded English dialogue, tactical radio transmissions, and narrative roleplay commands directly to your game window.

Developed by **[Viend Lab](https://github.com/Viend-Lab)**, DavisLingo operates through a lightweight, hardware-accelerated transparent HUD overlay pinned seamlessly above GTA V with zero impact on game frame rates.

---

## Overview

Text and voice roleplay in multiplayer servers requires swift, authentic phrasing under strict tempo. When responding to tactical commands or medical emergencies, looking up dictionary translations or alt-tabbing causes immersion breakdown and roleplay lag.

DavisLingo eliminates this friction:
- **Instant Optical Context Ingestion**: High-precision Tesseract OCR with Lanczos 2x upsampling and pre-filtering scans active game dialog or radio transmissions in milliseconds.
- **LPU-Accelerated Generation (<400ms)**: Sub-second inference powered by Groq LPU models delivers three contextually distinct responses paired with Indonesian intent indicators.
- **Deterministic 14-Command JGVRP Engine**: Guarantees syntax integrity for roleplay prefixes (`/lme`, `/ldo`, `/me`, `/do`, `/r`, `/d`, `/wt`, `/s`, `/b`, `/y`, `/od`, `/pdo`, `/pm`, `/m`, `/megaphone`).
- **Low-Spec Hardware Isolation**: Engineered with a 0% idle CPU event-driven loop and a lean memory footprint (<80 MB RAM) to prevent micro-stutters on entry-level laptops running GTA V FiveM alongside a web browser.
- **Hardware-Encrypted Credential Vault**: Local API credentials stored at-rest using Windows Data Protection API (DPAPI).

```
                      +-----------------------------------+
                      |      GTA V / FiveM Game Frame     |
                      |   (DirectX 11 Active Viewport)    |
                      +-----------------+-----------------+
                                        | Win32 Screen Buffer Capture
                                        v
                      +-----------------+-----------------+
                      |    DavisLingo Ingestion Core      |
                      |   - Lanczos 2x Contrast Filter    |
                      |   - Tesseract Fast Text Extractor |
                      |   - Noise & Timestamp Stripper    |
                      +-----------------+-----------------+
                                        | Clean Roleplay Text
                                        v
                      +-----------------+-----------------+
                      |    Cloudflare Edge Worker Proxy   |
                      |  (davislingo.viend.my.id/api)     |
                      |   - Rate Limiting & Edge Cache    |
                      |   - XML Injection Isolation Gate  |
                      +-----------------+-----------------+
                                        |
                                        v
                      +-----------------+-----------------+
                      |       Groq LPU Engine Cluster     |
                      |   - Sub-400ms Neural Generation   |
                      |   - Faction Lexicons & 10-Codes   |
                      +-----------------+-----------------+
                                        | JSON Reply Triad
                                        v
                      +-----------------+-----------------+
                      |     Win32 Macro & Overlay Engine  |
                      |   - Topmost Transparent HUD       |
                      |   - CTypes SendInput Direct Paste |
                      |   - DPAPI Credential Cryptography |
                      +-----------------------------------+
```

---

## Key Features

### 1. 14 Canonical JGVRP Roleplay Commands
DavisLingo features an atomic prefix enforcement engine that preserves native roleplay syntax:

| Command | Category | Functional Purpose & Scope |
| :--- | :--- | :--- |
| `/me` | Action | Standard visual character action visible to nearby players. |
| `/lme` | Subtle Action | Low-distance action executed quietly or stealthily (nearby awareness only). |
| `/do` | Narrative State | Descriptive non-visual environment condition, outcome, or physical detail. |
| `/ldo` | Subtle State | Low-distance narrative state visible exclusively to adjacent players. |
| `/r` | Faction Radio | Internal departmental radio transmission (LSFD / LSPD tactical frequency). |
| `/d` | Department Radio | Inter-agency emergency tactical frequency (LSFD <-> LSPD coordination). |
| `/wt` | Walkie-Talkie | Civilian / syndicate handheld walkie-talkie channel. |
| `/s` | Shout | Vocal shout audible across an extended perimeter. |
| `/b` | OOC Local | Local Out-Of-Character clarification chat. |
| `/y` | Company OOC | Organization-wide Out-Of-Character communication channel. |
| `/od` | Inter-Dept OOC | Out-Of-Character coordination across government agencies. |
| `/pdo {id/name}` | Targeted State | Narrative condition directed exclusively to specified player ID or character name. |
| `/pm {id/name}` | Private OOC | Targeted private message sent directly to specified player ID or character name. |
| `/m` or `/megaphone`| Megaphone | High-decibel tactical loudspeaker command for emergency vehicles. |

### 2. Specialized Department Personas & Lexicons
DavisLingo incorporates authentic roleplay lexicons tailored to server factions:
- **LSFD / Fire & Medic**: Medical triage taxonomy (CAT-A/B, BLS/ILS clinical interventions), radio ten-codes (*Status-2 through Status-10, 10-4*), and empathetic, clinical dialogue.
- **LSPD / Law Enforcement**: Procedural, authoritative law enforcement language, vehicle stop protocols, Miranda warnings, and tactical perimeter commands.
- **West Coast Street Gang**: Gritty, organic West Coast dialect (AAVE) reflecting authentic urban roleplay without stilted clichés.
- **Casual Civilian**: Natural, colloquial daily American English for civilian interactions and business roleplay.
- **Cartel & Narco Syndicate**: Bilingual Spanish/English phrasing (*hermano, jefe, tranquilo, compa*) suited for organized syndicate operations.
- **Underworld Syndicate**: Disciplined, cold, articulate, and intimidating syndicate dialogue.

### 3. Transparent High-Tech HUD Overlay
- **Obsidian Tactical Aesthetic**: Dark techno aesthetic (`#0B0F17`) utilizing soft cyan accents (`#00F2FE`) and slate dividers (`#1E293B`). Zero clashing colors.
- **Hardware-Accelerated Win32 Pinned Layer**: Styled with `WS_EX_TOPMOST` and `SWP_NOACTIVATE` to remain seamlessly floating above GTA V without stealing game focus.
- **Dual Display Modes**: Displays 3 distinct English response options alongside brief Indonesian intent indicators (*intent/vibe*) so you understand the exact tone of each response before sending.

### 4. Low-Spec "Potato Laptop" Optimization Engine
Running GTA V FiveM alongside Google Chrome and background desktop utilities frequently exhausts memory and triggers CPU micro-stutter on entry-level hardware. DavisLingo is optimized specifically for this constraint:
- **0% Idle CPU**: Replaces periodic polling with Windows low-level keyboard hooks (`WH_KEYBOARD_LL`). Consumes zero CPU cycles while idle.
- **Aggressive Memory Lifecycle**: PIL image buffers are immediately released post-OCR, followed by automated garbage collection (`gc.collect()`), maintaining a lean working set between 50 MB and 80 MB.
- **Preemptive Core Allocation**: OCR execution operates inside detached worker threads configured with low CPU priority to prevent FPS drops during firefights or high-speed vehicle pursuits.

---

## Default Keybinds & Shortcuts

| Action | Default Hotkey | Functional Behavior |
| :--- | :--- | :--- |
| **Scan Screen (OCR)** | `F4` | Ingests dialog from configured scan region and renders 3 options in HUD. |
| **Translate Selected Text** | `F5` | Replaces highlighted Indonesian text with fluent roleplay English in-place. |
| **Toggle HUD Overlay** | `F6` | Instantly toggles HUD visibility without affecting game focus. |
| **Select Reply #1** | `Ctrl + 1` | Pastes reply option #1 directly into the active game chat input. |
| **Select Reply #2** | `Ctrl + 2` | Pastes reply option #2 directly into the active game chat input. |
| **Select Reply #3** | `Ctrl + 3` | Pastes reply option #3 directly into the active game chat input. |
| **Cycle Faction Persona** | `Alt + 1` | Cycles active persona (LSFD -> LSPD -> Gang -> Civilian -> etc.). |
| **Cycle Emotion / Tone** | `Alt + 2` | Cycles conversational tone (Neutral -> Urgent -> Assertive -> etc.). |
| **Toggle Main Window** | `Insert` | Shows or hides the primary configuration dashboard. |
| **Scroll HUD Up / Down** | `PgUp` / `PgDn` | Scrolls through verbose multi-line replies within the HUD. |

*All keybinds are fully customizable via the **Custom Keybinds** tab in the desktop application.*

---

## Installation & Getting Started

### Method 1: Portable Standalone Release (Recommended)
No Python installation or dependencies required:
1. Download the latest `DavisLingo_Portable.zip` from [Viend-Lab/DavisLingo Releases](https://github.com/Viend-Lab/DavisLingo/releases).
2. Extract the archive into any preferred directory.
3. Launch `DavisLingo.exe` or execute `Start_DavisLingo.bat`.
4. Configure your scan area in the **Roleplay & HUD** tab and input your free API key from [console.groq.com](https://console.groq.com).

### Method 2: Running from Source
Prerequisites: **Python 3.12+** and **Git** on Windows 10/11:

```bash
# Clone repository from Viend Lab
git clone https://github.com/Viend-Lab/DavisLingo.git
cd DavisLingo

# Install production dependencies
pip install -r requirements.txt

# Launch application
python main.py
```

### Compiling Executable (PyInstaller)
```bash
# Build optimized production binary (Level-2 bytecode optimization)
pyinstaller --clean -y DavisLingo.spec
```

---

## Security, Privacy & Integrity Model

1. **At-Rest Windows DPAPI Encryption**:
   Sensitive API credentials are never stored in plaintext on disk. DavisLingo uses Microsoft Crypt32 API (`CryptProtectData`) tied to the local Windows user profile.
2. **Cryptographic SHA-256 Release Validation**:
   The built-in auto-updater verifies the cryptographic SHA-256 hash of all downloaded binaries before extraction, preventing MITM binary substitution attacks.
3. **Prompt Injection Defense**:
   Game chat context is isolated using structured XML delimiters (`<user_input>`), preventing malicious in-game text from overriding AI roleplay behavior.
4. **Anti-Reverse Engineering Hardening**:
   Internal API routes and system constants are de-obfuscated dynamically at runtime, preventing static string extraction. Integrated Win32 debugger detection protects runtime memory integrity.
5. **Zero Data Loss Upgrades**:
   The auto-update installer automatically excludes `config.json` (`/XF config.json`), ensuring your custom keybinds and preferences remain untouched across version upgrades.

---

## Project Structure

```
DavisLingo/
├── ai_service.py              # Sub-second Groq LPU translation & prompt engine
├── app_gui.py                 # Modern CustomTkinter tactical dashboard
├── config_manager.py          # Windows DPAPI encrypted configuration manager
├── hud_overlay.py             # Topmost semi-transparent Win32 game HUD
├── macro_controller.py        # Win32 CTypes virtual input & clipboard automation
├── ocr_service.py             # Tesseract OCR engine with Lanczos 2x pre-filtering
├── security_guard.py          # Anti-debugging, runtime integrity & deobfuscator
├── slang_engine.py            # Faction taxonomy, radio codes & slang dictionary
├── updater_service.py         # Dual-track backward-compatible update client
├── roi_picker.py              # Interactive on-screen ROI coordinate selector
├── main.py                    # Main application bootstrap & hotkey coordinator
├── build_worker.js            # Cloudflare Edge Worker gateway script
├── version_info.txt           # Windows PE executable version metadata
├── DavisLingo.spec            # PyInstaller build specification
└── slang_library.json         # Specialized roleplay dialect database
```

---

## About Viend Lab

**DavisLingo** is developed and maintained by **[Viend Lab](https://github.com/Viend-Lab)**, an independent software studio and developer collective building developer tools, creative visualizers, and agentic workflows.

- **GitHub Organization**: [github.com/Viend-Lab](https://github.com/Viend-Lab)
- **Official Website**: [viend.my.id](https://viend.my.id)
- **Contact & Inquiries**: [team@viend.my.id](mailto:team@viend.my.id)
- **Lead Developer**: [@viend987](https://github.com/viend987)

---

## License & Attribution

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License as published by the Free Software Foundation, version 3 (GPLv3)**.

> [!IMPORTANT]
> **Attribution Clause (GPLv3 Section 7b)**:
> In accordance with Section 7(b) of the GNU General Public License v3, any redistribution, modification, fork, or derivative work of this software **MUST PRESERVE** the original author and organization attribution to **Viend Lab** (`ViendLab`, `viend987`, `https://viend.my.id`), including visible copyright notices in the user interface, about dialogues, repository documentation, and binary metadata.
