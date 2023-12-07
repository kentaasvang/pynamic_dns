import time
import requests
import settings

from cf_client import CFClient

def get_current_server_ip():
    result = requests.get("https://ifconfig.me")
    return result.text

cf_client = CFClient(settings.AUTH_KEY, settings.ZONE_ID)

while True:
    # Get the current IP address
    current_ip = get_current_server_ip()
    print(current_ip)

    dns_records = cf_client.get_dns_records()
    for dns_record in dns_records["result"]:
        if dns_record["name"] in settings.domains:
            if dns_record["content"] != current_ip:
                print("Changing IP for", dns_record["name"])
                res = cf_client.change_ip(dns_record["name"], current_ip)
            else:
                print("IP for", dns_record["name"], "is already correct")

    # Sleep for 2 hours
    time.sleep(1*60*60*2)