import requests
import settings

class CFClient:
    base_url = "https://api.cloudflare.com/client/v4/"
    def __init__(self, auth_key, zone_id):
        self.auth_key = auth_key
        self.zone_id = zone_id

    def get_dns_records(self):
        url = self.base_url + "zones/" + self.zone_id + "/dns_records"
        result = requests.get(url, headers={"Authorization": "Bearer " + self.auth_key})
        print(result)
        

if __name__ == "__main__":
    client = CFClient(settings.AUTH_KEY, settings.ZONE_ID)
    client.get_dns_records()