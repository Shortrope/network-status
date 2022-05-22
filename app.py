from flask import Flask, render_template
from net_info import get_physical_interfaces, get_bridge_interfaces, get_interface_mac, get_iface_data

app = Flask(__name__)


@app.route('/')
def index():
    physical_interfaces = get_physical_interfaces()
    bridge_interfaces = get_bridge_interfaces()
    iface_data = get_iface_data()
    
    return render_template('index.html', physical_interfaces=physical_interfaces, bridge_interfaces=bridge_interfaces, iface_data=iface_data)
