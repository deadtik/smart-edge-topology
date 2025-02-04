from mininet.topo import Topo

class LinearTopo(Topo):
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add links between switches and hosts
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(s1, s2)

def create_linear_topology():
    return LinearTopo()
