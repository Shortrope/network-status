import subprocess
import re
import json
import os
from pprint import pprint


def get_physical_interfaces():
    ifaces_list = subprocess.run(
        "ls -l /sys/class/net | grep -v virtual | grep -v total | awk '{print $9}'",
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=False
    )
    return ifaces_list.stdout.split()


def get_bridge_interfaces():
    virtual_net_list = subprocess.run(
        "ls -1 /sys/devices/virtual/net",
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=False
    ).stdout.split()
    iface_config_file_list = subprocess.run(
        "for p in `ls -1 /etc/sysconfig/network-scripts/ifcfg-*`; do basename $p | cut -d'-' -f2 | grep -v '^lo$'; done",
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=False
    ).stdout.split()
    bridge_list = [iface for iface in iface_config_file_list if iface in virtual_net_list]
    return bridge_list


def get_interface_mac(iface):
    mac = subprocess.run(
        f"ip link show {iface} | grep link | awk '{{print $2}}'",
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=False
    ).stdout.strip()
    return mac

def is_physical_interface_connected(iface):
    carrier = subprocess.run(
        f"cat /sys/class/net/{iface}/carrier",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        check=False
    ).stdout.strip()
    if carrier == '':
        return False
    if int(carrier) == 1:
        return True
    return False


def ip_addr_show():
    ip_addr_show = subprocess.run(
        ["ip", "address", "show"],
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
    return ip_addr_show.stdout


def iface_speed(iface_name):
    output = subprocess.run(
        ["ethtool", iface_name],
        universal_newlines=True,
        stdout=subprocess.PIPE
    ).stdout.split('\n')
    speed_re = re.compile(r'(\d{2}\w+\/(Full|Half))')
    speeds = set()
    for line in output:
        speed_matches = speed_re.findall(line)
        if speed_matches:
            for item in speed_matches:
                speeds.add(item[0])
        else:
            continue
    if not speeds:
        return ''
    return(sorted(speeds)[0])


def create_iface_data_array(ip_addr_show_text):
    '''
    Returns an array of dicts:
    [{'ifIndex': '2',
      'ifName': 'eno1',
      'ifStatus': 'UP',
      'ifType': 'ether',
      'ipv4': '',
      'ipv6': '',
      'mac': 'ac:1f:6b:48:4b:84',
      'speed': '1000baseT/Full'},
      {'ifIndex': '7',
      'ifName': 'br0',
      'ifStatus': 'UNKNOWN',
      'ifType': 'ether',
      'ipv4': '192.168.1.14',
      'ipv6': 'fe80::ae1f:6bff:fe48:4b84/64',
      'mac': 'ac:1f:6b:48:4b:84',
      'speed': ''}
      ... 
    '''
    data = []

    iface_name_re = re.compile(r'^(\d{1,2}): ([^:]+):[^\n]+state (\w+)')
    link_re = re.compile(r'^\s+link\/(ether) ([0-9a-fA-F:]+)')
    ipv4_re = re.compile(r'^\s+inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2})')
    ipv6_re = re.compile(r'^\s+inet6 (([0-9a-fA-F:]+)\/(\d{1,3}))')

    for line in ip_addr_show_text.split('\n'):
        iface_info = {'ifName': '', 'mac': '', 'ipv4': '', 'ipv6': ''}
        match_name = iface_name_re.search(line)
        if match_name:
            iface_info['ifIndex'] = match_name.group(1)
            iface_info['ifName'] = match_name.group(2)
            iface_info['ifStatus'] = match_name.group(3)
            iface_info['speed'] = iface_speed(match_name.group(2))
            data.append(iface_info)
            
        match_mac = link_re.search(line)
        if match_mac:
            data[-1]['ifType'] = match_mac.group(1)
            data[-1]['mac'] = match_mac.group(2)
            
        match_ipv4 = ipv4_re.search(line)
        if match_ipv4:
            data[-1]['ipv4'] = match_ipv4.group(1) 

        match_ipv6 = ipv6_re.search(line)
        if match_ipv6:
            data[-1]['ipv6'] = match_ipv6.group(1)
            
    return data                

def get_iface_data():
    return create_iface_data_array(ip_addr_show())

def filter_interface_data(iface_data, filter_list):
    filtered_data = [] 
    for iface in iface_data:
        if iface['ifName'] in filter_list:
            filtered_data.append(iface)
    return filtered_data

def get_physical_iface_data():
    return filter_interface_data(get_iface_data(), get_physical_interfaces())

def get_bridge_iface_data():
    return filter_interface_data(get_iface_data(), get_bridge_interfaces())



if __name__ == '__main__':
    print(get_physical_interfaces())
    print(get_bridge_interfaces())
    print(is_physical_interface_connected('eno1'))
    print(is_physical_interface_connected('eno2'))
    print(is_physical_interface_connected('eno3'))
    print(is_physical_interface_connected('eno4'))
    #print(get_interface_speed('br1'))
    print(iface_speed('eno1'))
    print(iface_speed('eno2'))
    print(iface_speed('eno3'))
    print(iface_speed('eno4'))
    #pprint(create_iface_data_array(ip_addr_show()))
    pprint(filter_interface_data(get_iface_data(), get_physical_interfaces()))
    pprint(get_iface_data())