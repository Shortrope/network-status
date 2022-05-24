How Should the interface info be represented?
- everything in one dict
- physical interface dict and a bridge dict

```python
{
    'eno1': {
        'carrier': True, 
        'mac': 'aa:aa:aa:00:00:01',
        'speed': 1000
        'bridge':  { 'name': 'br0', 
            'ipv4': '192.168.1.14', 
            'netmask': '255.255.255.0', 
            'dhcp_static': 'static', 
            'defroute': True 
            }
        },
    'eno2': {
             'carrier': False,
             'mac': 'aa:aa:aa:00:00:02',
             'speed': 1000
        
        },
    'eno3': {
             'carrier': False,
             'mac': 'aa:aa:aa:00:00:03',
             'speed': 1000
        
        },
    'eno4': {
             'carrier': False,
             'mac': 'aa:aa:aa:00:00:04',
             'speed': 1000
        
        },
    
}
```


Default interface config after edgeLinux installation.
```
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=dhcp
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=eno3
UUID=3e51121d-57b4-466b-a792-7ae53f
DEVICE=eno3
ONBOOT=no
```