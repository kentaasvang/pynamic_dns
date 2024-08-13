import os
import logging
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

DEBUG = False

if os.getenv("DEBUG") == "1":
    DEBUG = True

# Storage
STORAGE_DIR = Path("data")
STORAGE_DIR.mkdir(exist_ok=True)
STORAGE_PATH = STORAGE_DIR / "public_ip_address"

# WORKER 
SLEEP_IN_SECONDS=1*60*30

# CLOUDFLARE
ZONE_ID = os.getenv("ZONE_ID", "")
DNS_ID = os.getenv("DNS_ID", "")
API_TOKEN = os.getenv("API_TOKEN", "") 

# Logging
LOG_LEVEL = logging.INFO

if DEBUG:
    LOG_LEVEL = logging.DEBUG

