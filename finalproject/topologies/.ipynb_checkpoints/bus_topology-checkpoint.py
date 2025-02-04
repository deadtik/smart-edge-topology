from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch

def create_bus_topology():
    net = Mininet(controller=Controller, switch=OVSSwitch)
    net.addController('c0', controller=Controller, protocol='tcp', port=6654)
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    s1 = net.addSwitch('s1')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    return net


