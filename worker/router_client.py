import json
import os

import ntc_templates
from netmiko import ConnectHandler


def get_interfaces(ip, username, password):
    os.environ["NET_TEXTFSM"] = os.path.join(
        os.path.dirname(ntc_templates.__file__),
        "templates",
    )

    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "conn_timeout": 10,
        "auth_timeout": 10,
        "banner_timeout": 10,
    }

    with ConnectHandler(**device) as connection:
        # The lab router already provides a privileged EXEC prompt (#).
        # Therefore, do not call conn.enable() here.
        interfaces = connection.send_command(
            "show ip interface brief",
            use_textfsm=True,
        )

    print(json.dumps(interfaces, indent=2), flush=True)
    return interfaces
