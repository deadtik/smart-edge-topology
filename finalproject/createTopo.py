from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, Node
from mininet.cli import CLI

class Router(Node):
    def config(self, **kwargs):  # Accept any extra parameters to avoid errors
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super().terminate()

class CustomNetwork(Topo):
    def build(self):
        # Add routers
        r1 = self.addNode('r1', cls=Router)
        r2 = self.addNode('r2', cls=Router)

        # Add hosts
        h1 = self.addHost('h1', ip='192.168.1.2/24', defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2', ip='192.168.1.3/24', defaultRoute='via 192.168.1.1')
        h3 = self.addHost('h3', ip='192.168.1.4/24', defaultRoute='via 192.168.1.1')

        h4 = self.addHost('h4', ip='192.168.2.2/24', defaultRoute='via 192.168.2.1')
        h5 = self.addHost('h5', ip='192.168.2.3/24', defaultRoute='via 192.168.2.1')
        h6 = self.addHost('h6', ip='192.168.2.4/24', defaultRoute='via 192.168.2.1')

        # Connect hosts directly to routers
        self.addLink(r1, h1)
        self.addLink(r1, h2)
        self.addLink(r1, h3)

        self.addLink(r2, h4)
        self.addLink(r2, h5)
        self.addLink(r2, h6)

        # Connect routers to each other
        self.addLink(r1, r2)

def configureNetwork(net):
    r1 = net.get('r1')
    r2 = net.get('r2')

    # Assign IP addresses to routers
    r1.setIP('192.168.1.1/24', intf='r1-eth1')
    r2.setIP('192.168.2.1/24', intf='r2-eth1')

    # Assign IPs for router interconnection
    r1.setIP('10.0.1.1/30', intf='r1-eth2')
    r2.setIP('10.0.1.2/30', intf='r2-eth2')

    # Configure routing
    r1.cmd('ip route add 192.168.2.0/24 via 10.0.1.2')
    r2.cmd('ip route add 192.168.1.0/24 via 10.0.1.1')

    # Set default gateways on hosts
    net.get('h1').cmd('route add default gw 192.168.1.1')
    net.get('h2').cmd('route add default gw 192.168.1.1')
    net.get('h3').cmd('route add default gw 192.168.1.1')

    net.get('h4').cmd('route add default gw 192.168.2.1')
    net.get('h5').cmd('route add default gw 192.168.2.1')
    net.get('h6').cmd('route add default gw 192.168.2.1')

def testConnectivity(net):
    h1 = net.get('h1')
    h4 = net.get('h4')

    print("Testing connectivity between h1 and h4...")
    result = h1.cmd('ping -c 3 192.168.2.2')
    print(result)

if __name__ == '__main__':
    topo = CustomNetwork()
    net = Mininet(topo=topo, controller=Controller, switch=OVSKernelSwitch)
    net.start()
    configureNetwork(net)
    testConnectivity(net)
    CLI(net)
    net.stop()

