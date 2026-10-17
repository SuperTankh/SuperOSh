"""
    This file englobes all the classes, variables, and functions of the OS. Version 0.2.3
"""
from datetime import datetime
from copy import deepcopy
from time import sleep
from typing import Any, Union
from pathlib import Path
from importlib import util
from sys import modules
from contextlib import contextmanager

class Modifiable:
    """
        Stores a text, a value, and sometimes options, which can be changed with modify().
    """
    def __init__(self, text: str, value: Any, options: Union[dict[str, Union[str, int, float, type]], None] = None) -> None:
        """
            Stores the value and the text in this instance.

            Parameters:
                self (Modifiable): The instance.
                text (str): The text that will be shown in the interface.
                value (Any): The default value of the instance.

            Returns:
                Nothing.
        """
        self.text: str = text
        if not isinstance(value, (bool, list, int, float, str)):
            value = str(value)
        self.__value: Union[bool, list[str], int, float, str] = value
        self.options: dict[str, Union[str, int, float, type]] = options if options is not None else {}

    def value(self) -> Any:
        """
            Gets the value of the instance.

            Parameters:
                self (Modifiable): The instance.

            Returns:
                The value of the instance.
        """
        return self.__value

    def modify(self) -> None:
        """
            Allows the user to change the value of the instance with a user-friendly interface.

            Parameters:
                self (Modifiable): The instance whose value will be changed.

            Returns:
                Nothing
        """
        new_value: Any = ''
        branches: str = (' - '.join(branch for branch in Core.choices)) + '\n' if Core.choices else ''
        text: str = f'{branches}{self.text} To abort, enter {Core.user.abort}.\n'
        while True:
            if isinstance(self.__value, bool):
                displayed_value: str = 'Enabled' if self.__value else 'Disabled'
                new_value = interface(text = f'{self.text}\n{Core.choices[-1]}: {displayed_value}', elements = ['Enable', 'Disable'])
                new_value = True if new_value == 'Enable' else False if new_value == 'Disable' else new_value
            elif isinstance(self.__value, list):
                value_elements: str = ', '.join(element for element in self.__value)
                value: str = f'{Core.choices[-1]}: {value_elements}'
                chosen_choice = interface(text = f'{self.text}\n{value}', elements = [str(element) for element in self.options.keys()])
                if chosen_choice != Core.user.abort:
                    if chosen_choice in self.__value:
                        new_value = self.__value
                        new_value.remove(chosen_choice)
                    else:
                        new_value = self.__value
                        new_value.append(chosen_choice)
                else:
                    new_value = Core.user.abort
            elif isinstance(self.__value, (int, float)):
                new_minimum: Union[int, float] = self.options['minimum'] if isinstance(self.options['minimum'], (int, float)) else 0
                new_type: type = self.options['type'] if isinstance(self.options['type'], type) else float
                new_maximum: Union[int, float] = self.options['maximum'] if isinstance(self.options['maximum'], (int, float)) else 100
                number_text: str = f'{text}{Core.choices[-1]}: {self.__value}'
                new_value = quantify(text = number_text, minimum = new_minimum, category = new_type, maximum = new_maximum)
            else:
                value: str = f'{Core.choices[-1]}: {self.__value}'
                if self.options:
                    new_value = interface(text = f'{self.text}\n{value}', elements = [str(element) for element in self.options.keys()])
                    if new_value != Core.user.abort:
                        if self.options[new_value] != '':
                            new_value = self.options[new_value]
                else:
                    new_value = write(text = f'{text}{Core.choices[-1]}: {self.__value}')
            if new_value == Core.user.abort:
                break
            if new_value != '':
                self.__value = new_value

class User:
    """
        Stores the data of a user account.
    """
    def __init__(self, username: str, user_password: str, user_role: str) -> None:
        """
            Initialises account data.

            Parameters:
                username (str): The username of the account.
                user_password (str): The password of the account.
                user_role (str): The permissions role of the account.

            Returns:
                Nothing.
        """
        self.username: str = username
        self.__password: str = user_password
        self.role: str = user_role
        self.new: bool = True
        self.applications: dict[str, Any] = {}
        self.name: str = 'User'
        self.age: int = 16
        self.positive: str = 'Yes'
        self.negative: str = 'No'
        self.next_page: str = 'Next page'
        self.previous_page: str = 'Previous page'
        self.abort: str = 'Abort'
        self.password_reminder: bool = True
        self.movement_keys: dict[str, list[str]] = {
            'up': [],
            'down': [],
            'right': [],
            'left': []
        }
        self.home_screen_order: list[Union[str, dict[str, Union[list[str], str]]]] = []
        self.wi_fi: Modifiable = Modifiable('Connect, manage known networks, metered network.', False)

    def is_password(self, entered_password: str) -> bool:
        """
            Verifies if the entered password is the same as the user password.

            Parameters:
                self (User): The user account data.
                entered_password (str): The entered password to verify.

            Returns:
                A boolean.
        """
        return entered_password == self.__password

    def get_password(self) -> str:
        """
            Get the account password only if the current user is the user or an Administrator, and if the user enabled password_reminder.

            Parameters:
                self (User): The user account data.

            Returns:
                The password of the current user.
        """
        return self.__password if (Core.user.role == 'Administrator' or Core.user == self) and self.password_reminder else ''

