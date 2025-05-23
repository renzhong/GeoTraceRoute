import ipinfo
import os
import urllib.request
import json

class IpInfoQuery:
    def __init__(self):
        self.url_format = 'https://api.ipinfo.io/lite/{ip}?token={token}'
        self.access_token = os.environ.get('IPINFO_TOKEN', '')
        if not self.access_token:
            raise ValueError('IPINFO_TOKEN 环境变量未设置')

    def query(self, ip):
        print("query 1 ", ip)
        try:
            url = self.url_format.format(ip=ip, token=self.access_token)
            with urllib.request.urlopen(url) as response:
                resp_data = response.read().decode('utf-8')
                print("HTTPS 返回结果:", resp_data)
                data = json.loads(resp_data)
            result = {
                "ip": ip,
                "country": data.get("country", ""),
            }
            return result
        except Exception as e:
            return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: query.py <IP_ADDRESS>")
        sys.exit(1)

    ip = sys.argv[1]
    query = IpInfoQuery()
    query.query(ip)
