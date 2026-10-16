#!/usr/bin/env python3
import logging
import os
import subprocess

import speedtest  # For network speed test

# ANSI codes for custom color
RESET = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[32m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
RED = '\033[31m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_RED = '\033[91m'
BRIGHT_CYAN = '\033[96m'

# Command history
command_history = []

# Logging setup
logging.basicConfig(filename="network_tools.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    """Pause the script and wait for user input to continue."""
    input(f"{BRIGHT_YELLOW}Press Enter to continue...{RESET}")

def execute_command(command, success_message=None):
    """Execute a system command and log the result."""
    command_history.append(command)
    try:
        subprocess.run(command, shell=True, check=True)
        if success_message:
            logging.info(success_message)
            print(f"\n{BRIGHT_GREEN}{success_message}{RESET}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
        print(f"\n{BRIGHT_RED}Command failed: {e}{RESET}")

def get_input(prompt, min_value=None, max_value=None):
    """
    Get user input and handle 'q' to quit.
    If min_value and max_value are provided, validate numeric input.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'q':
            return 'q'
        if min_value is not None and max_value is not None:
            if user_input.isdigit() and min_value <= int(user_input) <= max_value:
                return int(user_input)
            print(f"{BRIGHT_RED}Invalid choice. Please enter a number between {min_value} and {max_value} or 'q' to quit.{RESET}")
        else:
            return user_input

def display_welcome_message():
    """Display a welcome message with futuristic ASCII art."""
    clear_screen()
    print(f"{BRIGHT_CYAN}{BOLD}")
    print("  ╭──────────────────────────────────────────────────────╮")
    print("  │                                                      │")
    print("  │    • ▌ ▄ ·.  ▪  .▄▄ ·  ▄▄▄·  ▄▄▄·  ▄▄▄·  ▄▄▄·  ▄▄▄·  │")
    print("  │    ·██ ▐███▪ ██ ▐█ ▀. ▐█ ▄█ ▐█ ▄█ ▐█ ▄█ ▐█ ▄█ ▐█ ▄█  │")
    print("  │    ▐█ ▌▐▌▐█· ▐█·▄▀▀▀█▄ ██▀·  ██▀·  ██▀·  ██▀·  ██▀·  │")
    print("  │    ██ ██▌▐█▌ ▐█▌▐█▄▪▐█ ▐█▪·• ▐█▪·• ▐█▪·• ▐█▪·• ▐█▪·• │")
    print("  │    ▀▀  █▪▀▀▀ ▀▀▀ ▀▀▀▀ .▀   .▀   .▀   .▀   .▀   .▀    │")
    print("  │                                                      │")
    print("  │    ▄▄▄▄▄ ▄ .▄ ▄▄▄· ▄▄▄▄▄ ▄▄▄· ▄▄▄▄▄ ▄▄▄· ▄▄▄▄▄ ▄▄▄·  │")
    print("  │    •██  ██▪▐█▐█ ▀█ •██  ▐█ ▀█ •██  ▐█ ▀█ •██  ▐█ ▀█  │")
    print("  │     ▐█.▪██▀▐█▄█▀▀█  ▐█.▪▄█▀▀█  ▐█.▪▄█▀▀█  ▐█.▪▄█▀▀█  │")
    print("  │     ▐█▌·██▌▐▀▐█ ▪▐▌ ▐█▌·▐█ ▪▐▌ ▐█▌·▐█ ▪▐▌ ▐█▌·▐█ ▪▐▌ │")
    print("  │     ▀▀▀ ▀▀▀ · ▀  ▀  ▀▀▀  ▀  ▀  ▀▀▀  ▀  ▀  ▀▀▀  ▀  ▀  │")
    print("  │                                                      │")
    print("  ╰──────────────────────────────────────────────────────╯")
    print(f"{RESET}")
    print(f"{GREEN}Welcome to the Network Tools Suite!{RESET}")
    print(f"{CYAN}Your gateway to mastering network management and troubleshooting.{RESET}")
    print(f"{YELLOW}Explore the tools below to diagnose, configure, and optimize your network.{RESET}")
    pause()

def display_main_menu():
    """Display the main menu."""
    clear_screen()
    print(f"{GREEN}{BOLD}Network Tools Menu:{RESET}")
    print(f"{CYAN}1. IP Configuration (ipconfig){RESET}")
    print(f"{CYAN}2. DNS Lookup (nslookup){RESET}")
    print(f"{CYAN}3. Traceroute (tracert){RESET}")
    print(f"{CYAN}4. Ping a Host{RESET}")
    print(f"{CYAN}5. Display ARP Table (arp){RESET}")
    print(f"{CYAN}6. Display Active Connections (netstat){RESET}")
    print(f"{CYAN}7. Show Network Routes (route){RESET}")
    print(f"{CYAN}8. Test Network Connection{RESET}")
    print(f"{CYAN}9. Network Speed Test{RESET}")
    print(f"{CYAN}10. Network Troubleshooting Wizard{RESET}")
    print(f"{CYAN}11. Reset Network Settings{RESET}")
    print(f"{CYAN}12. Save Output to File{RESET}")
    print(f"{CYAN}13. Search Command History{RESET}")
    print(f"{CYAN}14. Help Tooltips{RESET}")
    print(f"{RED}15. Exit (or press 'q' to quit){RESET}")

def ipconfig_menu():
    """Display the IP configuration menu."""
    while True:
        clear_screen()
        print(f"{YELLOW}IP Configuration Options:{RESET}")
        print("1. Basic IP Configuration")
        print("2. Detailed IP Configuration (/all)")
        print("3. Release IPv4 Address (/release)")
        print("4. Release IPv6 Address (/release6)")
        print("5. Renew IPv4 Address (/renew)")
        print("6. Renew IPv6 Address (/renew6)")
        print("7. Flush DNS Resolver Cache (/flushdns)")
        print("8. Register DNS (/registerdns)")
        print("9. Display DNS Resolver Cache (/displaydns)")
        print("10. Show Class IDs (/showclassid)")
        print("11. Set Class ID (/setclassid)")
        print("12. Show IPv6 Class IDs (/showclassid6)")
        print("13. Set IPv6 Class ID (/setclassid6)")
        print("14. Show All Compartments (/allcompartments)")
        print("15. Set Static IP Address (/set static)")
        print("16. Show DHCP Status (/showdhcp)")
        print(f"{RED}17. Exit to Main Menu (or press 'q' to quit){RESET}")
        choice = get_input(f"\n{BRIGHT_CYAN}Enter your choice: {RESET}", 1, 17)

        if choice == 'q':
            break
        commands = [
            "ipconfig",
            "ipconfig /all",
            "ipconfig /release",
            "ipconfig /release6",
            "ipconfig /renew",
            "ipconfig /renew6",
            "ipconfig /flushdns",
            "ipconfig /registerdns",
            "ipconfig /displaydns",
            "ipconfig /showclassid",
            "ipconfig /setclassid",
            "ipconfig /showclassid6",
            "ipconfig /setclassid6",
            "ipconfig /allcompartments",
            "ipconfig /showdhcp"
        ]

        if 1 <= choice <= 15:
            execute_command(commands[choice - 1], f"Running {commands[choice - 1]}...")
        elif choice == 16:
            ip_address = input("\nEnter the static IP address (e.g., 192.168.1.100): ")
            subnet_mask = input("\nEnter the subnet mask (e.g., 255.255.255.0): ")
            gateway = input("\nEnter the default gateway (e.g., 192.168.1.1): ")
            execute_command(f"netsh interface ipv4 set address name=\"Ethernet\" static {ip_address} {subnet_mask} {gateway}")
        elif choice == 17:
            break
        pause()

def nslookup_menu():
    """Display the DNS lookup menu."""
    while True:
        clear_screen()
        print(f"{YELLOW}DNS Lookup Options:{RESET}")
        print("1. Standard Lookup")
        print("2. Lookup CNAME Records (-type=CNAME)")
        print("3. Lookup NS Records (-type=NS)")
        print("4. Lookup MX Records (-type=MX)")
        print("5. Lookup AAAA Records (-type=AAAA)")
        print("6. Lookup PTR Records (-type=PTR)")
        print("7. Lookup SOA Records (-type=SOA)")
        print("8. Specify DNS Server for Lookup")
        print(f"{RED}9. Exit to Main Menu (or press 'q' to quit){RESET}")
        choice = get_input(f"\n{BRIGHT_CYAN}Enter your choice: {RESET}", 1, 9)

        if choice == 'q':
            break
        if choice == 1:
            domain = input("\nEnter the domain name or IP address: ")
            execute_command(f"nslookup {domain}", f"Running: nslookup {domain}")
        elif choice == 2:
            domain = input("\nEnter the domain name for CNAME lookup: ")
            execute_command(f"nslookup -type=CNAME {domain}", f"Running: nslookup -type=CNAME {domain}")
        elif choice == 3:
            domain = input("\nEnter the domain name for NS lookup: ")
            execute_command(f"nslookup -type=NS {domain}", f"Running: nslookup -type=NS {domain}")
        elif choice == 4:
            domain = input("\nEnter the domain name for MX lookup: ")
            execute_command(f"nslookup -type=MX {domain}", f"Running: nslookup -type=MX {domain}")
        elif choice == 5:
            domain = input("\nEnter the domain name for AAAA lookup: ")
            execute_command(f"nslookup -type=AAAA {domain}", f"Running: nslookup -type=AAAA {domain}")
        elif choice == 6:
            domain = input("\nEnter the domain name for PTR lookup: ")
            execute_command(f"nslookup -type=PTR {domain}", f"Running: nslookup -type=PTR {domain}")
        elif choice == 7:
            domain = input("\nEnter the domain name for SOA lookup: ")
            execute_command(f"nslookup -type=SOA {domain}", f"Running: nslookup -type=SOA {domain}")
        elif choice == 8:
            dns_server = input("\nEnter the DNS server address: ")
            domain = input("\nEnter the domain name for lookup: ")
            execute_command(f"nslookup {domain} {dns_server}", f"Running: nslookup {domain} {dns_server}")
        elif choice == 9:
            break
        pause()

def traceroute_menu():
    """Display the traceroute menu."""
    while True:
        clear_screen()
        print(f"{YELLOW}Traceroute Options:{RESET}")
        print("1. Standard Traceroute")
        print("2. Traceroute with Custom TTL (Time-To-Live)")
        print(f"{RED}3. Exit to Main Menu (or press 'q' to quit){RESET}")
        choice = get_input(f"\n{BRIGHT_CYAN}Enter your choice: {RESET}", 1, 3)

        if choice == 'q':
            break
        if choice == 1:
            host = input("\nEnter the host to trace: ")
            execute_command(f"tracert {host}", f"Running: tracert {host}")
        elif choice == 2:
            host = input("\nEnter the host to trace: ")
            ttl = input("\nEnter the TTL (default is 30): ")
            execute_command(f"tracert -h {ttl} {host}", f"Running: tracert -h {ttl} {host}")
        elif choice == 3:
            break
        pause()

def ping_menu():
    """Display the ping menu."""
    while True:
        clear_screen()
        print(f"{YELLOW}Ping Options:{RESET}")
        print("1. Standard Ping")
        print("2. Custom Ping (Specify packet size, count, and timeout)")
        print(f"{RED}3. Exit to Main Menu (or press 'q' to quit){RESET}")
        choice = get_input(f"\n{BRIGHT_CYAN}Enter your choice: {RESET}", 1, 3)

        if choice == 'q':
            break
        if choice == 1:
            host = input("\nEnter the host to ping: ")
            execute_command(f"ping {host}", f"Running: ping {host}")
        elif choice == 2:
            host = input("\nEnter the host to ping: ")
            size = input("\nEnter the packet size (bytes): ")
            count = input("\nEnter the number of packets to send: ")
            timeout = input("\nEnter the timeout in milliseconds: ")
            execute_command(f"ping {host} -l {size} -n {count} -w {timeout}", f"Running: ping {host} -l {size} -n {count} -w {timeout}")
        elif choice == 3:
            break
        pause()

def arp_menu():
    """Display the ARP table menu."""
    while True:
        clear_screen()
        print(f"{YELLOW}ARP Table Options:{RESET}")
        print("1. Display ARP Table")
        print("2. Add ARP Entry")
        print("3. Delete ARP Entry")
        print(f"{RED}4. Exit to Main Menu (or press 'q' to quit){RESET}")
        choice = get_input(f"\n{BRIGHT_CYAN}Enter your choice: {RESET}", 1, 4)

        if choice == 'q':
            break
        if choice == 1:
            execute_command("arp -a", "Running: arp -a")
        elif choice == 2:
            ip_address = input("\nEnter the IP address for the ARP entry: ")
            mac_address = input("\nEnter the MAC address for the ARP entry: ")
            execute_command(f"arp -s {ip_address} {mac_address}", f"Running: arp -s {ip_address} {mac_address}")
        elif choice == 3:
            ip_address = input("\nEnter the IP address to delete from ARP table: ")
            execute_command(f"arp -d {ip_address}", f"Running: arp -d {ip_address}")
        elif choice == 4:
            break
        pause()

def netstat_menu():
    """Display the netstat menu."""
    while True:
        clear_screen()
        print(f"{YELLOW}Netstat Options:{RESET}")
        print("1. Display Active Connections")
        print("2. Display Listening Ports (-an)")
        print("3. Display Routing Table (-r)")
        print("4. Display TCP Connections")
        print("5. Display UDP Connections")
        print(f"{RED}6. Exit to Main Menu (or press 'q' to quit){RESET}")
        choice = get_input(f"\n{BRIGHT_CYAN}Enter your choice: {RESET}", 1, 6)

        if choice == 'q':
            break
        if choice == 1:
            execute_command("netstat", "Running: netstat")
        elif choice == 2:
            execute_command("netstat -an", "Running: netstat -an")
        elif choice == 3:
            execute_command("netstat -r", "Running: netstat -r")
        elif choice == 4:
            execute_command("netstat -t", "Running: netstat -t")
        elif choice == 5:
            execute_command("netstat -u", "Running: netstat -u")
        elif choice == 6:
            break
        pause()

def route_menu():
    """Display the route menu."""
    while True:
        clear_screen()
        print(f"{YELLOW}Route Options:{RESET}")
        print("1. Show Network Routes")
        print("2. Add Route")
        print("3. Delete Route")
        print(f"{RED}4. Exit to Main Menu (or press 'q' to quit){RESET}")
        choice = get_input(f"\n{BRIGHT_CYAN}Enter your choice: {RESET}", 1, 4)

        if choice == 'q':
            break
        if choice == 1:
            execute_command("route print", "Running: route print")
        elif choice == 2:
            destination = input("\nEnter the destination IP address: ")
            subnet_mask = input("\nEnter the subnet mask: ")
            gateway = input("\nEnter the gateway IP address: ")
            execute_command(f"route add {destination} mask {subnet_mask} {gateway}", f"Running: route add {destination} mask {subnet_mask} {gateway}")
        elif choice == 3:
            destination = input("\nEnter the destination IP address to delete: ")
            execute_command(f"route delete {destination}", f"Running: route delete {destination}")
        elif choice == 4:
            break
        pause()

def test_network_connection():
    """Test network connectivity."""
    execute_command("ping 8.8.8.8 -n 4", "Testing network connection...")

def test_network_speed():
    """Test network speed using speedtest-cli."""
    try:
        print(f"\n{BRIGHT_GREEN}Testing network speed...{RESET}")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        print(f"\n{BRIGHT_GREEN}Download Speed: {download_speed:.2f} Mbps{RESET}")
        print(f"{BRIGHT_GREEN}Upload Speed: {upload_speed:.2f} Mbps{RESET}")
    except Exception as e:
        print(f"\n{BRIGHT_RED}Error: {e}{RESET}")
    pause()

def network_troubleshooting_wizard():
    """Guide users through common network troubleshooting steps."""
    print(f"\n{BRIGHT_GREEN}Starting Network Troubleshooting Wizard...{RESET}")
    print(f"{CYAN}1. Checking network connectivity...{RESET}")
    execute_command("ping 8.8.8.8 -n 4", "Testing connectivity to Google DNS...")
    print(f"{CYAN}2. Flushing DNS cache...{RESET}")
    execute_command("ipconfig /flushdns", "Flushing DNS cache...")
    print(f"{CYAN}3. Renewing IP address...{RESET}")
    execute_command("ipconfig /renew", "Renewing IP address...")
    print(f"{CYAN}4. Displaying active connections...{RESET}")
    execute_command("netstat -an", "Displaying active connections...")
    print(f"\n{BRIGHT_GREEN}Troubleshooting complete!{RESET}")
    pause()

def reset_network_settings():
    """Reset network settings (TCP/IP stack and Winsock)."""
    print(f"\n{BRIGHT_GREEN}Resetting network settings...{RESET}")
    execute_command("netsh int ip reset", "Resetting TCP/IP stack...")
    execute_command("netsh winsock reset", "Resetting Winsock...")
    print(f"\n{BRIGHT_GREEN}Network settings reset complete. Restart your computer to apply changes.{RESET}")
    pause()

def save_output_to_file():
    """Save the output of a command to a file."""
    command = input("\nEnter the command to save output for: ").strip()
    filename = input("\nEnter the filename to save output (e.g., output.txt): ").strip()
    try:
        with open(filename, "w") as f:
            subprocess.run(command, shell=True, check=True, stdout=f, text=True)
        print(f"\n{BRIGHT_GREEN}Output saved to {filename}{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"\n{BRIGHT_RED}Command failed: {e}{RESET}")
    pause()

def search_command_history():
    """Search the command history for specific commands."""
    search_term = input("\nEnter a term to search in command history: ").strip()
    matches = [cmd for cmd in command_history if search_term.lower() in cmd.lower()]
    if matches:
        print(f"\n{BRIGHT_GREEN}Matching commands:{RESET}")
        for i, cmd in enumerate(matches, 1):
            print(f"{i}. {cmd}")
    else:
        print(f"\n{BRIGHT_RED}No matching commands found.{RESET}")
    pause()

def display_help_tooltips():
    """Display tooltips for menu options."""
    clear_screen()
    print(f"{YELLOW}Help Tooltips:{RESET}")
    tooltips = {
        "ipconfig": "Displays or configures network interface settings.",
        "nslookup": "Queries DNS records for a domain or IP address.",
        "tracert": "Traces the route to a host.",
        "ping": "Tests connectivity to a host.",
        "arp": "Displays or modifies the ARP table.",
        "netstat": "Displays network connections and statistics.",
        "route": "Displays or modifies the network routing table.",
        "test_network_connection": "Tests internet connectivity.",
        "network_speed_test": "Tests network speed using speedtest-cli.",
        "network_troubleshooting_wizard": "Guides through common network troubleshooting steps.",
        "reset_network_settings": "Resets TCP/IP stack and Winsock.",
        "save_output_to_file": "Saves the output of a command to a file.",
        "search_command_history": "Searches the command history for specific commands.",
        "help_tooltips": "Displays tooltips for menu options."
    }
    for option, tooltip in tooltips.items():
        print(f"{BRIGHT_CYAN}{option}: {RESET}{tooltip}")
    pause()

def main():
    """Main function to run the program."""
    display_welcome_message()
    while True:
        display_main_menu()
        choice = get_input(f"\n{BRIGHT_CYAN}Enter your choice: {RESET}", 1, 15)

        if choice == 'q':
            print(f"\n{RED}Exiting program. Goodbye!{RESET}")
            break
        if choice == 1:
            ipconfig_menu()
        elif choice == 2:
            nslookup_menu()
        elif choice == 3:
            traceroute_menu()
        elif choice == 4:
            ping_menu()
        elif choice == 5:
            arp_menu()
        elif choice == 6:
            netstat_menu()
        elif choice == 7:
            route_menu()
        elif choice == 8:
            test_network_connection()
        elif choice == 9:
            test_network_speed()
        elif choice == 10:
            network_troubleshooting_wizard()
        elif choice == 11:
            reset_network_settings()
        elif choice == 12:
            save_output_to_file()
        elif choice == 13:
            search_command_history()
        elif choice == 14:
            display_help_tooltips()
        elif choice == 15:
            print(f"\n{RED}Exiting program. Goodbye!{RESET}")
            break

if __name__ == "__main__":
    main()
