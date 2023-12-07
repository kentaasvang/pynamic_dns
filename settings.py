import os
from dotenv import load_dotenv
load_dotenv()

ZONE_ID = os.getenv("ZONE_ID")
AUTH_KEY = os.getenv("AUTH_KEY") 

# add domains to track here
domains = [] 