class Core:
    """
        Stores boring, but important variables.
    """
    keyboard_control: bool = False
    users: dict[str, User] = {
        'AlfredTheAdmin': User(
            username = 'AlfredTheAdmin',
            user_password = 'WhyAreYouTryingToLogInMyAccount?',
            user_role = 'Administrator'
        )
    }
    user: User = users['AlfredTheAdmin']
    applications: dict[str, dict[str, Any]] = {}
    choices: list[str] = []
    indexes: list[list[int]] = []

class Unique:
    """
        Stores variables that can only be changed in an Administrator account.
    """
    device_name: str = 'SuperDeviceh'
    lock_screen_timeout: float = 4.0
    lock_screen_time: bool = True

DIGITS: tuple[str] = tuple[str]('0123456789')
LOWERCASES: tuple[str] = tuple[str]('abcdefghijklmnopqrstuvwxyz')
UPPERCASES: tuple[str] = tuple[str]('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
PUNCTUATIONS: tuple[str] = tuple[str](' \"\'!:;,?./')
SYMBOLS: tuple[str] = tuple[str]('#$%&()*+-<=>@[\\]^_`{|}~')
CHARACTERS: tuple[str, str, str, str, str] = (*LOWERCASES, *UPPERCASES, *PUNCTUATIONS, *SYMBOLS, *DIGITS)

try:
    from msvcrt import kbhit, getwch
    Core.keyboard_control = True
except ModuleNotFoundError:
    def kbhit() -> bool:
        """
            Is the puppet replacement for kbhit(). Does nothing interesting.

            Parameters:
                Nothing.

            Returns:
                A boolean: Always False.
        """
        return False
    def getwch() -> str:
        """
            Is the puppet replacement for getwch(). Does nothing interesting.

            Parameters:
                Nothing.

            Returns:
                A string: The Enter character.
        """
        return '\r'

@contextmanager
def indexation(choice: str = ''):
    """
        Creates a new index level instead of manually appending and deleting the index values.

        Parameters:
            choice (str): The choice that will be added in the choices tree.

        Returns:
            Nothing.
    """
    Core.indexes.append([])
    if choice:
        Core.choices.append(choice)
    try:
        yield
    finally:
        del Core.indexes[-1]
        if choice:
            del Core.choices[-1]

def show(text: str) -> None:
    """
        Clears the terminal and shows a text, replaces print().

        Parameters:
            text (str): The text that will be printed in the terminal

        Returns:
            Nothing.
    """
    print(f'\033c{text}')

def write(text: str) -> str:
    """
        Shows a text and awaits an input that only has allowed characters and returns it, replaces input().

        Parameters:
            text (str): The text that will be shown.

        Returns:
            The string input that only includes allowed characters.
    """
    error: str = ''
    while True:
        show(text = f'{error}{text}')
        answer: str = input('>>> ')
        if all(element in CHARACTERS for element in answer):
            return answer
        error = 'Input includes unrecognised character.\n'

def information(text: str) -> None:
    """
        Shows a text and awaits any input to continue.

        Parameters:
            text (str): The text that will be shown.

        Returns:
            Nothing.
    """
    if Core.keyboard_control:
        show(text = f'{text}\nInput anything to continue.')
        getwch()
    else:
        write(text = f'{text}\nEnter to continue.')

def interface(text: str, elements: list[str]) -> str:
    """
        Is the main function to display multiple choices, and only exit once anything has been chosen.

        Parameters:
            text (str): The text that will be shown.
            elements (list[str]): All possible choices in a raw list.

        Returns:
            The chosen string element in the list, abort is part of the list and can also be returned.
    """
    pages: list[list[str]] = []
    page_index: int = 0
    elements_index: list[int] = [0]*(((len(elements)-1)//8)+1) if (not Core.indexes) or (not Core.indexes[-1]) else Core.indexes[-1]
    elements = list(elements)
    elements.insert(0, Core.user.abort)
    while len(elements) > 0:
        pages.append([*elements[0:9]])
        del elements[0:9]
        if len(elements) > 0:
            pages[-1].append(Core.user.next_page)
            elements.insert(0, Core.user.previous_page)
    del elements
    while True:
        current_page: list[str] = pages[page_index]
        current_page[elements_index[page_index]] += ' <--'
        enumeration: str = '\n'.join(f'{digit}. {element}' for digit, element in enumerate[str](current_page))
        branches: str = (' - '.join(branch for branch in Core.choices)) + '\n' if Core.choices else ''
        interface_text: str = branches + (text + '\n' if text else '') + enumeration
        if Core.keyboard_control:
            show(text = interface_text)
            action: str = getwch()
        else:
            action: str = write(text = interface_text)
        current_page[elements_index[page_index]] = current_page[elements_index[page_index]][:-4]
        if action in [*DIGITS] + (['\r', '\b'] if Core.keyboard_control else ['']):
            choice: int = int(action) if action in DIGITS else 0 if action == '\b' else elements_index[page_index]
            if choice == 9:
                action = Core.user.next_page
            elif choice == 0:
                action = Core.user.abort if page_index == 0 else Core.user.previous_page
            elif 1 <= choice <= 8 and choice <= len(current_page) - 1:
                action = current_page[choice]
            else:
                action = ''
        if (action in [*Core.user.movement_keys['right'], Core.user.next_page]) and page_index < len(pages)-1:
            page_index += 1
        elif (action in [*Core.user.movement_keys['left'], Core.user.previous_page]) and page_index > 0:
            page_index -= 1
        elif (action in Core.user.movement_keys['up']) and (elements_index[page_index] > 0):
            elements_index[page_index] -= 1
        elif (action in Core.user.movement_keys['down']) and (elements_index[page_index] < len(current_page)-1):
            elements_index[page_index] += 1
        elif action in current_page:
            if Core.indexes and Core.indexes[-1] == []:
                Core.indexes[-1] = elements_index
            return action
        else:
            information(text = 'Invalid answer.')

def ask(text: str) -> bool:
    """
        Asks a close-ended question and returns the answer.

        Parameters:
            text (str): The text that will be shown.

        Returns:
            The answer of the question, which is either positive or negative.
    """
    while True:
        answer: str = interface(text = text, elements = [Core.user.positive, Core.user.negative])
        if answer == Core.user.positive:
            return True
        if answer == Core.user.negative:
            return False
        information(text = f'You must provide an answer. \"{Core.user.abort}\" is not an option.')

def menu(dictionary: dict[str, Union[str, dict[str, Any], Any]]) -> None:
    """
        For applications, this makes the link between nested dictionaries, specific types of values and function calls.

        Parameters:
            dictionary (dict): A dictionary of valid elements that vary.

        Returns:
            Nothing.
    """
    while True:
        if '.condition' in dictionary.keys() and callable(dictionary['.condition']):
            condition: Any = dictionary['.condition']()
            if isinstance(condition, Modifiable):
                condition = condition.value()
            if not condition:
                information(text = 'You can not continue.' if '.checkfail' not in dictionary.keys() else str(dictionary['.checkfail']))
                break
        menu_text: str = ''
        if '.description' in dictionary.keys() and isinstance(dictionary['.description'], str):
            menu_text = str(dictionary['.description'])
        elements: list[str] = []
        for element in dictionary:
            if element[0] != '.':
                if element not in elements:
                    elements.append(element)
        selected_value: str = interface(text = menu_text, elements = elements)
        if selected_value == Core.user.abort:
            break
        selected_action: Any = dictionary[selected_value]
        with indexation(choice = selected_value):
            if isinstance(selected_action, dict):
                nested_action: dict[str, Any] = selected_action
                if '.name' in nested_action.keys():
                    Core.choices[-1] = str(nested_action['.name']()) if callable(nested_action['.name']) else nested_action['.name']
                menu(dictionary = nested_action)
            elif isinstance(selected_action, str):
                information(text = selected_action)
            elif callable(selected_action):
                result: Any = selected_action()
                if isinstance(result, Modifiable):
                    result.modify()
            else:
                information(text = 'Unrecognised action.')

def quantify(text: str, minimum: Union[int, float], category: type, maximum: Union[int, float]) -> Union[int, float, str]:
    """
        A function specialised in asking for a number, verifying the number, and returning it.

        Parameters:
            text (str): The text that will be shown.
            minimum (int or float): The minimum of the returned value.
            category (type): Decides whether the returned value is an integer or a real number.
            maximum (int or float): The maximum of the returned value.

        Returns:
            Either the Abort value, or a valid number.
    """
    while True:
        number: str = write(text = text)
        if number == Core.user.abort:
            return Core.user.abort
        if number and ((category == int and '.' not in number) or (len(number.split('.')) == 2 and category == float)):
            if all(digit in DIGITS for digit in (number.removeprefix('-') if number[0] == '-' else number).replace('.', '')):
                if minimum <= category(number) <= maximum:
                    return category(number)
                information(text = 'Number out of range.')
            else:
                information(text = 'Invalid number.')
        else:
            information(text = 'Invalid answer.')

def password(username: str) -> bool:
    """
        Verifies the password of the user if the password is not empty.

        Parameters:
            username (str): The username of the user to check.

        Returns:
            A boolean.
    """
    if username not in Core.users:
        return False
    if Core.users[username].is_password(entered_password = ''):
        return True
    tries: int = 0
    while True:
        answer: str = write(text = f'Enter the password of {username} for security, or \"{Core.user.abort}\" to abort.')
        if answer == Core.user.abort:
            return False
        if Core.users[username].is_password(entered_password = answer):
            return True
        if answer:
            information(text = 'The password is incorrect.')
            if Core.users[username].password_reminder:
                information(text = f'The password of the account is {Core.users[username].get_password()} to remind you.')
            tries += 1
            if tries >= 4:
                seconds: int = tries*5
                while seconds > 0:
                    show(text = f'You have incorrectly entered the password multiple times. You have been blocked for {seconds} seconds.')
                    seconds -= 1
                    sleep(1)
                    while kbhit():
                        getwch()

if __name__ == '__main__':
    modules['main'] = modules[__name__]
    while True:
        while True:
            write(text = f'Enter to turn on {Unique.device_name}.')
            time: str = datetime.now().strftime('%A %d %B %Y' + (', %H:%M:%S' if Unique.lock_screen_time else ''))
            string: str = f'{time}\nEnter anything to continue, or \"{Core.user.abort}\"'
            if Core.keyboard_control:
                user_input: str = ''
                time_left: float = Unique.lock_screen_timeout
                time_to_add: float = 0.0
                while time_left > 0.0:
                    show(text = f'{string}, or wait {time_left:.2f} seconds to turn off {Unique.device_name}.\n>>> {user_input}')
                    if kbhit():
                        character: str = getwch()
                        time_left += time_to_add
                        time_to_add -= time_to_add
                        if character == '\r':
                            break
                        if character == '\b':
                            user_input = user_input[0:-1]
                        elif character in CHARACTERS:
                            user_input += character
                        else:
                            information(text = 'Invalid character.')
                    time_left -= 0.01
                    time_to_add += 0.01
                    sleep(0.01)
            else:
                user_input: str = write(text =  f'{string} to turn off {Unique.device_name}.')
            if user_input not in (Core.user.abort, ''):
                break
        user_text: str = 'Enter the user you want to log in, or \"Create account\" to create an account, or '
        while True:
            current_user: str = write(text = f'{user_text}\"{Core.user.abort}\" to turn off {Unique.device_name}.')
            if current_user == Core.user.abort:
                break
            if current_user in Core.users and password(username = current_user):
                Core.user = Core.users[Core.users[current_user].username]
                if Core.user.new:
                    information(text = f'Welcome to SuperOSh, {Core.user.username}!')
                    information(text = 'Let us get you started quickly. Answer to a few questions first before accessing SuperOSh.')
                    for keybind in Core.user.movement_keys:
                        while True:
                            mark: str = write(text = f'Which key should be assigned to the action \"{keybind}\"?')
                            if len(mark) != 1 or any(any(key == mark for key in keys) for keys in Core.user.movement_keys.values()):
                                information(text = 'The key should only be a single letter')
                            else:
                                Core.user.movement_keys[keybind] = [mark.lower(), mark.upper()]
                                break
                    Core.user.new = False
                    information(text = 'In interfaces menus, you can press the corresponding key to do the corresponding action.')
                    for action_name, key in Core.user.movement_keys.items():
                        information(text = f'Enter \"{key[0]}\" or \"{key[1]}\" to do {action_name}.')
                    information(text = 'Thank you for choosing SuperOSh!')
                for file in Path(__file__).parent.glob('*_application.py'):
                    spec: Any = util.spec_from_file_location(file.stem, file)
                    if spec is None:
                        continue
                    module: Any = util.module_from_spec(spec)
                    loader: Any = spec.loader
                    if loader is None:
                        continue
                    loader.exec_module(module)
                    if not hasattr(module, 'application'):
                        continue
                    application_module: Any = module.application
                    if not isinstance(application_module, dict):
                        continue
                    if not all(branch in application_module for branch in ['name', 'description', 'version', 'visual', 'developer', 'main']):
                        continue
                    if not isinstance(application_module['name'], str):
                        continue
                    if not all(isinstance(application_module[element], str) for element in ['description', 'visual', 'developer']):
                        continue
                    if 'age' in application_module:
                        if not isinstance(application_module['age'], int):
                            continue
                    else:
                        application_module['age'] = 0
                    if not isinstance(application_module['version'], dict):
                        continue
                    if not all(element in application_module['version'] for element in ['major', 'minor', 'patch']):
                        continue
                    if not all(isinstance(application_module['version'][element], int) for element in ['major', 'minor', 'patch']):
                        continue
                    if not isinstance(application_module['main'], dict):
                        continue
                    if application_module['name'] in Core.applications:
                        continue
                    for user in Core.users.values():
                        user.home_screen_order.append(application_module['name'])
                        if 'initialisation' in application_module and isinstance(application_module['initialisation'], dict):
                            user.applications[application_module['name']] = deepcopy(application_module['initialisation'])
                        if hasattr(module, 'on_load'):
                            module.on_load()
                    Core.applications[application_module['name']] = application_module
                current_order: list[Union[str, dict[str, Union[list[str], str]]]] = list(Core.user.home_screen_order)
                folder_stack: list[tuple[str, list[Union[str, dict[str, Union[list[str], str]]]]]] = []
                title: str = f'Hello, {Core.user.username}!'
                temporary_index: list[int] = []
                while True:
                    choices: list[str] = []
                    applications: dict[str, str] = {}
                    folders: dict[str, dict[str, Union[list[str], str]]] = {}
                    for item in current_order:
                        if isinstance(item, dict):
                            folder_name: Any = item.get('name')
                            if isinstance(folder_name, str):
                                folders[folder_name] = item
                                choices.append(folder_name)
                        else:
                            visual: str = Core.applications[item]['visual']
                            applications[visual + ' ' * len(visual) + item] = item
                            choices.append(visual + ' ' * len(visual) + item)
                    Core.indexes = [[0]*(((len(choices)-1)//8)+1)] if not temporary_index else [temporary_index]
                    application_choice: str = interface(text = title, elements = choices)
                    temporary_index = Core.indexes[-1]
                    Core.indexes = []
                    if application_choice == Core.user.abort:
                        if not folder_stack:
                            break
                        title, current_order = folder_stack.pop()
                    elif application_choice in applications:
                        if Core.applications[applications[application_choice]]['age'] > Core.user.age:
                            information(text = 'You do not have the required age to use this application.')
                            continue
                        with indexation(choice = application_choice):
                            menu(dictionary = Core.applications[applications[application_choice]]['main'])
                    elif application_choice in folders:
                        folder = folders[application_choice]
                        folder_applications: Any = folder.get('applications', [])
                        if isinstance(folder_applications, list):
                            folder_stack.append((title, current_order))
                            current_order = folder_applications
                            title = application_choice
                    else:
                        information(text = 'The application was not found.')
                if Core.user.role == 'Guest':
                    del Core.users[Core.user.username]
                    for account in Core.users.values():
                        if account.role == 'Administrator':
                            Core.user = account
                            break
            elif current_user == 'Create account':
                while True:
                    new_username: str = write(text = f'What will be the username? Enter \"{Core.user.abort}\" to cancel.')
                    if new_username == Core.user.abort:
                        break
                    if new_username in Core.users:
                        information(text = 'This username is already taken.')
                    elif new_username != '':
                        account_role: str = write(text = 'What role do you want to have?\nAdministrator\nUser\nGuest')
                        if account_role == 'Administrator' and any('Administrator' == user.role for user in Core.users.values()):
                            information(text = 'Administrator account already exists')
                        elif account_role in ['User', 'Administrator', 'Guest']:
                            if account_role == 'Guest':
                                information(text = 'The account will be deleted on log out.')
                            new_password: str = write(text = 'What should be password of the account?')
                            if new_password != '' and write(text = 'Enter again your password for security.') == new_password:
                                new_user: User = User(username = new_username, user_password = new_password, user_role = account_role)
                                for the_application_name, application in Core.applications.items():
                                    new_user.home_screen_order.append(the_application_name)
                                    new_user.applications[the_application_name] = deepcopy(application.get('initialisation'))
                                Core.users[new_username] = new_user
                                break
                        else:
                            information(text = 'Invalid role.')
            else:
                information(text = 'Account does not exist.')
