"""push_config.py
This script pushes configuration commands to all devices at once.
"""

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os
import sys

# find inventory.py in parent folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inventory import DEVICES, DEVICE_NAMES

NTP_COMMANDS = [
    'ntp server 8.8.8.8',
    'ntp server 8.8.4.4',
]

LOGGING_COMMANDS = [
    'logging buffered 16384',
    'logging console warnings',
]

# combine all commands into one list
COMMANDS_TO_PUSH = NTP_COMMANDS + LOGGING_COMMANDS

print("="*50)
print("CONFIG PUSH STARTING")
print("="*50)
print(f"Pushing {len(COMMANDS_TO_PUSH)} commands to {len(DEVICES)} device(s)")
print("\nCommands to push:")
for cmd in COMMANDS_TO_PUSH:
    print(f"  → {cmd}")
print()

# track results 
results = []

# loop through every device 
for i, device in enumerate(DEVICES):
    name = DEVICE_NAMES[i]
    print(f"Configuring {name} ({device['host']})...")

    try:
        with ConnectHandler(**device) as conn:

            # enable mode
            conn.enable()

            # send_config_set() automatically:
            # 1. Types 'configure terminal'
            # 2. Sends each command one by one
            # 3. Types 'end' when finished
            output = conn.send_config_set(COMMANDS_TO_PUSH)

            # save config to NVRAM
            conn.save_config()

            print(f"  Config applied and saved successfully!")
            results.append({'device': name, 'status': 'SUCCESS'})

    except NetmikoTimeoutException:
        print(f"  TIMEOUT — {name} did not respond")
        results.append({'device': name, 'status': 'TIMEOUT'})

    except NetmikoAuthenticationException:
        print(f"  AUTH FAILED — check credentials for {name}")
        results.append({'device': name, 'status': 'AUTH_FAIL'})

    except Exception as e:
        print(f"  ERROR — {name}: {e}")
        results.append({'device': name, 'status': 'ERROR'})

# print summary 
print("\n" + "="*50)
print("PUSH SUMMARY")
print("="*50)
for r in results:
    icon = '✓' if r['status'] == 'SUCCESS' else '✗'
    print(f"  {icon}  {r['device']:<25} {r['status']}")

success = sum(1 for r in results if r['status'] == 'SUCCESS')
print(f"\nResult: {success}/{len(results)} devices configured successfully")