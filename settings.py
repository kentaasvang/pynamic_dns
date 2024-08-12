import os
import logging
from dotenv import load_dotenv
load_dotenv()

DEBUG = True if os.getenv("PYNAMIC_DNS_DEBUG") == "1" else False

# WORKER 
SLEEP_IN_SECONDS=1*60*30

# CLOUDFLARE
ZONE_ID = os.getenv("ZONE_ID")
AUTH_KEY = os.getenv("AUTH_KEY") 


# LOGGER
# writing to file:
#LOG_FILE = os.path.join("logs", f"{datetime.now().isoformat()} pynamic_dns.log")
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOG_FILE = None

