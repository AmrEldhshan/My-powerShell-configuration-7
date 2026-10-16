#!/usr/bin/env python3
import os

import pyshark


# Function to print in color
def print_in_color(text, color_code):
    """Print text in a specified color."""
    print(f"\033[{color_code}m{text}\033[0m")

# Function to display packet information
def display_packet_info(packet):
    """Display relevant packet information."""
    if hasattr(packet, 'ip'):
        print_in_color(f"Source IP: {packet.ip.src} -> Destination IP: {packet.ip.dst}", 32)  # Green
        print_in_color(f"Protocol: {packet.ip.proto}", 33)  # Yellow

        # If it's a TCP or UDP packet, display port numbers
        if hasattr(packet, 'tcp'):
            print_in_color(f"TCP Port: {packet.tcp.srcport} -> {packet.tcp.dstport}", 34)  # Blue
        elif hasattr(packet, 'udp'):
            print_in_color(f"UDP Port: {packet.udp.srcport} -> {packet.udp.dstport}", 34)  # Blue

# Function to start the sniffer
def start_sniffer(interface="Wi-Fi"):
    """Start sniffing packets on the specified interface."""
    print_in_color("Starting the network sniffer...", 35)  # Magenta
    print_in_color(f"Sniffing on interface: {interface}\n", 35)

    # Capture packets on the specified interface
    cap = pyshark.LiveCapture(interface=interface)
    cap.sniff(packet_count=10, prn=display_packet_info)  # Limit to 10 packets for simplicity

# Main function to run the sniffer
def main():
    """Main function to run the network sniffer."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen for readability

    print_in_color("Network Sniffer - Console Application", 36)  # Cyan
    print_in_color("Press Ctrl+C to stop sniffing\n", 36)

    interface = input("Enter the network interface to sniff (default Wi-Fi): ")
    if not interface:
        interface = "Wi-Fi"  # Default to Wi-Fi on Windows

    try:
        start_sniffer(interface)
    except KeyboardInterrupt:
        print_in_color("\nSniffer stopped. Exiting...", 31)  # Red
        exit(0)

if __name__ == "__main__":
    main()

