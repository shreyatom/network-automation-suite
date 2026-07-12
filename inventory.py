"""inventory.py
Loads device credentials from .env file
Never hardcode passwords — always use environment variables
"""

import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

DEVICES = [
    {
        'device_type': 'cisco_ios',
        'host':     os.getenv('DEVICE_HOST'),
        'username': os.getenv('DEVICE_USERNAME'),
        'password': os.getenv('DEVICE_PASSWORD'),
        'port':     int(os.getenv('DEVICE_PORT', 22)),
        'secret':   os.getenv('DEVICE_SECRET'),
        'timeout':  60,
    }
]

DEVICE_NAMES = ['DevNet-Cat8kv']