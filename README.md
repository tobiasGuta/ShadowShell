# ShadowShell
A simple SSH server for Windows, with integrated Windows Firewall management.



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
