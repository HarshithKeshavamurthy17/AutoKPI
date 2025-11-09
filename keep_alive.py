#!/usr/bin/env python3
"""
Keep AutoKPI Alive Script
Pings your Streamlit app every 5 minutes to keep it awake
Run this on your computer or a server to keep your app alive
"""

import requests
import time
from datetime import datetime
import sys

# Your Streamlit app URL - UPDATE THIS!
APP_URL = "https://YOUR_APP_NAME.streamlit.app"

# Health check endpoint
HEALTH_ENDPOINT = f"{APP_URL}/_stcore/health"

# Alternative: Ping main page
MAIN_PAGE = APP_URL

# Interval in seconds (5 minutes = 300 seconds)
INTERVAL = 300


def ping_app(url, description):
    """Ping the app and return status"""
    try:
        response = requests.get(url, timeout=30)
        status = "✅" if response.status_code == 200 else "⚠️"
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {status} {description} - Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ❌ {description} - Error: {e}")
        return False


def main():
    """Main loop to keep app alive"""
    print(f"🚀 AutoKPI Keep-Alive Script")
    print(f"📡 App URL: {APP_URL}")
    print(f"⏱️  Interval: {INTERVAL} seconds (5 minutes)")
    print(f"🔄 Starting keep-alive pings...\n")
    
    ping_count = 0
    success_count = 0
    
    try:
        while True:
            ping_count += 1
            
            # Try health endpoint first
            if ping_app(HEALTH_ENDPOINT, f"[{ping_count}] Health Check"):
                success_count += 1
            else:
                # Fallback to main page
                print(f"   ⬇️  Trying main page as fallback...")
                if ping_app(MAIN_PAGE, f"[{ping_count}] Main Page"):
                    success_count += 1
            
            # Stats
            success_rate = (success_count / ping_count) * 100
            print(f"   📊 Stats: {success_count}/{ping_count} successful ({success_rate:.1f}%)\n")
            
            # Wait before next ping
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Keep-alive stopped by user")
        print(f"📊 Final Stats: {success_count}/{ping_count} successful ({success_rate:.1f}%)")
        sys.exit(0)


if __name__ == "__main__":
    if "YOUR_APP_NAME" in APP_URL:
        print("❌ ERROR: Please update APP_URL in keep_alive.py with your actual Streamlit app URL!")
        print(f"   Current: {APP_URL}")
        print(f"   Example: https://autokpi.streamlit.app")
        sys.exit(1)
    
    main()

