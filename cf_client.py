import pprint
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
        json_result = result.json()
        return json_result

    def change_ip(self, domain, ip):
        dns_record_id = self.get_record_id(domain)
        url = self.base_url + "zones/" + self.zone_id + "/dns_records/" + dns_record_id
        result = requests.put(url, headers={"Authorization": "Bearer " + self.auth_key}, json={"name": domain, "type": "A", "content": ip})
        json_result = result.json()
        return json_result

    def get_record_id(self, domain):
        dns_records = self.get_dns_records()
        for record in dns_records["result"]:
            if record["name"] == domain:
                return record["id"]
        return None


if __name__ == "__main__":
    client = CFClient(settings.AUTH_KEY, settings.ZONE_ID)
    ret = client.change_ip("test.hsomsorg.no", "0.0.0.0")
    pprint.pprint(ret)