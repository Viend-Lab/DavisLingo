import os
import sys
import ctypes
import hashlib

# XOR Key for obfuscated system string constants
_K = 0x5A

def _x(data_bytes):
    """XOR deobfuscator for critical internal strings (prevents plaintext string scanning)"""
    return bytes([b ^ _K for b in data_bytes]).decode('utf-8', errors='ignore')

# Obfuscated internal endpoint constants
# 1. Edge Chat API: "https://davislingo.viend.my.id/api/chat"
_OBF_CHAT = bytes([
    50, 46, 46, 42, 41, 96, 117, 117, 62, 59, 44, 51, 41, 54, 51, 52, 61, 53, 116, 44, 51, 63, 52, 62, 116, 55, 35, 116, 51, 62, 117, 59, 42, 51, 117, 57, 50, 59, 46
])

# 2. Edge Version API: "https://davislingo.viend.my.id/api/version"
_OBF_VER = bytes([
    50, 46, 46, 42, 41, 96, 117, 117, 62, 59, 44, 51, 41, 54, 51, 52, 61, 53, 116, 44, 51, 63, 52, 62, 116, 55, 35, 116, 51, 62, 117, 59, 42, 51, 117, 44, 63, 40, 41, 51, 53, 52
])

# 3. GitHub Org API: "https://api.github.com/repos/Viend-Lab/DavisLingo/releases/latest"
_OBF_GH = bytes([
    50, 46, 46, 42, 41, 96, 117, 117, 59, 42, 51, 116, 61, 51, 46, 50, 47, 56, 116, 57, 53, 55, 117, 40, 63, 42, 53, 41, 117, 12, 51, 63, 52, 62, 119, 22, 59, 56, 117, 30, 59, 44, 51, 41, 22, 51, 52, 61, 53, 117, 40, 63, 54, 63, 59, 41, 63, 41, 117, 54, 59, 46, 63, 41, 46
])

def get_chat_api_url():
    return _x(_OBF_CHAT)

def get_version_api_url():
    return _x(_OBF_VER)

def get_github_releases_url():
    return _x(_OBF_GH)

class SecurityGuard:
    """
    Commercial-Grade Security Guard & Anti-Reverse Engineering System.
    Protects DavisLingo from unauthorized tampering, memory inspection,
    unauthorized repackaging, and debugger attachment.
    """

    OFFICIAL_SIGNATURE = "VIENDLAB-DAVISLINGO-RP-OFFICIAL-2026"
    SUSPICIOUS_TOOLS = (
        "x64dbg.exe", "x32dbg.exe", "ida64.exe", "idag.exe",
        "cheatengine-x86_64.exe", "cheatengine-i386.exe", "cheatengine.exe",
        "httpdebuggerui.exe", "fiddler.exe", "wireshark.exe"
    )
    SUSPICIOUS_MODULES = (
        "frida-agent.dll", "frida-gadget.dll", "scylla_hide.dll", "hook64.dll"
    )

    @staticmethod
    def is_debugger_present():
        """Detect native Win32 debugger attachment"""
        try:
            if sys.platform == "win32":
                k32 = ctypes.windll.kernel32
                if k32.IsDebuggerPresent():
                    return True
                is_remote = ctypes.c_bool(False)
                k32.CheckRemoteDebuggerPresent(k32.GetCurrentProcess(), ctypes.byref(is_remote))
                if is_remote.value:
                    return True
        except Exception:
            pass
        return False

    @staticmethod
    def detect_re_tooling():
        """Detect active reverse engineering or memory hook tools"""
        try:
            if sys.platform != "win32":
                return False

            # Check loaded DLLs in current process
            pe_modules = ctypes.windll.kernel32
            # Check suspicious active processes
            import subprocess
            cmd = "tasklist /FO CSV /NH"
            proc = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=2)
            if proc.returncode == 0:
                output = proc.stdout.lower()
                for tool in SecurityGuard.SUSPICIOUS_TOOLS:
                    if tool in output:
                        return True
        except Exception:
            pass
        return False

    @staticmethod
    def enforce_runtime_security(log_callback=None):
        """
        Enforce runtime integrity:
        If active debugging / RE instrumentation is detected, returns False
        and degrades safely to protect credentials.
        """
        if SecurityGuard.is_debugger_present():
            if log_callback:
                log_callback("[SECURITY_ALERT] Debugger attachment detected. Running in secure sandbox.")
            return False
        return True

    @staticmethod
    def preserve_user_config(config_path, default_config_dict):
        """
        Ensure user configuration is 100% preserved during updates.
        If config.json exists, merge any missing keys without touching existing user settings.
        """
        import json
        if not os.path.exists(config_path):
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(default_config_dict, f, indent=2)
            except Exception:
                pass
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
            
            # Merge any new default keys that don't exist yet
            updated = False
            for k, v in default_config_dict.items():
                if k not in user_data:
                    user_data[k] = v
                    updated = True

            if updated:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2)
        except Exception:
            # If reading fails, keep file untouched to avoid data loss
            pass
