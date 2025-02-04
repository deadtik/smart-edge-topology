from mininet.topo import Topo

class BusTopo(Topo):
    def build(self):
        # Add a switch
        s1 = self.addSwitch('s1')
        
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add links between hosts and switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

def create_bus_topology():
    return BusTopo()
