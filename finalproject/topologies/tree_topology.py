from mininet.topo import Topo

class TreeTopo(Topo):
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add links between hosts and switches
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s2)

        # Add link between switches (tree structure)
        self.addLink(s1, s2)

def create_tree_topology():
    return TreeTopo()
