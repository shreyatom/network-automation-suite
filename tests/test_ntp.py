"""test_ntp.py
Tests that NTP was configured correctly after running push_config.py
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

class TestNTPConfig:

    def test_ntp_server_8888_configured(self, device_conn):
        """Check NTP server 8.8.8.8 is in running config."""
        output = device_conn.send_command(
            'show running-config | include ntp'
        )
        assert 'ntp server 8.8.8.8' in output, \
            f"NTP server 8.8.8.8 not found! Got:\n{output}"

    def test_ntp_server_8844_configured(self, device_conn):
        """Check backup NTP server 8.8.4.4 is in running config."""
        output = device_conn.send_command(
            'show running-config | include ntp'
        )
        assert 'ntp server 8.8.4.4' in output, \
            f"NTP server 8.8.4.4 not found! Got:\n{output}"

    def test_ntp_associations_exist(self, device_conn):
        """Check NTP associations are forming."""
        output = device_conn.send_command('show ntp associations')
        assert '8.8' in output, \
            f"No NTP associations found:\n{output}"