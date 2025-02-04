import sys
import os

# Define the base directory
base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)  # Add the base directory to path

# Now Python can locate `createTopo`
from createTopo import CustomNetwork 

# Append other directories correctly
sys.path.append(os.path.join(base_dir, 'topologies'))
sys.path.append(os.path.join(base_dir, 'utils'))


from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel

# Import topology creation and utility functions
from topologies.bus_topology import create_bus_topology
from topologies.star_topology import create_star_topology
from topologies.ring_topology import create_ring_topology
from topologies.mesh_topology import create_mesh_topology
from topologies.linear_topology import create_linear_topology
from topologies.heirarchical_topology import create_heirarchical_topology
from topologies.tree_topology import create_tree_topology
from topologies.distributed_topology import create_distributed_topology
from topologies.hybrid1_topology import create_hybrid1_topology
from topologies.hybrid2_topology import create_hybrid2_topology

from utils.errors import add_network_errors
from utils.datacollected import collect_synthetic_data
from utils.savetocsv import save_data_to_csv
from createTopo import createTopo  # Importing your default topology class

def run_simulation(create_topology, topology_name, edges, **error_params):
    """Run the simulation for a specific topology."""
    # Create the topology
    topo = create_topology()

    # Create the Mininet network with the created topology and controller
    net = Mininet(topo=topo, switch=OVSKernelSwitch, controller=OVSController)
    net.addController(name='c0', controller=OVSController)

    # Start the network
    print(f"Running {topology_name} topology...")
    net.start()

    # Inject network errors
    print(f"Injecting errors into the network for {topology_name}...")
    add_network_errors(net, **error_params)

    # Perform a simple ping test to verify connectivity
    print("Performing connectivity test...")
    net.pingAll()

    # Start the Mininet CLI for user interaction
    CLI(net)

    # Collect synthetic data (e.g., latency, throughput, etc.)
    print("Collecting synthetic data...")
    data = collect_synthetic_data(net, topology_name)
    print(f"Collected data for {topology_name}: {data}")

    # Save the data to a CSV file
    print("Saving collected data to CSV...")
    save_data_to_csv('network_metrics.csv', data)

    # Stop the network
    net.stop()
    print(f"Simulation completed for {topology_name} topology.")

if __name__ == '__main__':
    # Define the topologies and their corresponding edges
    topologies = {
        'bus': (create_bus_topology, [
            ('h1', 's1'),
            ('h2', 's1'),
            ('h3', 's1')
        ]),
        'star': (create_star_topology, [
            ('h1', 's1'),
            ('h2', 's1'),
            ('h3', 's1')
        ]),
        'ring': (create_ring_topology, [
            ('h1', 'h2'),
            ('h2', 'h3'),
            ('h3', 'h4'),
            ('h4', 'h1')
        ]),
        'mesh': (create_mesh_topology, [
            ('h1', 'h2'),
            ('h1', 'h3'),
            ('h1', 'h4'),
            ('h2', 'h3'),
            ('h2', 'h4'),
            ('h3', 'h4')
        ]),
        'linear': (create_linear_topology, [
            ('h1', 'h2'),
            ('h2', 'h3')
        ]),
        'heirarchical': (create_heirarchical_topology, [
            ('s1', 's2'),
            ('h1', 's1'),
            ('h2', 's2')
        ]),
        'tree': (create_tree_topology, [
            ('s1', 's2'),
            ('h1', 's1'),
            ('h2', 's2'),
            ('h3', 's2')
        ]),
        'distributed': (create_distributed_topology, [
            ('h1', 's1'),
            ('h2', 's1'),
            ('h3', 's2'),
            ('s1', 's2')
        ]),
        'hybrid1': (create_hybrid1_topology, [
            ('h1', 's1'),
            ('h2', 's1'),
            ('h3', 'h4'),
            ('h4', 's1'),
            ('h3', 's1')
        ]),
        'hybrid2': (create_hybrid2_topology, [
            ('h1', 's1'),
            ('h2', 's1'),
            ('h3', 's1'),
            ('h4', 'h3')
        ])
    }

    # Error parameters for injecting network errors
    error_params = {
        'packet_loss': '5%',  # 5% packet loss (as string with %)
        'latency': '50ms',     # 50ms latency (as string)
        'bandwidth': 10,       # 10 Mbps bandwidth (as integer)
        'jitter': '5ms'        # 5ms jitter (as string)
    }

    # Run the simulation for all topologies
    setLogLevel('info')  # Set Mininet log level
    for topology_name, (create_topology, edges) in topologies.items():
        run_simulation(create_topology, topology_name, edges, **error_params)
