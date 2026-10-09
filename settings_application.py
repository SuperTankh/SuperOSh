"""
    This file is the Settings application module. You can add your own virtual Wi-Fi networks. Version 3
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
        'current_wi_fi': Modify(text = 'Get a peek of nearby connections and be able to connect to them.', value = list[str](wi_fi_connections)[0], options = {name: name for name in wi_fi_connections}),
        'wi_fi': {
            name: {
                'automatic_connection': Modify(text = 'Connect automatically when in range.', value = True),
                'network_profile_type': Modify(text = 'With the public network, your device is not discoverable on the network. Use this in most cases. Use Private network if you need file sharing, and if you know and trust the people and devices on the network, because your device is discoverable.', value = 'Public network', options = {'Public network (recommended)': 'Public network', 'Private network (not recommended)': 'Private network'}),
                'metered_connection': Modify(text = 'Some applications might work differently to reduce data usage when you are connected to this network.', value = False),
                'data_duration': Modify(text = 'Select how much time in days a period should be.', value = 30, options = {'minimum': 1, 'type': int, 'maximum': inf}),
                'data_limit': Modify(text = f'How much data should be the maximum of {name}? Set to 0 to disable.', value = 100, options = {'minimum': 0, 'type': int, 'maximum': inf}),
                'data_unit': Modify(text = 'What unit should be set on the data limit?', value = 'MB', options = {'Byte': 'B', 'Kilobyte': 'KB', 'Megabyte': 'MB', 'Gigabyte': 'GB', 'Terabyte': 'TB'}),
                'random_hardware': Modify(text = 'Help protect your privacy by making it harder for people to track your device location when you connect to this network. The setting takes effect the next time you connect to this network.', value = 'Disabled', options = {'Disable': 'Disabled', 'Enable': 'Enabled', 'Change daily': 'Changes daily', 'Change each connection': 'Changes for each connection'}),
                'ip_assignment': Modify(text = 'Change if you want to change your IP settings manually, or automatically.', value = 'Automatic', options = {'Automatically (DHCP)': 'Automatic', 'Manually': 'Manual'}),
                'ip_ipv4_adress': Modify(text = 'Define the IP adress.', value = ''),
                'ip_ipv4_subnet': Modify(text = 'Define the subnet mask.', value = ''),
                'ip_ipv4_gateaway': Modify(text = 'Define the gateaway.', value = ''),
                'ip_ipv4_pdns': Modify(text = 'Define the preferred DNS.', value = ''),
                'ip_ipv4_phttps': Modify(text = 'How you want to use your DNS over HTTPS?', value = 'Disabled', options = {'Disable': 'Disabled', 'Enable (Automatic template)': 'Enabled automatically', 'Enable (Manual template)': 'Enabled manually'}),
                'ip_ipv4_phttpst': Modify(text = 'What is the template of the DNS? Only works on Manual HTTPS DNS mode.', value = ''),
                'ip_ipv4_ptext': Modify(text = 'Do you want to fall back to plaintext?', value = False),
                'ip_ipv4_adns': Modify(text = 'Define the preferred DNS.', value = ''),
                'ip_ipv4_ahttps': Modify(text = 'How you want to use your DNS over HTTPS?', value = 'Disabled', options = {'Disable': 'Disabled', 'Enable (Automatic template)': 'Enabled automatically', 'Enable (Manual template)': 'Enabled manually'}),
                'ip_ipv4_ahttpst': Modify(text = 'What is the template of the DNS? Only works on Manual HTTPS DNS mode.', value = ''),
                'ip_ipv4_atext': Modify(text = 'Do you want to fall back to plaintext?', value = False),
                'ip_ipv6_adress': Modify(text = 'Define the IP adress.', value = ''),
                'ip_ipv6_subnet': Modify(text = 'Define the subnet prefix length.', value = ''),
                'ip_ipv6_gateaway': Modify(text = 'Define the gateaway.', value = ''),
                'ip_ipv6_pdns': Modify(text = 'Define the preferred DNS.', value = ''),
                'ip_ipv6_phttps': Modify(text = 'How you want to use your DNS over HTTPS?', value = 'Disabled', options = {'Disable': 'Disabled', 'Enable (Automatic template)': 'Enabled automatically', 'Enable (Manual template)': 'Enabled manually'}),
                'ip_ipv6_phttpst': Modify(text = 'What is the template of the DNS? Only works on Manual HTTPS DNS mode.', value = ''),
                'ip_ipv6_ptext': Modify(text = 'Do you want to fall back to plaintext?', value = False),
                'ip_ipv6_adns': Modify(text = 'Define the preferred DNS.', value = ''),
                'ip_ipv6_ahttps': Modify(text = 'How you want to use your DNS over HTTPS?', value = 'Disabled', options = {'Disable': 'Disabled', 'Enable (Automatic template)': 'Enabled automatically', 'Enable (Manual template)': 'Enabled manually'}),
                'ip_ipv6_ahttpst': Modify(text = 'What is the template of the DNS? Only works on Manual HTTPS DNS mode.', value = ''),
                'ip_ipv6_atext': Modify(text = 'Do you want to fall back to plaintext?', value = False),
                'look_other_connections': Modify(text = 'Look for other wireless networks while connected to this network.', value = False),
                'ssid': Modify(text = 'Connect even if the network is not broadcasting its name.', value = False),
                'security_type': Modify(text = 'Change the security type of this network.', value = 'WPA3-Personal', options = {'No authentification (open)': 'No authentification', 'WPA3-Personal': '', 'WPA2-Personal': '', 'WPA2-Personal Entreprise': '', 'WPA3-Personal Entreprise': '', 'WPA3-Personal Entreprise 192 bits': '', '802.1X': ''}),
                'encryption_type': Modify(text = 'Change the encryption type of this network.', value = 'AES', options = {'AES': '', 'GCMP-256': ''})
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
                        'Data usage': lambda: information(text = f'The data usage for {Core.user.applications["Settings"]["current_wi_fi"].value()} is 0 {Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['data_unit'].value()}.'),
                        'Limit duration': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['data_duration'],
                        'Data limit': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['data_limit'],
                        'Limit unit': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['data_unit']
                    },
                    'Random hardware addresses': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['random_hardware'],
                    'IP assignment': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_assignment'],
                    'Manual IP & DNS': {
                        '.condition': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_assignment'].value() == 'Manual',
                        '.checkfail': 'IP is already assigned automatically.',
                        'IPv4': {
                            'IP adress': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_adress'],
                            'Subnet mask': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_subnet'],
                            'Gateaway': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_gateaway'],
                            'Preferred DNS': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_pdns'],
                            'DNS over HTTPS': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_phttps'],
                            'DNS over HTTPS template': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_phttpst'],
                            'DNS fallback to plaintext': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_ptext'],
                            'Alternative DNS': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_adns'],
                            'Alternative DNS over HTTPS': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_ahttps'],
                            'Alternative DNS over HTTPS template': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_ahttpst'],
                            'Alternative DNS fallback to plaintext': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv4_atext']
                        },
                        'IPv6': {
                            'IP adress': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_adress'],
                            'Subnet prefix length': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_subnet'],
                            'Gateaway': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_gateaway'],
                            'Preferred DNS': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_pdns'],
                            'DNS over HTTPS': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_phttps'],
                            'DNS over HTTPS template': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_phttpst'],
                            'DNS fallback to plaintext': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_ptext'],
                            'Alternative DNS': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_adns'],
                            'Alternative DNS over HTTPS': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_ahttps'],
                            'Alternative DNS over HTTPS template': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_ahttpst'],
                            'Alternative DNS fallback to plaintext': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ip_ipv6_atext']
                        }
                    },
                    'Dynamic check': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['look_other_connections'],
                    'Dynamic connection': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['ssid'],
                    'Security type': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['security_type'],
                    'Encryption type': lambda: Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['encryption_type'],
                    'Network informations': lambda: information(text = f'SSID: {Core.user.applications['Settings']['current_wi_fi'].value()}\nProtocol: Wi-Fi\nSecurity type: {Core.user.applications['Settings']['wi_fi'][Core.user.applications['Settings']['current_wi_fi'].value()]['encryption_type'].value()}')
                },
                'Show available networks': lambda: Core.user.applications['Settings']['current_wi_fi']
            }
        }
    }
}
