"""
    This file is the Settings application module. You can add your own virtual Wi-Fi networks. Version 2
"""
from typing import Any
from math import inf
from main import Core, information, Modify

wi_fi_connections: dict[str, str] = {
    'Alfrhoused': 'StopTryingToGetMyWiFi!',
    'Ackerman': '1234abcd'
}

application: dict[str, Any] = {
    'name': 'Settings',
    'description': 'The Settings application is where you change your device preferences and system configurations.',
    'version': {'major': 9, 'minor': 0, 'patch': 1},
    'visual': '⚙️',
    'developer': 'SuperOSh',
    'age': 0,
    'initialisation': {
        'current_wi_fi': Modify(text = 'Get a peek of nearby connections and be able to connect to them.', value = list(wi_fi_connections)[0], options = {name: name for name in wi_fi_connections}),
        'wi_fi': {
            name: {
                'automatic_connection': Modify(text = 'Connect automatically when in range.', value = True),
                'network_profile_type': Modify(text = 'With the public network, your device is not discoverable on the network. Use this in most cases. Use Private network if you need file sharing, and if you know and trust the people and devices on the network, because your device is discoverable.', value = 'Public network', options = {'Public network (recommended)': 'Public network', 'Private network (not recommended)': 'Private network'}),
                'metered_connection': Modify(text = 'Some applications might work differently to reduce data usage when you are connected to this network.', value = False),
                'data_duration': Modify(text = 'Select how much time in days a period should be.', value = 30, options = {'minimum': 1, 'type': int, 'maximum': inf}),
                'data_limit': Modify(text = f'How much data should be the maximum of {name}? Set to 0 to disable.', value = 100, options = {'minimum': 0, 'type': int, 'maximum': inf}),
                'data_unit': Modify(text = 'What unit should be set on the data limit?', value = 'MB', options = {'Byte': 'B', 'Kilobyte': 'KB', 'Megabyte': 'MB', 'Gigabyte': 'GB', 'Terabyte': 'TB'})
            }
            for name in wi_fi_connections
        }
    },
    'main': {
'.description': 'Welcome in the Settings! You can change your device preferences and system configurations as you want.',
'Network': {
    'Internet': {
        'Wi-Fi': lambda: Core.user.settings.wi_fi,
        'Current Wi-Fi properties': {
            '.name': lambda: Core.user.applications['Settings']['current_wi_fi'].value(),
            '.description': 'These settings only apply to the current network.',
            '.condition': lambda: Core.user.settings.wi_fi,
            '.checkfail': 'Connect to a Wi-Fi connection first.',
            'Wi-Fi network password': lambda: information(text = f'The password is {wi_fi_connections[Core.user.applications["Settings"]["current_wi_fi"].value()]} for this Wi-Fi network.'),
            'Automatic connection': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['automatic_connection'],
            'Network profile type': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['network_profile_type'],
            'Metered connection': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['metered_connection'],
            'Data': {
                'Data usage': lambda: information(text = f'The data usage for {Core.user.applications["Settings"]["current_wi_fi"].value()} is 0 Mb.'),
                'Limit duration': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['data_duration'],
                'Data limit': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['data_limit'],
                'Limit unit': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['data_unit'],
            }
        },
        'Show available networks': lambda: Core.user.applications['Settings']['current_wi_fi']
    }
}
    }
}
