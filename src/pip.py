#!/usr/bin/env python3

import sys
import os
import re
from rich.console import Console
from rich.table import Table

sys.path.append(os.path.join(os.path.dirname(__file__), 'query'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from ipinfo_query import IpInfoQuery
from utils import check_reserved_ip

ipfifo_query = IpInfoQuery()

console = Console()

class LatencyStats:
    def __init__(self):
        self.total = 0.0
        self.count = 0
        self.max = None
        self.min = None

    def add_latency(self, latency):
        if latency is not None:
            latency = float(latency)
            self.total += latency
            self.count += 1
            if self.max is None or latency > self.max:
                self.max = latency
            if self.min is None or latency < self.min:
                self.min = latency

    def average_latency(self):
        return self.total / self.count if self.count > 0 else 0

    def debug_string(self):
        if self.count == 0:
            return "None"
        return "count:{} avg:{} max:{} min:{}".format(self.count, self.average_latency(), self.max, self.min)

class GeoInfo:
    def __init__(self, name, country, city):
        self.name = name
        self.country = country
        self.city = city

    def debug_string(self):
        return "name:{} country:{} city:{}".format(self.name, self.country, self.city)

    def info(self):
        return "country:{} city:{}".format(self.country, self.city)

class TraceRouteLine:
    hop = -1
    domain = '*'
    ip = ''
    latencies = LatencyStats()
    geo_info_list = []

    def __init__(self, hop, domain = "*", ip = '', latencies = None):
        self.hop = hop
        self.domain = domain
        self.ip = ip
        self.latencies = latencies if latencies is not None else LatencyStats()
        self.geo_info_list = []

    def debug_string(self):
        debug_string = "hop:{} domain:{} ip:{} latency:{}".format(
                self.hop, self.domain, self.ip,
                self.latencies.debug_string())

        for geo_info in self.geo_info_list:
            debug_string += " geo_info:{}".format(geo_info.debug_string())

        return debug_string


def parse_traceroute_output(line):
    if len(line) == 0:
        return TraceRouteLine(-1)

    hop = -2
    i = 0

    parts = line.split()

    if parts[i].isdigit():
        hop = int(int(parts[i]))
        i += 1

    # 找到不是 * 的列
    while i < len(parts) and parts[i] == "*":
        i += 1

    domain = ""
    ip = ""
    latencies = []

    # 如果找到了有效的列
    if i == len(parts):
        domain = "*"
        ip = ""
        return TraceRouteLine(hop, domain, ip)
    else:
        domain = parts[i]
        match = re.match(r"\((.+)\)", parts[i+1])
        ip = match.group(1) if match else ""
        i += 2
    print("domain:{} ip:{}".format(domain, ip))

    latency_stats = LatencyStats()
    while i < len(parts):
        latency_value = parts[i]
        latency_unit = parts[i + 1] if i + 1 < len(parts) else None
        if latency_unit == "ms":
            latency_stats.add_latency(float(latency_value))
            i += 2
        else:
            i += 1

    return TraceRouteLine(hop, domain, ip, latency_stats)

def query(query_client, ip, name):
    result = query_client.query(ip)
    if result is None:
        return None

    country = result['country']
    city = result['city'] if 'city' in result else ''
    geo_info = GeoInfo(name, country, city)

    return geo_info

def process_line(line):
    line_obj = parse_traceroute_output(line)

    if line_obj.ip != '':
        geo_info = query(ipfifo_query, line_obj.ip, "ipinfo")
        if geo_info is not None:
            line_obj.geo_info_list.append(geo_info)

    return line_obj

def init_table(line_obj_list):
    index = 0
    max_geo_query = 0
    for i, obj in enumerate(line_obj_list):
        if len(obj.geo_info_list) > max_geo_query:
            index = i
            max_geo_query = len(obj.geo_info_list)

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Hop", style="dim", width=6)
    table.add_column("域名", width=20)
    table.add_column("IP", justify="right")
    table.add_column("尝试次数", justify="right")
    table.add_column("平均耗时", justify="right")
    table.add_column("最大耗时", justify="right")
    table.add_column("最小耗时", justify="right")

    if index != 0:
        max_obj = line_obj_list[index]
        for geo_info in max_obj.geo_info_list:
            table.add_column(geo_info.name, justify="right")

    return table

def display_traceroute_results(table, line_obj_list):
    for line_obj in line_obj_list:
        if line_obj.hop == 0:
            continue

        hop = ''
        if line_obj.hop > 0:
            table.add_section()
            hop = str(line_obj.hop)

        row_data = [hop, line_obj.domain, line_obj.ip]

        row_data.append(str(line_obj.latencies.count))
        row_data.append(str(round(line_obj.latencies.average_latency(), 2)))
        row_data.append(str(line_obj.latencies.max))
        row_data.append(str(line_obj.latencies.min))

        for geo_info in line_obj.geo_info_list:
            row_data.append(geo_info.info())

        table.add_row(*row_data)

    return table

def main():
    line_obj_list = []
    for line in sys.stdin:
        line_obj = process_line(line.strip())
        line_obj_list.append(line_obj)
        # print(line)
        # print(line_obj.debug_string())
        table = init_table(line_obj_list)
        table = display_traceroute_results(table, line_obj_list)
        console.clear()
        console.print(table)

if __name__ == "__main__":
    main()
