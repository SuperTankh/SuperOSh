"""
    This file englobes all the classes, variables, and functions of the OS.
"""
from datetime import datetime
from time import sleep

class User:
    """
        Stores the data of a user account.
    """
    def __init__(self, username: str, password: str, role: str) -> None:
        """
            Initialises account data.

            Parameters:
                username (str): the username of the account.
                password (str): the password of the account.
                role (str): the permissions role of the account.

            Returns:
                Nothing.
        """
        self.username: str = username
        self.__password: str = password
        self.role: str = role
        self.__new: bool = True
        self.user_experience: User.UserExperience = self.UserExperience()
        self.settings: User.Settings = self.Settings()

    class UserExperience:
        """
            Stores the User Experience data of the account.
        """
        def __init__(self) -> None:
            """
                Initialises User Experience account data.

                Parameters:
                    self (User.UserExperience()): the user experience data.

                Returns:
                    Nothing.
            """
            self.positive: str = 'Yes'
            self.negative: str = 'No'
            self.next_page: str = 'Next page'
            self.previous_page: str = 'Previous page'
            self.abort: str = 'Abort'

    class Settings:
        """
            Stores the Settings data of the account.
        """
        def __init__(self) -> None:
            """
                Initialises Settings account data.

                Parameters:
                    self (User.Settings()): the user account data.

                Returns:
                    Nothing.
            """
            self.password_reminder = True
            self.movement_keys: dict[str, list[str]] = {
                'up': [],
                'down': [],
                'right': [],
                'left': []
            }

    def is_password(self, entered_password: str) -> bool:
        """
            Verifies if the entered password is the same as the user password.

            Parameters:
                self (User): the user account data.
                entered_password (str): the entered password to verify.

            Returns:
                A boolean depending on the parameter.
        """
        return entered_password == self.__password

    def get_password(self) -> str:
        """
            Get the account password only if the current user is the user or an Administrator, and if the user enabled password_reminder.

            Parameters:
                self (User): the user account data.

            Returns:
                The password of the current user.
        """
        return self.__password if (Core.user.role == 'Administrator' or Core.user == self) and self.settings.password_reminder else ''

    def get_new(self) -> bool:
        """
            Sends the state of the account, if the account is \"new\" or not.

            Parameters:
                self (User): the user account data.

            Returns:
                The state of the account.
        """
        return self.__new

    def set_new(self) -> None:
        """
            To prevent malicious applications to change self.__new, only change it once.

            Parameters:
                self (User): the user account data.

            Returns:
                Nothing.
        """
        if self.__new:
            self.__new = False

class Core:
    """
        Stores boring, but important variables.
    """
    keyboard_control: bool = False
    users: dict[str, User] = {
        'AlfredTheAdmin': User(
            username = 'AlfredTheAdmin',
            password = 'WhyAreYouTryingToLogInMyAccount?',
            role = 'Administrator'
        )
    }
    user: User = users['AlfredTheAdmin']

class Unique:
    """
        Stores variables that can only be changed in an Administrator account.
    """
    device_name: str = 'SuperDeviceh'
    lock_screen_timeout: float = 4.0
    lock_screen_time: bool = True

