# utils/datacollected.py

from mininet.net import Mininet
import time

def collect_synthetic_data(net, bus):
    h1 = net.get('h1')
    h2 = net.get('h2')

    # Latency Test (Ping)
    latency_result = h1.cmd(f'ping -c 5 {h2.IP()}')
    latency = float(latency_result.split("\n")[-2].split("/")[4])  # Extract average latency in ms

    # Throughput Test (Iperf)
    h2.cmd('iperf -s &')  # Start Iperf server on h2
    time.sleep(1)  # Give some time for the server to start
    throughput_result = h1.cmd(f'iperf -c {h2.IP()} -t 10')
    throughput = float(throughput_result.split()[-2])  # Extract throughput value in Mbps

    # Packet Loss Test (Ping)
    packet_loss_result = h1.cmd(f'ping -c 100 {h2.IP()}')
    packet_loss = float(packet_loss_result.split("\n")[-3].split()[0].replace('%', ''))  # Extract packet loss %

    # Bandwidth
    bandwidth = throughput_result.split()[-2]  # Extract bandwidth

    # Jitter Test (Ping)
    jitter_result = h1.cmd(f'ping -c 10 {h2.IP()}')
    jitter = float(jitter_result.split("\n")[-2].split(" = ")[-1].split("/")[0])  # Extract jitter

    # Return the data in a dictionary format
    return {
        "topology": bus,
        "latency": latency,
        "throughput": throughput,
        "packet_loss": packet_loss,
        "bandwidth": bandwidth,
        "jitter": jitter
    }

