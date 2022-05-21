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

physical_interfaces = get_physical_interfaces()
bridge_interfaces = get_bridge_interfaces()


if __name__ == '__main__':
    print(physical_interfaces)
    print(bridge_interfaces)