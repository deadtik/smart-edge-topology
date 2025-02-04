def add_network_errors(net, latency=None, packet_loss=None, bandwidth=None, jitter=None):
    """
    Add network errors to all links in the network.
    
    :param net: Mininet network object
    :param latency: Latency in milliseconds (e.g., '50ms')
    :param packet_loss: Packet loss percentage (e.g., '10%')
    :param bandwidth: Bandwidth limit in Mbps (e.g., 10)
    :param jitter: Jitter in milliseconds (e.g., '5ms')
    """
    for link in net.links:
        link_intf1 = link.intf1
        link_intf2 = link.intf2

        # Apply TC (Traffic Control) parameters
        tc_command = "tc qdisc add dev {intf} root netem"

        if latency:
            tc_command += f" delay {latency}"
        if jitter:
            tc_command += f" {jitter} distribution normal"
        if packet_loss:
            tc_command += f" loss {packet_loss}"
        if bandwidth:
            # Bandwidth is managed using 'tbf' qdisc
            rate = f"{bandwidth}mbit"
            burst = "32kbit"
            # Make sure to apply bandwidth to both interfaces
            for intf in (link_intf1, link_intf2):
                tc_command_with_bandwidth = tc_command + f" && tc qdisc add dev {intf} parent 1:1 handle 10: tbf rate {rate} burst {burst} latency 50ms"
                try:
                    intf.node.cmd(tc_command_with_bandwidth.format(intf=intf))
                except Exception as e:
                    print(f"Error applying traffic control to {intf}: {e}")
        else:
            # Apply to both interfaces of the link (without bandwidth)
            for intf in (link_intf1, link_intf2):
                try:
                    intf.node.cmd(tc_command.format(intf=intf))
                except Exception as e:
                    print(f"Error applying traffic control to {intf}: {e}")

