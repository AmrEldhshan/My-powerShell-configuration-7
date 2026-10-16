#!/usr/bin/env python3
from colorama import Fore, Style, init


def print_hacker_logo():
    # Initialize colorama to ensure compatibility with PowerShell
    init(autoreset=True)

    # Customizable logo with enhancements
    logo = f"""
{Fore.GREEN}{Style.BRIGHT}
   ╔══════════════════════════════════════════════════╗
   ║  ████████    ██        ██████   ██████  ██████  ║
   ║  ████████    ██        ██████   ██████  ██████  ║
   ║  ██████      ██        ██████   ██████  ██████  ║
   ║                                              ║
   ║  ██████████████████████████████████████████  ║
   ║  ███   {Fore.YELLOW}Welcome, TSOCIATY{Fore.GREEN}   ███   ║
   ║  ███   {Fore.YELLOW}Ethical Hacking Zone{Fore.GREEN}   ███   ║
   ║  ███   {Fore.YELLOW}Malware Analysis & Beyond{Fore.GREEN} ███   ║
   ║  ██████████████████████████████████████████  ║
   ║                                              ║
   ╚════════════════════════════════════════════════╝

{Fore.CYAN}{Style.BRIGHT}
=======================================================
           WELCOME TO TSOCIATY'S ZONE!
       {Fore.YELLOW}Analyze. Break. Secure. Repeat.{Fore.CYAN}
=======================================================
{Style.RESET_ALL}
    """
    print(logo)

if __name__ == "__main__":
    print_hacker_logo()

