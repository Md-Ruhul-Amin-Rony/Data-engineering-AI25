"""Example 1 — the smallest thing worth containerising.

No dependencies on purpose: nothing to install, nothing to blame.
"""

import os
import platform
import socket

print("Hello from inside a container. 🐳")
print(f"hostname : {socket.gethostname()}")
print(f"python   : {platform.python_version()}")
print(f"os       : {platform.platform()}")
print(f"user     : {os.environ.get('USER', 'root')}")
print()
print("That hostname is not your machine. That is the whole idea.")
