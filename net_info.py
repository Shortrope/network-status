import subprocess
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
        universal_newlines=True,
        check=False
    ).stdout.strip()
    if carrier == '':
        return False
    if int(carrier) == 1:
        return True
    return False


def get_iface_data():
    iface_data = {}
    for iface in get_physical_interfaces():
        mac = get_interface_mac(iface)
        connected = is_physical_interface_connected(iface)
        #speed = get_interface_speed(iface)
        iface_data.update({iface : { 'mac': mac, 'connected': connected }})
    for iface in get_bridge_interfaces():
        mac = get_interface_mac(iface)
        using_physical_iface = 'n/a'
        for phys_iface in get_physical_interfaces():
            if mac == iface_data[phys_iface]['mac']:
                using_physical_iface = phys_iface
                break
        iface_data.update({iface : { 'mac': mac, 'using': using_physical_iface }})
                
    return iface_data




if __name__ == '__main__':
    print(get_physical_interfaces())
    print(get_bridge_interfaces())
    pprint(get_iface_data())
    print(is_physical_interface_connected('eno1'))
    print(is_physical_interface_connected('eno2'))
    #print(get_interface_speed('br1'))