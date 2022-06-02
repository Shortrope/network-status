from flask import Flask, render_template
from net_info import get_physical_iface_data, get_bridge_iface_data

app = Flask(__name__)


@app.route('/')
def index2():
    physical_iface_data = get_physical_iface_data()
    bridge_iface_data = get_bridge_iface_data()
    return render_template('index.html', physical_iface_data=physical_iface_data, bridge_iface_data=bridge_iface_data)
    