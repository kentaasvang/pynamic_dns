import os
from dotenv import load_dotenv
load_dotenv()

from logging import (
        DEBUG,
        INFO,
        WARNING
)

from datetime import datetime

# WORKER 
SLEEP_IN_SECONDS=5


# CLOUDFLARE
ZONE_ID = os.getenv("ZONE_ID")
AUTH_KEY = os.getenv("AUTH_KEY") 
domains = [] 


# LOGGER
# writing to file:
#LOG_FILE = os.path.join("logs", f"{datetime.now().isoformat()} pynamic_dns.log")
LOG_LEVEL = INFO
LOG_FILE = None

