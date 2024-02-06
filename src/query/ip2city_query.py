import csv
import json
import ipaddress

class IP2LocationLiteQuery:
    def __init__(self, csv_path, languages=['en']):
        self.csv_path = csv_path
        self.languages = languages

    def ip_to_int(self, ip):
        return int(ipaddress.ip_address(ip))

    def query(self, ip):
        ip_int = self.ip_to_int(ip)
        with open(self.csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ip_from = int(row["IP_FROM"])
                ip_to = int(row["IP_TO"])
                if ip_from <= ip_int <= ip_to:
                    # 找到匹配的 IP 范围
                    result = {
                        "ip": ip,
                        "country": row["COUNTRY_NAME"].strip('"'),
                        "city": row["CITY_NAME"].strip('"'),
                        "latitude": row["LATITUDE"].strip('"'),
                        "longitude": row["LONGITUDE"].strip('"')
                    }
                    return result
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: query.py <IP_ADDRESS>")
        sys.exit(1)

    ip = sys.argv[1]
    csv_path = '/Users/devin.zhang/test/ip_location/Ip2locationLite/IP2LOCATION-LITE-DB5.CSV'
    query_tool = IP2LocationLiteQuery(csv_path)
    result = query_tool.query(ip)
    print(result)
