"""nterface_monitor.py
This script watches interface states and alerts when anything changes.
"""

from netmiko import ConnectHandler
import time
import os
import sys

# find inventory.py in parent folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inventory import DEVICES, DEVICE_NAMES

POLL_INTERVAL = 30  # check every 30 seconds

def get_interface_states(conn):
    """
    Runs 'show ip interface brief' and returns a dictionary like:
    {
        'GigabitEthernet1': 'up',
        'GigabitEthernet2': 'down',
    }
    """
    output = conn.send_command('show ip interface brief')
    states = {}

    # loop through each line of output
    for line in output.splitlines()[1:]:  # skip the header line
        parts = line.split()
        if len(parts) >= 6:
            interface_name  = parts[0]   # e.g. GigabitEthernet1
            link_status     = parts[4]   # e.g. up or down
            states[interface_name] = link_status

    return states

# monitor only the first device
device = DEVICES[0]
name   = DEVICE_NAMES[0]

print("="*50)
print(f"INTERFACE MONITOR STARTED")
print("="*50)
print(f"Device:   {name} ({device['host']})")
print(f"Polling every {POLL_INTERVAL} seconds")
print(f"Press Ctrl+C to stop\n")

previous_states = {}

try:
    with ConnectHandler(**device) as conn:
        conn.enable()

        while True:
            # get current interface states
            current_states = get_interface_states(conn)
            timestamp = time.strftime('%H:%M:%S')

            # first poll — just show baseline
            if not previous_states:
                print(f"[{timestamp}] Baseline captured:")
                for iface, state in current_states.items():
                    status_icon = '✓' if state == 'up' else '✗'
                    print(f"  {status_icon}  {iface:<35} {state}")
                print()

            else:
                # compare current vs previous states
                changes_found = False

                for iface, state in current_states.items():
                    previous = previous_states.get(iface, 'unknown')

                    if previous != state:
                        changes_found = True

                        if state == 'up':
                            print(f"[{timestamp}] ✓ LINK UP   — {iface} came UP")
                        else:
                            print(f"[{timestamp}] ✗ LINK DOWN — {iface} went {state.upper()}")

                if not changes_found:
                    print(f"[{timestamp}] All interfaces stable — no changes detected")

            # save for next comparison
            previous_states = current_states

            # wait before next poll
            time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("\nMonitor stopped by user.")

except Exception as e:
    print(f"\nERROR: {e}")