import json
import os
import sys
import copy
import base64
import ctypes
from ctypes import wintypes

OFFICIAL_AUTHOR = "Viend (ViendLab)"
PROJECT_SIGNATURE = "VIENDLAB-DAVISLINGO-RP-OFFICIAL-2026"

crypt32 = getattr(ctypes.windll, "crypt32", None) if sys.platform == "win32" else None
kernel32 = getattr(ctypes.windll, "kernel32", None) if sys.platform == "win32" else None

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]

def encrypt_dpapi(plain_text: str) -> str:
    if not plain_text or not crypt32 or not kernel32:
        return plain_text
    try:
        data_bytes = plain_text.encode('utf-8')
        in_blob = DATA_BLOB()
        in_blob.cbData = len(data_bytes)
        in_blob.pbData = (ctypes.c_byte * len(data_bytes))(*data_bytes)
        
        out_blob = DATA_BLOB()
        # CRYPTPROTECT_UI_FORBIDDEN = 0x1
        res = crypt32.CryptProtectData(
            ctypes.byref(in_blob),
            "DavisLingoSecureKey",
            None,
            None,
            None,
            0x1,
            ctypes.byref(out_blob)
        )
        if not res:
            return plain_text
        try:
            encrypted_bytes = bytes((ctypes.c_byte * out_blob.cbData).from_address(ctypes.addressof(out_blob.pbData.contents)))
            return "DPAPI:" + base64.b64encode(encrypted_bytes).decode('ascii')
        finally:
            kernel32.LocalFree(out_blob.pbData)
    except Exception:
        return plain_text

def decrypt_dpapi(cipher_text: str) -> str:
    if not cipher_text or not crypt32 or not kernel32:
        return cipher_text
    if not cipher_text.startswith("DPAPI:"):
        return cipher_text # unencrypted fallback
    try:
        raw_b64 = cipher_text[len("DPAPI:"):]
        encrypted_bytes = base64.b64decode(raw_b64)
        in_blob = DATA_BLOB()
        in_blob.cbData = len(encrypted_bytes)
        in_blob.pbData = (ctypes.c_byte * len(encrypted_bytes))(*encrypted_bytes)
        
        out_blob = DATA_BLOB()
        res = crypt32.CryptUnprotectData(
            ctypes.byref(in_blob),
            None,
            None,
            None,
            None,
            0x1,
            ctypes.byref(out_blob)
        )
        if not res:
            return ""
        try:
            decrypted_bytes = bytes((ctypes.c_byte * out_blob.cbData).from_address(ctypes.addressof(out_blob.pbData.contents)))
            return decrypted_bytes.decode('utf-8')
        finally:
            kernel32.LocalFree(out_blob.pbData)
    except Exception:
        return ""

DEFAULT_CONFIG = {
    "ai_provider": "groq",
    "groq_api_key": "",
    "groq_model": "qwen/qwen3.8-27b",
    "current_style": "LSFD / Fire & Medic",
    "emotion_tone": "Neutral",
    "auto_paste_top_reply": False,
    "bbox": {
        "left": 265,
        "top": 233,
        "width": 645,
        "height": 73
    },
    "osd_bbox": {
        "left": 1091,
        "top": 122,
        "width": 340,
        "height": 580
    },
    "osd_enabled": True,
    "osd_duration": 15,
    "osd_alpha": 0.88,
    "sound_feedback": True,
    "hotkeys": {
        "hotkey_ocr": "f4",
        "hotkey_clipboard": "f5",
        "hotkey_toggle_hud": "f6",
        "hotkey_ans1": "ctrl+1",
        "hotkey_ans2": "ctrl+2",
        "hotkey_ans3": "ctrl+3",
        "hotkey_cycle_style": "alt+1",
        "hotkey_cycle_tone": "alt+2",
        "hotkey_toggle_window": "insert",
        "hotkey_scroll_up": "page up",
        "hotkey_scroll_down": "page down"
    }
}

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_config_path():
    return os.path.join(get_base_dir(), "config.json")

def deep_merge(base, override):
    """
    Recursively merge override dictionary into base dictionary.
    Keys present in base but missing in override are preserved.
    Keys present in override overwrite base.
    """
    result = copy.deepcopy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result

class ConfigManager:
    def __init__(self):
        self.config_path = get_config_path()
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                
                # Decrypt sensitive keys if encrypted with DPAPI
                raw_key = loaded.get("groq_api_key", "")
                if raw_key and raw_key.startswith("DPAPI:"):
                    loaded["groq_api_key"] = decrypt_dpapi(raw_key)

                # Deep merge to preserve all user config while automatically adopting new keys
                self.data = deep_merge(DEFAULT_CONFIG, loaded)

                # If loaded was plaintext, save back encrypted
                if raw_key and not raw_key.startswith("DPAPI:"):
                    self.save()
                elif self.data != loaded:
                    self.save()
                return
            except Exception:
                pass
        self.data = copy.deepcopy(DEFAULT_CONFIG)
        self.save()

    def save(self):
        try:
            disk_data = copy.deepcopy(self.data)
            # Transparently encrypt groq_api_key for at-rest disk storage
            plain_key = disk_data.get("groq_api_key", "")
            if plain_key and not plain_key.startswith("DPAPI:"):
                disk_data["groq_api_key"] = encrypt_dpapi(plain_key)

            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(disk_data, f, indent=4)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value, auto_save=True):
        self.data[key] = value
        if auto_save:
            self.save()
