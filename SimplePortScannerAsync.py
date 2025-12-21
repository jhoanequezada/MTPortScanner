"""Port Scanner
A multi-threaded port scanner tool using socket and concurrent modules.
Allows rapid scanning of open and closed ports on a target IP.

Usage: Run the script following the prompts to specify host and port range"""

import socket
import concurrent.futures

#ANSI COLORS FOR OUTPUT
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_RESET = "\033[0m"


def get_port_name(port: int) -> str:
    '''Return port name, otherwise return Unknown for irrelevant ports'''
    try:
        return socket.getservbyport(port)
    except OSError as e:
        return "Unknown"


def check_connectivity(host: str, port: int, timeout=2):
    '''Main function, creates socket, attempts connection, calls get_port_name, appends connections to
    open or closed ports list based on if connection was successful'''
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    port_name = get_port_name(port)

    try:
        s.connect((host, port))
        open_ports.append([port, port_name])

    
    except (ConnectionRefusedError, OSError, socket.timeout):
        closed_ports.append([port, port_name])

    
    finally:
        s.close()


def order_lists():
    open_ports.sort()
    closed_ports.sort()


def output_table(open_ports, closed_ports) -> None:
    '''This just outpuits the final table that shows all open and closed ports in a table'''
    print(f"\n{'-'*65}")
    print(f"{'OPEN PORTS':<30} | {'CLOSED PORTS':<30}")
    print('-'*65)

    max_length = max(len(open_ports), len(closed_ports))

    for i in range(max_length):
        #Get open port if available
        if i < len(open_ports):
            #Formatting string: "Port: Name"
            o_str = f"{open_ports[i][0]}: {open_ports[i][1]}"
            #Add green color and format like cell
            o_cell = f"{COLOR_GREEN}{o_str:<30}{COLOR_RESET}"
        else:
            #Empty cell if no more open ports
            o_cell = f"{' ':<30}"
        #Get closed port if available
        if i < len(closed_ports):
            #Formatting string "Port: Name"
            c_str = f"{closed_ports[i][0]}: {closed_ports[i][1]}"
            #Add red color and format like cell
            c_cell = f"{COLOR_RED}{c_str:<30}{COLOR_RESET}"
        else:
            #Empty cell
            c_cell = ""

        #Print row
        print(f"{o_cell} | {c_cell}")


if __name__ == "__main__":
    try:
        host = str(input("Enter the IP you want to scan: "))
        ports = int(input("Please enter up to what port you want to scan: "))
    except ValueError:
        exit()

    open_ports = []
    closed_ports = []

    #Multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        tasks = [executor.submit(check_connectivity, host, port, 2) for port in range(ports + 1)]

    order_lists()
    output_table(open_ports, closed_ports)

