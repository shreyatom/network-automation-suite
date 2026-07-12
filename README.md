# Network Automation Suite
### Python + Netmiko + Pytest | Cisco IOS XE

Automates configuration management for a Cisco IOS XE network using Python
and Netmiko with a Pytest validation layer that verifies device state after
every change. Tested against a real Cisco Catalyst 8000v via Cisco DevNet.

---

## Topology
3 interface topology on Cisco Catalyst 8000v:
- GigabitEthernet1 — up
- GigabitEthernet2 — up
- GigabitEthernet3 — administratively down

---

## Tech Stack
| Tool         | Purpose                                    |
|--------------|--------------------------------------------|
| Python 3.13  | Core automation language                   |
| Netmiko 4.7  | SSH library for Cisco IOS device mgmt      |
| Pytest 9.1   | Validates config changes were applied      |
| Cisco DevNet | Free always-on real Cisco IOS XE sandbox   |

---

## Scripts
| Script                       | What it does                              |
|------------------------------|-------------------------------------------|
| scripts/backup_configs.py    | SSH backup of running-config              |
| scripts/push_config.py       | Push NTP/logging config to fleet          |
| scripts/interface_monitor.py | Real-time interface state monitoring      |

---

## Pytest Tests
| Test                          | What it verifies                          |
|-------------------------------|-------------------------------------------|
| tests/test_connectivity.py    | SSH connection and enable mode            |
| tests/test_ntp.py             | NTP servers configured correctly          |
| tests/test_interfaces.py      | Interface states and health               |

---

## How to Run

### 1. Clone the repo
git clone https://github.com/[your-username]/network-automation-suite.git
cd network-automation-suite

### 2. Install dependencies
pip install -r requirements.txt

### 3. Update inventory.py with your device credentials
DEVICES = [
    {'device_type': 'cisco_ios', 'host': 'YOUR_DEVICE_IP', ...}
]

### 4. Run a script
python scripts/backup_configs.py
python scripts/push_config.py

### 5. Run all tests
pytest tests/ -v

---

## Test Results
All 9 tests passing on real Cisco Catalyst 8000v (IOS XE 17.12):
- 3 connectivity tests
- 3 NTP config tests
- 3 interface state tests

---

## Project Background
Built to demonstrate network automation skills developed during a
Technical Apprenticeship at Cisco Systems, where Python and Pytest
were used for timing protocol (SyncE/PTP) test automation.