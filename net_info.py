import subprocess


def get_physical_interfaces():
    ifaces_list = subprocess.run(
        "ls -l /sys/class/net | grep -v virtual | grep -v total | awk '{print $9}'",
        shell=True,
        stdout=subprocess.PIPE,
        check=False
    ).stdout.decode().split()
    return ifaces_list

def get_bridge_interfaces():
    bridge_list = subprocess.run(
        "for p in `ls -1 /etc/sysconfig/network-scripts/ifcfg-*`; do basename $p | cut -d'-' -f2 | grep -v '^lo$'; done",
        shell=True,
        stdout=subprocess.PIPE,
        check=False
    ).stdout.decode().split()
    return list(filter(lambda bridge_list_item: bridge_list_item not in get_physical_interfaces(), bridge_list))

def get_interface_mac(iface):
    mac = subprocess.run(
        f"ip link show {iface} | grep link | awk '{{print $2}}'",
        shell=True,
        stdout=subprocess.PIPE,
        check=False
    ).stdout.decode().strip()
    return mac


def get_iface_data():
    iface_data = {}
    for iface in get_physical_interfaces():
        mac = get_interface_mac(iface)
        #speed = get_interface_speed(iface)
        iface_data.update({iface : { 'mac': mac }})
    for iface in get_bridge_interfaces():
        mac = get_interface_mac(iface)
        iface_data.update({iface : { 'mac': mac }})
                
    return iface_data




if __name__ == '__main__':
    print(get_physical_interfaces())
    print(get_bridge_interfaces())
    print(get_iface_data())
    #print(get_interface_speed('br1'))