"""test_interfaces.py
Tests that interfaces are in expected states.
"""

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from netmiko import ConnectHandler
from inventory import DEVICES, DEVICE_NAMES

@pytest.fixture(scope='module', params=DEVICES, ids=DEVICE_NAMES)
def device_conn(request):
    conn = ConnectHandler(**request.param)
    conn.enable()
    yield conn
    conn.disconnect()

class TestInterfaces:

    def test_at_least_one_interface_up(self, device_conn):
        """Check at least one interface is up."""
        output = device_conn.send_command('show ip interface brief')
        up_interfaces = [
            line for line in output.splitlines()
            if 'up' in line.lower()
        ]
        assert len(up_interfaces) > 0, \
            "No interfaces are up! Something is wrong."

    def test_no_err_disabled_interfaces(self, device_conn):
        """Check no interfaces are err-disabled."""
        output = device_conn.send_command('show ip interface brief')
        err_disabled = [
            line for line in output.splitlines()
            if 'err-disabled' in line
        ]
        assert len(err_disabled) == 0, \
            f"Found err-disabled interfaces:\n" + '\n'.join(err_disabled)

    def test_show_interfaces_responds(self, device_conn):
        """Check show interfaces command works."""
        output = device_conn.send_command('show interfaces')
        assert len(output) > 100, \
            "show interfaces output too short — something is wrong"