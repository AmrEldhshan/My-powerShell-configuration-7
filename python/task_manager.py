#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
import time
from datetime import datetime

import psutil

# ANSI Color codes for main script output (not for fzf)
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"

def clear_screen():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")  # Clear screen for Windows
    else:
        os.system("clear")  # Clear screen for macOS/Linux

def get_process_list(sort_by="pid", filter_by=None, filter_value=None):
    """Collect a list of running processes with optional sorting and filtering."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'memory_info', 'cpu_percent', 'create_time']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            username = proc.info['username']
            status = proc.info['status']
            memory_usage = proc.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
            cpu_usage = proc.info['cpu_percent']
            create_time = datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S')

            # Skip if any critical field is None
            if pid is None or name is None or username is None or status is None:
                continue

            # Apply filtering
            if filter_by and filter_value:
                if filter_by == "status" and status != filter_value:
                    continue
                elif filter_by == "name" and filter_value.lower() not in name.lower():
                    continue
                elif filter_by == "username" and filter_value.lower() != username.lower():
                    continue

            # Format the process entry with proper spacing
            process_entry = (
                f"{pid:<8} | "  # PID (left-aligned, 8 characters)
                f"{name:<20} | "  # Name (left-aligned, 20 characters)
                f"{username:<15} | "  # Username (left-aligned, 15 characters)
                f"{status:<10} | "  # Status (left-aligned, 10 characters)
                f"{memory_usage:>8.2f} MB | "  # Memory usage (right-aligned, 8 characters)
                f"{cpu_usage:>6.1f}% | "  # CPU usage (right-aligned, 6 characters)
                f"{create_time}"  # Creation time
            )
            processes.append((pid, process_entry))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, KeyError):
            # Skip processes that are no longer running, inaccessible, or missing fields
            continue

    # Apply sorting
    if sort_by == "pid":
        processes.sort(key=lambda x: int(x[0]))
    elif sort_by == "name":
        processes.sort(key=lambda x: x[1].split('|')[1].strip().lower())
    elif sort_by == "memory":
        processes.sort(key=lambda x: float(x[1].split('|')[4].strip().split()[0]), reverse=True)
    elif sort_by == "cpu":
        processes.sort(key=lambda x: float(x[1].split('|')[5].strip().split('%')[0]), reverse=True)

    return [x[1] for x in processes]

def kill_process(pid):
    """Kill a process by its PID with colorful feedback."""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        print(f"{GREEN}Process {pid} terminated.{RESET}")
    except psutil.NoSuchProcess:
        print(f"{RED}Process {pid} does not exist.{RESET}")
    except psutil.AccessDenied:
        print(f"{RED}Access denied to terminate process {pid}.{RESET}")

def display_header(refresh_interval, sort_by, filter_by, filter_value):
    """Display a colorful header with dynamic information."""
    clear_screen()  # Clear the screen for dynamic updates
    # Display system metrics
    memory_info = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent()
    disk_usage = psutil.disk_usage('/').percent
    total_memory = memory_info.total / (1024 * 1024)  # Convert to MB
    used_memory = memory_info.used / (1024 * 1024)  # Convert to MB

    print(f"{BOLD}{BLUE}=== Process Manager ==={RESET}")
    print(f"{CYAN}Refresh Interval: {refresh_interval} seconds | Sort By: {sort_by} | Filter: {filter_by}={filter_value}{RESET}")
    print(f"{YELLOW}Memory Usage: {used_memory:.2f} MB / {total_memory:.2f} MB | CPU Usage: {cpu_usage:.1f}% | Disk Usage: {disk_usage:.1f}%{RESET}")
    print(f"{MAGENTA}Press 'q' to open options menu{RESET}")
    print(f"{MAGENTA}----------------------------------------{RESET}")

def options_menu():
    """Display the options menu and handle user input."""
    print(f"{BOLD}{BLUE}=== Options Menu ==={RESET}")
    print(f"{CYAN}1. Refresh Process List{RESET}")
    print(f"{CYAN}2. Save Current Output{RESET}")
    print(f"{CYAN}3. Kill Multiple Processes{RESET}")
    print(f"{CYAN}4. Export to CSV{RESET}")
    print(f"{CYAN}5. Quit{RESET}")
    choice = input(f"{CYAN}Enter your choice (1-5): {RESET}").strip()
    return choice

def save_process_list(processes):
    """Save the process list to a file."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"process_list_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write("\n".join(processes))
    print(f"{GREEN}Process list saved to {filename}.{RESET}")

def export_to_csv(processes):
    """Export the process list to a CSV file."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"process_list_{timestamp}.csv"
    with open(filename, 'w') as file:
        file.write("PID,Name,Username,Status,Memory Usage (MB),CPU Usage (%),Creation Time\n")
        for process in processes:
            file.write(process.replace(" | ", ",") + "\n")
    print(f"{GREEN}Process list exported to {filename}.{RESET}")

def kill_multiple_processes():
    """Kill multiple processes by their PIDs."""
    pids = input(f"{CYAN}Enter PIDs to kill (comma-separated): {RESET}").strip().split(',')
    for pid in pids:
        if pid.strip().isdigit():
            kill_process(int(pid.strip()))

def select_process_with_fzf(processes):
    """Use fzf to select a process from the list with custom formatting."""
    process_list = "\n".join(processes)
    result = subprocess.run(
        [
            "fzf",
            "--ansi",  # Enable ANSI color support
            "--height", "40%",
            "--reverse",
            "--color", "fg:#bbccdd,bg:#334455,hl:#ffcc00,fg+:#ffffff,bg+:#556677,hl+:#ffdd00",  # Custom colors
        ],
        input=process_list, text=True, capture_output=True
    )
    if result.returncode == 0:  # User selected a process
        return result.stdout.strip()
    return None  # No selection

def main():
    refresh_interval = 2  # Default refresh interval in seconds
    sort_by = "pid"  # Default sorting
    filter_by = None  # Default filter
    filter_value = None  # Default filter value

    while True:
        display_header(refresh_interval, sort_by, filter_by, filter_value)
        processes = get_process_list(sort_by, filter_by, filter_value)

        # Use fzf to select a process
        selected_process = select_process_with_fzf(processes)

        if selected_process:
            pid = int(selected_process.split('|')[0].strip())
            action = input(f"{CYAN}Selected PID: {pid}. Do you want to kill this process? (y/n): {RESET}").lower()

            if action == 'y':
                kill_process(pid)
                time.sleep(1)  # Pause to show feedback before refreshing
        else:
            # No process selected, check if the user wants to open the options menu
            user_input = input(f"{CYAN}Press 'q' to open options menu or any other key to continue: {RESET}").lower()
            if user_input == 'q':
                choice = options_menu()
                if choice == '1':
                    # Refresh process list
                    continue
                elif choice == '2':
                    # Save current output
                    save_process_list(processes)
                    time.sleep(1)  # Pause to show feedback before refreshing
                elif choice == '3':
                    # Kill multiple processes
                    kill_multiple_processes()
                    time.sleep(1)  # Pause to show feedback before refreshing
                elif choice == '4':
                    # Export to CSV
                    export_to_csv(processes)
                    time.sleep(1)  # Pause to show feedback before refreshing
                elif choice == '5':
                    # Quit
                    print(f"{RED}Exiting...{RESET}")
                    sys.exit(0)
                else:
                    print(f"{RED}Invalid choice.{RESET}")

        # Wait for the specified refresh interval
        time.sleep(refresh_interval)

if __name__ == "__main__":
    main()
