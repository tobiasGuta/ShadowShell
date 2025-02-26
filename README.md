# ShadowShell
A simple SSH server for Windows, with integrated Windows Firewall management.

## Features

* **Remote Command Execution:** Execute system commands remotely via SSH.
* **Windows Firewall Integration:** Easily add or disable firewall rules for SSH access.
* **Customizable Prompt:** Provides a user-friendly and informative command prompt.
* **Simple Setup:** Quick and easy to get started.
* **Cross-Platform Compatibility:** While optimized for Windows, it can run on other platforms with Python.

## Usage

### Prerequisites

* Python 3.6 or later.
* `paramiko` library (install with `pip install paramiko`).

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/tobiasGuta/ShadowShell.git
    cd ShadowShell
    ```

2.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running ShadowShell

* To start ShadowShell with the Windows Firewall rule enabled (default):

    ```bash
    python shadowshell.py
    ```

* To start ShadowShell without the Windows Firewall rule:

    ```bash
    python shadowshell.py -f n
    ```
    
    ```bash
    py .\server.py -f n
    INFO:root:[*] Firewall rule not added. Ensure port 2222 is open manually.
    INFO:root:[*] Starting SSH server on 0.0.0.0:2222...
    INFO:root:[*] Connection received from ip:port
    INFO:paramiko.transport:Connected (version 2.0, client OpenSSH_9.2p1)
    INFO:paramiko.transport:Auth rejected (none).
    INFO:paramiko.transport:Auth granted (password).
    INFO:root:[*] Authenticated! Shell ready.
    ```

### Connecting to ShadowShell

1.  Find the IP address of the machine running ShadowShell.
2.  Use an SSH client (e.g., PuTTY, OpenSSH) to connect to the IP address on port `2222` (or the port you configured).
3.  Use the username `changeme` and the password `changeme` (change these immediately).

## Security Considerations

**Important:** ShadowShell should be used responsibly and only in authorized environments.

* **Change Default Credentials:** Immediately change the default username and password.
* **Firewall Rules:** Be aware of the risks associated with opening ports in your firewall.
* **Network Security:** Ensure your network is secure to prevent unauthorized access.
* **Use Strong Passwords:** Use strong, unique passwords.
