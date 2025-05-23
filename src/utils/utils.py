import ipaddress

def check_reserved_ip(ip):
    ip_obj = ipaddress.ip_address(ip)
    # 检查是否是保留的私有地址或者特殊用途地址
    return ip_obj.is_private or ip_obj.is_multicast or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved

if __name__ == "__main__":
    # 示例
    ips = ["192.168.1.1", "127.0.0.1", "8.8.8.8", "fe80::", "ff02::1"]
    for ip in ips:
        print(f"{ip} is reserved: {check_reserved_ip(ip)}")