class Characters:
    """
        Stores main characters, such as letters, digits and some special characters.
    """
    digits: list[str] = list('0123456789')
    lowercase_letters: list[str] = list('abcdefghijklmnopqrstuvwxyz')
    uppercase_letters: list[str] = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    special_characters: list[str] = list(' !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
    characters: list[str] = [
        *lowercase_letters,
        *uppercase_letters,
        *special_characters,
        *digits
    ]

try:
    from msvcrt import kbhit, getwch
except ModuleNotFoundError:
    def kbhit() -> bool:
        """
            Is the puppet replacement for kbhit(). Does nothing interesting.

            Parameters:
                Nothing.

            Returns:
                A boolean: False.
        """
        return False
    def getwch() -> str:
        """
            Is the puppet replacement for getwch(). Does nothing interesting.

            Parameters:
                Nothing.

            Returns:
                A string: the Enter character.
        """
        return '\r'

def enumeration(elements: list[str]) -> str:
    """
        Transforms a plain list into an enumeration of this list.

        Parameters:
            elements (list[str]): the list of elements.

        Returns:
            A string of the enumeration of the list.
    """
    return '\n'.join(f'{digit}. {element}' for digit, element in enumerate[str](elements))

def show(text: str) -> None:
    """
        Clears the terminal and shows a text, replaces print().

        Parameters:
            text (str): the text that will be printed in the terminal

        Returns:
            Nothing.
    """
    print(f'\033c{text}')

def write(text: str) -> str:
    """
        Shows a text and awaits an input that only has allowed characters and returns it, replaces input().

        Parameters:
            text (str): the text that will be shown.

        Returns:
            The string input that only includes allowed characters.
    """
    error: str = ''
    while True:
        show(text = f'{error}{text}')
        answer: str = input('>>> ')
        if all(element in Characters.characters for element in answer):
            return answer
        error = 'Input includes unrecognised character.\n'

def information(text: str) -> None:
    """
        Shows a text and awaits any input to continue.

        Parameters:
            text (str): the text that will be shown.

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
            text (str): the text that will be shown.
            elements (list[str]): all possible choices in a raw list.

        Returns:
            The chosen string element in the list, abort is part of the list and can also be returned.
    """
    pages: list[list[str]] = []
    page_index: int = 0
    element_index: int = 0
    elements.insert(0, Core.user.user_experience.abort)
    while len(elements) > 0:
        pages.append([*elements[0:9]])
        del elements[0:9]
        if len(elements) > 0:
            pages[-1].append(Core.user.user_experience.next_page)
            elements.insert(0, Core.user.user_experience.previous_page)
    del elements
    while True:
        current_page: list[str] = pages[page_index]
        current_page[element_index] += ' <--'
        if Core.keyboard_control:
            show(text = f'{text}\n{enumeration(elements = current_page)}')
            action: str = getwch()
        else:
            action: str = write(text = f'{text}\n{enumeration(elements = current_page)}')
        current_page[element_index] = current_page[element_index][0:-4]
        if action in [*Characters.digits] + (['\r', '\b'] if Core.keyboard_control else ['']):
            choice: int = int(action) if action in Characters.digits else 0 if action == '\b' else element_index
            action = Core.user.user_experience.next_page if choice == 9 else (Core.user.user_experience.abort if page_index == 0 else Core.user.user_experience.previous_page) if choice == 0 else current_page[choice] if 1 <= choice <= 8 and choice <= len(current_page) - 1 else ''
        if (action in Core.user.settings.movement_keys['right'] or action == Core.user.user_experience.next_page) and page_index < len(pages)-1:
            element_index = 0
            page_index += 1
        elif (action in Core.user.settings.movement_keys['left'] or action == Core.user.user_experience.previous_page) and page_index > 0:
            element_index = 0
            page_index -= 1
        elif (action in Core.user.settings.movement_keys['up']) and (element_index > 0):
            element_index -= 1
        elif (action in Core.user.settings.movement_keys['down']) and (element_index < len(current_page)-1):
            element_index += 1
        elif action in current_page:
            return action
        else:
            information(text = 'Invalid answer!')

def ask(text: str) -> bool:
    """
        Asks a close-ended question and returns the answer.

        Parameters:
            text (str): the text that will be shown.

        Returns:
            The answer of the question, which is either positive or negative.
    """
    while True:
        answer: str = interface(text = text, elements = [Core.user.user_experience.positive,Core.user.user_experience.negative])
        if answer == Core.user.user_experience.positive:
            return True
        if answer == Core.user.user_experience.negative:
            return False
        information(text = f'You must provide an answer. \"{Core.user.user_experience.abort}\" is not a choice.')

def verify_password(username: str) -> bool:
    """
        Verifies the password of the user.

        Parameters:
            username (str): the username of the user to check.

        Returns:
            A boolean depending on whether the user password was entered, skipped, or aborted.
    """
    if username not in Core.users:
        return False
    if Core.users[username].is_password(entered_password = ''):
        return True
    tries: int = 0
    while True:
        answer: str = write(text = f'Enter the password of {username} for security, or \"{Core.user.user_experience.abort}\" to abort.')
        if answer == Core.user.user_experience.abort:
            return False
        if Core.users[username].is_password(entered_password = answer):
            return True
        information(text = 'The password is incorrect.')
        if Core.users[username].settings.password_reminder:
            information(text = f'The password of the account is {Core.users[username].get_password()} to remind you.')
        tries += 1
        if tries >= 4:
            seconds: int = tries*5
            while seconds > 0:
                show(text = f'You have incorrectly entered the password. You have been blocked for {seconds} seconds.')
                seconds -= 1
                sleep(1)
                while kbhit():
                    getwch()

def create_account() -> str:
    """
        Creates a user account.

        Parameters:
            Nothing.

        Returns:
            The username of the new account, or an empty string.
    """
    while True:
        new_username: str = write(text = f'What will be the username of the account? Enter \"{Core.user.user_experience.abort}\" to cancel.')
        if new_username == Core.user.user_experience.abort:
            return ''
        if new_username in Core.users:
            information(text = 'This username is already taken.')
        else:
            account_role: str = interface(text = 'What role do you want to have?', elements = ['Administrator', 'User', 'Guest'])
            if account_role == 'Administrator' and any('Administrator' == user.role for user in Core.users.values()):
                information(text = 'Administrator account already exists')
            elif account_role in ['User', 'Guest']:
                if account_role == 'Guest':
                    information(text = 'The account will be deleted on log out.')
                while True:
                    new_password: str = write(text = 'What should be password of the account?')
                    if new_password != '' and write(text = 'Enter again your password for security.') == new_password:
                        Core.users[new_username] = User(username = new_username, password = new_password, role = account_role)
                        return new_username

def lock_screen() -> None:
    """
        Contains the lock screen of the OS.

        Parameters:
            Nothing.

        Returns:
            Nothing.
    """
    while True:
        write(text = f'Enter to turn on {Unique.device_name}.')
        time: str = datetime.now().strftime('%A %d %B %Y' + (', %H:%M:%S' if Unique.lock_screen_time else ''))
        if Core.keyboard_control:
            user_input: str = ''
            time_left: float = Unique.lock_screen_timeout
            time_to_add: float = 0.0
            while time_left > 0.0:
                show(text = f'{time}\nEnter \"{Core.user.user_experience.abort}\" or wait {time_left:.2f} seconds to turn off {Unique.device_name}, or anything else to continue.\n>>> {user_input}')
                if kbhit():
                    character: str = getwch()
                    time_left += time_to_add
                    time_to_add -= time_to_add
                    if character == '\r':
                        break
                    if character == '\b':
                        user_input = user_input[0:-1]
                    elif character in Characters.characters:
                        user_input += character
                    else:
                        information(text = 'Invalid character!')
                time_left -= 0.01
                time_to_add += 0.01
                sleep(0.01)
        else:
            user_input: str = write(text = f'{time}\nEnter \"{Core.user.user_experience.abort}\" to turn off {Unique.device_name}, or anything else to continue.')
        if user_input not in (Core.user.user_experience.abort, ''):
            break

if __name__ == '__main__':
    while True:
        lock_screen()
        while True:
            current_user: str = write(text = f'Enter the user you want to log in, or \"Create account\" to create an account, or \"{Core.user.user_experience.abort}\" to turn off {Unique.device_name}.')
            if current_user == Core.user.user_experience.abort:
                break
            if current_user in Core.users and verify_password(username = current_user):
                Core.user = Core.users[Core.user.username]
                if Core.user.get_new():
                    information(text = f'Welcome to SuperOSh, {Core.user.username}!')
                    information(text = 'Let us get you started quickly. Answer to a few questions first before accessing SuperOSh.')
                    for keybind in Core.user.settings.movement_keys:
                        while True:
                            new_key: str = write(text = f'Which key should be assigned to the action \"{keybind}\"?')
                            if len(new_key) != 1 or new_key not in [*Characters.lowercase_letters, *Characters.uppercase_letters]:
                                information(text = 'The key should only be a single letter')
                            else:
                                Core.user.settings.movement_keys[keybind] = [new_key.lower(), new_key.upper()]
                                break
                    Core.user.set_new()
                interface(text = 'Do you prefer this or that?', elements = ['This', 'That', 'No, this', 'That!!', 'vro', 'What?', 'Are u serious', '(slowed x reverb)', 'choice1', 'choice2', 'Super'])
                # placeholder
            elif current_user == 'Create account':
                create_account()
            else:
                information(text = 'Account does not exist.')
