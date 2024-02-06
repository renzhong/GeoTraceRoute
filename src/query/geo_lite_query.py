import geoip2.database

languages = ['zh-CN', 'en']

class GeoLiteQuery:
    def __init__(self, db_path):
        # 初始化时加载GeoLite2数据库
        self.db_path = db_path
        self.db = geoip2.database.Reader(db_path)

    def get_name_by_languages(self, names_dict):
        # 按照语言列表顺序尝试获取名称
        for lang in languages:
            if names_dict and lang in names_dict:
                return names_dict[lang]
        return "Unknown"

    def query(self, ip):
        try:
            response = self.db.city(ip)

            country_name = self.get_name_by_languages(response.country.names)
            city_name = self.get_name_by_languages(response.city.names)

            print(response)
            result = {
                "ip": ip,
                "country": country_name,
                "city": city_name,
                "latitude": response.location.latitude if response.location.latitude else 0,
                "longitude": response.location.longitude if response.location.longitude else 0
            }
            return result
        except Exception as e:
            return None

    def close(self):
        # 关闭数据库连接
        self.db.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: query.py <IP_ADDRESS>")
        sys.exit(1)

    ip = sys.argv[1]
    # 示例用法
    # db_path = '/Users/devin.zhang/test/ip_location/GeoLite/GeoLite2-City_20240202/GeoLite2-City.mmdb'
    db_path = '/Users/devin.zhang/test/ip_location/DbipLite/dbip-city-lite-2024-02.mmdb'
    geo_query = GeoLiteQuery(db_path)
    result = geo_query.query(ip)
    print(result)
    geo_query.close()
