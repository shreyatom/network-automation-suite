"""backup_configs.py
This script connects to each router via SSH and saves the config to a file.
"""

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from datetime import datetime
import os
import sys

# find inventory.py in parent folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inventory import DEVICES, DEVICE_NAMES

# create backups folder if it doesn't exist
os.makedirs('backups', exist_ok=True)

# timestamp for filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M')

# track results
results = []

# loop through every device
for i, device in enumerate(DEVICES):
    name = DEVICE_NAMES[i]
    print(f"\nConnecting to {name} ({device['host']})...")

    try:
        # connect to device via SSH
        with ConnectHandler(**device) as conn:

            # enable mode
            conn.enable()

            # get hostname from prompt
            hostname = conn.find_prompt().strip('#>')

            # run 'show running-config' and save output
            print(f"  Pulling running-config...")
            config = conn.send_command('show running-config')

            # save to file
            filename = f"backups/{hostname}_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write(f"! Backup of {hostname}\n")
                f.write(f"! Date: {datetime.now()}\n")
                f.write(f"! Device IP: {device['host']}\n")
                f.write("!" + "="*50 + "\n")
                f.write(config)

            print(f"  Saved to: {filename}")
            results.append({'device': name, 'status': 'SUCCESS', 'file': filename})

    except NetmikoTimeoutException:
        # device did not respond
        print(f"  TIMEOUT — {name} did not respond")
        results.append({'device': name, 'status': 'TIMEOUT', 'file': None})

    except NetmikoAuthenticationException:
        # wrong username or password
        print(f"  AUTH FAILED — check username/password for {name}")
        results.append({'device': name, 'status': 'AUTH_FAIL', 'file': None})

    except Exception as e:
        # any other error
        print(f"  ERROR — {name}: {e}")
        results.append({'device': name, 'status': f'ERROR', 'file': None})

# print summary report 
print("\n" + "="*50)
print("BACKUP SUMMARY")
print("="*50)
for r in results:
    icon = '✓' if r['status'] == 'SUCCESS' else '✗'
    print(f"  {icon}  {r['device']:<25} {r['status']}")
    if r['file']:
        print(f"       File: {r['file']}")

success = sum(1 for r in results if r['status'] == 'SUCCESS')
print(f"\nResult: {success}/{len(results)} devices backed up successfully")