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
        self.password: str = password
        self.role: str = role
        self.user_experience: User.UserExperience = self.UserExperience()

    class UserExperience:
        """
            Store the User Experience data of the account.
        """
        def __init__(self) -> None:
            """
                Initialises User Experience account data.

                Parameters:
                    Nothing.

                Returns:
                    Nothing.
            """
            self.positive: str = 'Yes'
            self.negative: str = 'No'
            self.next_page: str = 'Next page'
            self.previous_page: str = 'Previous page'
            self.abort: str = 'Abort'

class Core:
    """
        Stores boring, but important variables.
    """
    keyboard_control: bool = False
    users: dict[str, User] = {
        'AlfredTheAdmin': User(
            username = 'AlfredTheAdmin',
            password = 'WhyAreYouTryingToLogInMyAccount',
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
    movement_keys: dict[str, list[str]] = {
        'up': ['z', 'Z'],
        'down': ['s', 'S'],
        'right': ['d', 'D'],
        'left': ['q', 'Q']
    }

class Characters:
    """
        Stores main characters, such as letters, digits and some special characters.
    """
    digits: list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    lowercase_letters: list[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    uppercase_letters: list[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    special_characters: list[str] = [' ', '!', '\"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    characters: list[str] = [*lowercase_letters, *uppercase_letters, *special_characters, *digits]

try:
    from msvcrt import kbhit, getwch
    Core.keyboard_control = True
except ModuleNotFoundError:
    def kbhit() -> bool:
        return False
    def getwch() -> str:
        return '\r'

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
    while True:
        show(text = text)
        answer: str = input('>>> ')
        if all(element in Characters.characters for element in answer):
            return answer
        else:
            show(text = 'Input includes unrecognised character. Enter to rewrite.')
            input('>>> ')

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
            show(text = f'{text}\n{'\n'.join(f'{digit}. {element}' for digit, element in enumerate(current_page))}')
            action: str = getwch()
        else:
            action: str = write(text = f'{text}\n{'\n'.join(f'{digit}. {element}' for digit, element in enumerate(current_page))}')
        current_page[element_index] = current_page[element_index][0:-4]
        if action in [*Characters.digits] + (['\r', '\b'] if Core.keyboard_control else ['']):
            choice: int = element_index if action == ('\r' if Core.keyboard_control else '') else int(action) if action in Characters.digits else 0
            if choice == 0:
                action = Core.user.user_experience.abort if page_index == 0 else Core.user.user_experience.previous_page
            elif 1 <= choice <= 8 and choice <= len(current_page) - 1:
                return current_page[choice]
            elif choice == 9:
                action = Core.user.user_experience.next_page
        if (action in Unique.movement_keys['right'] or action == Core.user.user_experience.next_page) and page_index < len(pages)-1:
            element_index = 0
            page_index += 1
        elif (action in Unique.movement_keys['left'] or action == Core.user.user_experience.previous_page) and page_index > 0:
            element_index = 0
            page_index -= 1
        elif (action in Unique.movement_keys['up']) and (element_index > 0):
            element_index -= 1
        elif (action in Unique.movement_keys['down']) and (element_index < len(current_page)-1):
            element_index += 1
        elif action in current_page:
            return action
        else:
            information(text = 'Invalid answer!')

def ask(text: str):
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
        elif answer == Core.user.user_experience.negative:
            return False
        else:
            information(text = f'You must provide an answer. {Core.user.user_experience.abort} is not a choice.')

def verify_password(username: str) -> bool:
    if username not in Core.users:
        return False
    return True

if __name__ == '__main__':
    """
        Encapsulates the main OS. It is not a function to prevent application files to call OS.
    """
    from datetime import datetime
    from time import sleep
    while True:
        write(text = f'Enter to turn on {Unique.device_name}.')
        if Core.keyboard_control:
            time_left: float = Unique.lock_screen_timeout
            user_input: str = ''
            while time_left > 0.0:
                show(text = f'{datetime.now().strftime('%A %d %B %Y' + (', %H:%M:%S' if Unique.lock_screen_time == True else ''))}\nEnter \"{Core.user.user_experience.abort}\" or wait {time_left:.2f} seconds to turn off {Unique.device_name}, or anything else to continue.\n>>> {user_input}')
                if kbhit():
                    character: str = getwch()
                    time_left = Unique.lock_screen_timeout
                    if character == '\r':
                        break
                    elif character == '\b':
                        user_input = user_input[0:-1]
                    elif character in Characters.characters:
                        user_input += character
                    else:
                        information(text = 'Invalid character!')
                time_left -= 0.01
                sleep(0.01)
        else:
            user_input: str = write(text = f'{datetime.now().strftime('%A %d %B %Y' + (', %H:%M:%S' if Unique.lock_screen_time == True else ''))}\nEnter \"{Core.user.user_experience.abort}\" to turn off {Unique.device_name}, or anything else to continue.')
        if (user_input != Core.user.user_experience.abort) and (user_input != ''):
            while True:
                current_user: str = write(text = f'Enter the Core.user you want to log in, or \"Create account\" to create an account, or \"{Core.user.user_experience.abort}\" to turn off {Unique.device_name}.')
                if current_user in Core.users.keys():
                    verify_password(username = current_user)
                    # TBA
                    interface(text = 'Do you prefer this or that?', elements = ['This', 'That', 'No, this', 'That!!', 'vro', 'What?', 'Are u serious', '(slowed x reverb)', 'choice1', 'choice2', 'SuperTankh'])
                elif current_user == Core.user.user_experience.abort:
                    break
                elif current_user == 'Create account':
                    new_username: str = write(text = 'What should be the username of your new account?')
                    if new_username in Core.users.keys():
                        information(text = 'This username is already taken.')
                    else:
                        account_role: str = interface(text = 'What type of account do you want to make?', elements = ['Administrator', 'User', 'Guest'])
                        if account_role == 'Administrator' and all('Administrator' == Core.users[current_user].role for current_user in Core.users):
                            information(text = f'Administrator account already exists')
                        elif account_role in ['User', 'Guest']:
                            if account_role == 'Guest':
                                information(text = 'The account will be deleted on log out.')
                            while True:
                                new_password: str = write(text = 'What should be password of the account?')
                                if new_password != '' and write(text = 'Enter again your password for security.') == new_password:
                                    Core.users[new_username] = User(username = new_username, password = new_password, role = account_role)
                                    break
                else:
                    information(text = 'Account does not exist.')