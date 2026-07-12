"""test_connectivity.py
Tests that we can successfully SSH into each device.
"""

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from inventory import DEVICES, DEVICE_NAMES

@pytest.fixture(scope='module', params=DEVICES, ids=DEVICE_NAMES)
def device_conn(request):
    """
    This fixture:
    1. Connects to each device before tests run
    2. Passes the connection to each test
    3. Disconnects after all tests finish
    """
    conn = ConnectHandler(**request.param)
    conn.enable()
    yield conn          # test runs here
    conn.disconnect()   # runs after test finishes

class TestConnectivity:

    def test_ssh_connection(self, device_conn):
        """Test that SSH connection is working."""
        prompt = device_conn.find_prompt()
        assert prompt is not None
        assert len(prompt) > 0
        print(f"\n  Connected! Prompt: {prompt}")

    def test_in_enable_mode(self, device_conn):
        """Test that we are in enable mode (prompt ends with #)."""
        prompt = device_conn.find_prompt()
        assert prompt.endswith('#'), \
            f"Expected # prompt but got: {prompt}"

    def test_show_version_works(self, device_conn):
        """Test that show version command responds correctly."""
        output = device_conn.send_command('show version')
        assert 'Cisco' in output or 'IOS' in output, \
            f"Output does not look like Cisco IOS: {output[:100]}"