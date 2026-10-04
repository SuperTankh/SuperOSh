"""
    This file is the Settings application module.
"""
from typing import Any
from main import Core, information, Modify

wi_fi_connections: dict[str, dict[str, str]] = {
    'Alfrhoused': {
        'password': 'Ohhhh oh ohohh oh ohohh ohohh ohohhhh',
    }
}

application: dict[str, Any] = {
    'name': 'Settings',
    'description': 'The Settings application is where you change your device preferences and system configurations.',
    'version': {'major': 9, 'minor': 0, 'patch': 1},
    'visual': '⚙️',
    'developer': 'SuperOSh',
    'age': 0,
    'initialisation': {
        'current_wi_fi': 'Alfrhoused',
        'wi_fi_connections': ['Alfrhoused'],
        'automatic_connection': Modify(text = 'Connect automatically when in range.', value = True),
        'network_profile_type': Modify(text = 'With the public network, your device is not discoverable on the network. Use this in most cases. Use Private network if you need file sharing, and if you know and trust the people and devices on the network, as your device is discoverable.', value = 'Public network', options = {'Public network (recommended)': 'Public network', 'Private network (not recommended)': 'Private network'})
    },
    'main': {
        '.description': 'Welcome in the Settings! You can change your device preferences and system configurations as you want.',
        'Network': {
            'Internet': {
                'Wi-Fi': lambda: Core.user.settings.wi_fi,
                'Current Wi-Fi properties': {
                    '.name': lambda: Core.user.applications['Settings']['current_wi_fi'],
                    '.description': 'These settings only apply to the current network.',
                    '.condition': lambda: Core.user.settings.wi_fi,
                    '.checkfail': 'Connect to a Wi-Fi connection first.',
                    'Wi-Fi network password': lambda: information(text = f'The password is {wi_fi_connections[Core.user.applications['Settings']['current_wi_fi']]['password']} for this Wi-Fi network.'),
                    'Automatic connection': lambda: Core.user.applications['Settings']['automatic_connection'],
                    'Network profile type': lambda: Core.user.applications['Settings']['network_profile_type']
                }
            }
        }
    }
}
