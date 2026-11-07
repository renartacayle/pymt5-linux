"""Wine and headless MT5 process management on Linux."""

import os
import shutil
import subprocess
import logging
from typing import Optional, List, Dict

logger = logging.getLogger("pymt5_linux.wine_manager")

STANDARD_TERMINAL_PATHS = [
    os.path.expanduser("~/.wine/drive_c/Program Files/MetaTrader 5/terminal64.exe"),
    os.path.expanduser("~/.wine/drive_c/Program Files/MetaTrader 5/terminal.exe"),
    os.path.expanduser("~/.wine/drive_c/Program Files (x86)/MetaTrader 5/terminal64.exe"),
    os.path.expanduser("~/.wine/drive_c/Program Files (x86)/MetaTrader 5/terminal.exe"),
]


def is_wine_installed() -> bool:
    """Check if Wine is installed and present in PATH."""
    return shutil.which("wine") is not None


def get_wine_version() -> Optional[str]:
    """Return Wine version string or None if not installed."""
    if not is_wine_installed():
        return None
    try:
        res = subprocess.run(["wine", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return res.stdout.strip()
    except Exception:
        return None


def is_xvfb_installed() -> bool:
    """Check if Xvfb (X Virtual Framebuffer) is installed for headless operation."""
    return shutil.which("Xvfb") is not None


def find_mt5_terminals(wine_prefix: Optional[str] = None) -> List[str]:
    """Find installed MetaTrader 5 terminal executables."""
    found = []
    prefix = wine_prefix or os.path.expanduser("~/.wine")
    drive_c = os.path.join(prefix, "drive_c")

    if not os.path.exists(drive_c):
        return found

    # Check standard paths
    for p in STANDARD_TERMINAL_PATHS:
        if os.path.exists(p):
            found.append(p)

    # Search Program Files if not found in default paths
    if not found:
        for root, _, files in os.walk(drive_c):
            for f in files:
                if f.lower() in ("terminal64.exe", "terminal.exe"):
                    found.append(os.path.join(root, f))
    return found


def start_headless_display(display: str = ":99", screen: str = "1024x768x16") -> Optional[subprocess.Popen]:
    """Start Xvfb virtual framebuffer display server in background."""
    if not is_xvfb_installed():
        logger.warning("Xvfb is not installed. Run 'sudo apt install xvfb' for headless display.")
        return None

    cmd = ["Xvfb", display, "-screen", "0", screen, "-ac"]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.environ["DISPLAY"] = display
        logger.info(f"Started headless Xvfb on DISPLAY={display} (PID: {proc.pid})")
        return proc
    except Exception as e:
        logger.error(f"Failed to start Xvfb: {e}")
        return None


def launch_terminal(
    terminal_path: str,
    headless: bool = False,
    display: str = ":99",
    wine_prefix: Optional[str] = None,
    extra_args: Optional[List[str]] = None
) -> subprocess.Popen:
    """Launch MT5 terminal64.exe inside Wine."""
    env = os.environ.copy()
    if wine_prefix:
        env["WINEPREFIX"] = wine_prefix
    if headless:
        env["DISPLAY"] = display

    cmd = ["wine", terminal_path]
    if extra_args:
        cmd.extend(extra_args)

    logger.info(f"Launching MT5 via Wine: {' '.join(cmd)}")
    return subprocess.Popen(cmd, env=env)
