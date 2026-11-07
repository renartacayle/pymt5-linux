#!/usr/bin/env bash
# ==============================================================================
# Helper script to set up Wine, Xvfb, and MT5 on Ubuntu/Debian
# ==============================================================================
set -e

echo "=== [1/4] Installing Wine and Virtual Framebuffer (Xvfb) ==="
sudo dpkg --add-architecture i386 || true
sudo apt-get update
sudo apt-get install -y wine wine32 wine64 xvfb wget curl

echo "=== [2/4] Initializing Wine prefix ==="
wineboot --init

echo "=== [3/4] Downloading MetaTrader 5 Ubuntu Installer ==="
wget -nc https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5ubuntu.sh
chmod +x mt5ubuntu.sh

echo "=== [4/4] Setup Complete ==="
echo "You can now run: ./mt5ubuntu.sh to install MetaTrader 5."
echo "Then start your gateway with: pymt5-linux gateway"
