import networkx as nx
import matplotlib.pyplot as plt

# Function to visualize the topology using NetworkX and Matplotlib
def visualize_topology(edges, topology_name):
    G = nx.Graph()

    # Add edges (links) to the graph
    for edge in edges:
        G.add_edge(edge[0], edge[1])

    # Draw the network graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=2000, font_size=10)
    plt.title(topology_name)
    plt.show()   

    # Test data
edges_bus = [
    ('h1', 's1'),
    ('h2', 's1'),
    ('h3', 's1')
]
visualize_topology(edges_bus, 'Bus Topology')

edges_distributed = [
    ('h1', 's1'),
    ('h2', 's1'),
    ('h3', 's2'),
    ('s1', 's2')
]
visualize_topology(edges_distributed, 'Distributed Topology')

edges_heirarchical = [
    ('s1', 's2'),
    ('h1', 's1'),
    ('h2', 's2')
]
visualize_topology(edges_heirarchical, 'Heirarchical Topology')

edges_hybrid1 = [
    ('h1', 's1'),
    ('h2', 's1'),
    ('h3', 'h4'),
    ('h4', 's1'),
    ('h3', 's1')
]
visualize_topology(edges_hybrid1, 'Hybrid1 Topology')


edges_hybrid2 = [
    ('h1', 's1'),
    ('h2', 's1'),
    ('h3', 's1'),
    ('h4', 'h3')
]
visualize_topology(edges_hybrid2, 'Hybrid2 Topology')

edges_linear = [
    ('h1', 'h2'),
    ('h2', 'h3')
]
visualize_topology(edges_linear, 'Linear Topology')

edges_mesh = [
    ('h1', 'h2'),
    ('h1', 'h3'),
    ('h1', 'h4'),
    ('h2', 'h3'),
    ('h2', 'h4'),
    ('h3', 'h4')
]
visualize_topology(edges_mesh, 'Mesh Topology')

edges_ring = [
    ('h1', 'h2'),
    ('h2', 'h3'),
    ('h3', 'h4'),
    ('h4', 'h1')
]
visualize_topology(edges_ring, 'Ring Topology')

edges_star = [
    ('h1', 's1'),
    ('h2', 's1'),
    ('h3', 's1')
]
visualize_topology(edges_star, 'Star Topology')

edges_tree = [
    ('s1', 's2'),
    ('h1', 's1'),
    ('h2', 's2'),
    ('h3', 's2')
]
visualize_topology(edges_tree, 'Tree Topology')
