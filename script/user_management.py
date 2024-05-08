from rich.console import Console
from rich import print
from display import Display
import maskpass
import utils
import json
from leaderboard import Leaderboard


class UserManager:
    def __init__(self, storage_file='users.json'):
        self.storage_file = storage_file
        self.users = utils.load_data(self.storage_file)
        self.console = Console()
        self.leaderboard_file = 'leaderboard.json'
        self.leaderboard = utils.load_data(self.leaderboard_file)
        # from GameSystem
        self.logged_in_user = None
        self.display = Display()
        self.leaderboard_manager = Leaderboard()

    def create_user(self, username, password, email):
        if username in self.users:
            print("[deep_pink2](⋟﹏⋞)Oops, username already taken.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        else:
            self.users[username] = {'password': password, 'email': email, 'characters': []}
            utils.save_data(self.users, self.storage_file)
            print(f"[dark_slate_gray2]{username} created successfully.[/]")
            print()
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return "User created successfully."

    def save_users(self):
        utils.save_data(self.users, self.storage_file)

    def reload_data(self):
        self.users = utils.load_data(self.storage_file)

    def verify_user(self, username, password):
        self.reload_data()
        if username not in self.users:
            return False
        return self.users[username]['password'] == password

    def reset_password(self):
        while True:
            username = input("\033[93mEnter your username: \033[0m")
            if username.lower() == 'back' or username.lower() == 'b':
                return
            if username not in self.users:
                print("[deep_pink2](⋟﹏⋞)Oops, user does not exist.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                self.display.clear_last_two_lines(3)
                continue
            break
        while True:
            email = input("\033[93mEnter your email address for password reset:  \033[0m")
            if email.lower() == 'back' or email.lower() == 'b':
                return
            if self.users[username]['email'] != email:
                print("[deep_pink2](⋟﹏⋞)Oops, incorrect email.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                self.display.clear_last_two_lines(3)
                continue
            break
        new_password = maskpass.askpass(prompt="\033[93mEnter your new password: \033[0m", mask="*")
        self.users[username]['password'] = new_password
        utils.save_data(self.users, self.storage_file)
        print("[dark_slate_gray2]Password reset successfully.[/]")
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def username_verify(self, username):
        if username in self.users:
            print("[deep_pink2](⋟﹏⋞)Oops, username already taken.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            self.display.clear_last_two_lines(3)
            return username in self.users
        else:
            pass

    def login(self, username, password):
        if self.verify_user(username, password):
            self.logged_in_user = username
            return "Logged in successfully."
        else:
            print("[deep_pink2](＞﹏＜)Oops, incorrect username or password.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

    def delete_account(self, username):
        if username not in self.users:
            print("[deep_pink2](⋟﹏⋞)Oops, user does not exist.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return
        # Deleting the user account
        del self.users[username]
        print(f"[dark_slate_gray2]{username} has been deleted successfully.[/]")
        self.leaderboard_manager.delete_leaderboard(username)
        self.save_users()
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def delete_character(self, username):
        self.reload_data()
        user_data = self.users.get(username, None)
        if user_data is None:
            print("[deep_pink2](＞﹏＜)Oops, user not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        if not user_data['characters']:
            print("[deep_pink2](＞﹏＜)Oops, no characters available for this user.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return

        self.display.clear_screen()
        self.display.draw()
        print("[light_steel_blue]Select a character to delete:[/]")
        for i, character in enumerate(user_data['characters'], start=1):
            print(f"{i}, {character['name']}")
        self.display.draw()
        print("[orchid1 italic bold]💡Hints:[/]")
        print("- Type a number to select a character to delete")
        print("- Type '(B)ack' to go back to main menu")
        self.display.draw()

        choice = input("# ")
        if choice.lower() == 'back' or choice.lower() == 'b':
            return 'back'
        elif choice.isdigit():
            choice = int(choice)
            assert 1 <= choice <= len(user_data['characters'])
            self.display.clear_screen()
            self.display.draw()
            print("[orchid1 italic bold]💡Hints:[/]")
            print("- Type 'Y' or 'y' to delete the character")
            print("- Type 'N' or 'n' to go back")
            self.display.draw()
            print(f"[deep_pink2]{character['name']} will be deleted. Are you sure you want to continue?[/] ('Y/N')")
            answer = self.display.colored_input("[gold1]Your answer:[/] ", ).lower()
            if answer == 'y':
                character_name = user_data['characters'][choice - 1]['name']
                del user_data['characters'][choice - 1]
                self.leaderboard = utils.load_data(self.leaderboard_file)
                self.leaderboard = [entry for entry in self.leaderboard
                                    if not (
                                entry.get("Player") == username and entry.get("Character name") == character_name)]
                utils.save_data(self.leaderboard, self.leaderboard_file)
                # Saving the updated user data
                self.save_users()
                print("[dark_slate_gray2]Character deleted successfully.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            else:
                return

        else:
            print("[deep_pink2](＞﹏＜)Oops, invalid selection.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

    def get_bonus(self, username, character_name):
        try:
            with open('leaderboard.json', 'r') as file:
                users_data = json.load(file)
        except IOError:
            print("Error: File not found or inaccessible.")
            return None

        for entry in users_data:
            if entry.get("Player") == username and entry.get("Character name") == character_name:
                return entry.get('score')

        return None

    def reset_bonus(self, username, character_name):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)

            if username in users_data and "characters" in users_data[username]:
                for character in users_data[username]["characters"]:
                    if character["name"] == character_name:
                        character["bonus"] = 0

            with open('users.json', 'w') as file:
                json.dump(users_data, file, indent=4)

        except IOError:
            print("Error: File not found or inaccessible.")

class SaveLoad:
    def __init__(self):
        self.user_manager = UserManager()
        self.display = Display()

    def save_game(self, username, name, current_room, inventory, confidence, rooms):
        # Checking if the user exists
        with open('users.json', 'r') as json_file:
            user_data = json.load(json_file)
        if username not in user_data:
            print("[deep_pink2](＞﹏＜)Oops, user not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return

        character = user_data[username]['characters']

        # Checking for 'game_state' and 'characters' keys in user_data
        if 'characters' in user_data[username]:
            # looping through the characters of the user
            for char in user_data[username]['characters']:
                if char['name'] == name:
                    character = char
                    break
        else:
            print(f"No characters found for {username}")
            input("Press enter to continue")
            user_data[username]['characters'] = []

        if character is None:
            print(f"[deep_pink2](＞﹏＜)Oops, character {name} not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return
        # Replacing old game state with the new game state
        new_game_state = {
            'current_room': current_room,
            'inventory': inventory,
            'confidence': confidence,
            'rooms': rooms,
        }

        character['game_state'] = [new_game_state]

        try:
            with open('users.json', 'w') as file:
                json.dump(user_data, file, indent=4)
        except IOError:
            print("[deep_pink2](＞﹏＜)Oops, file not found or inaccessible.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

    def load_game(self, username):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except IOError:
            print("[deep_pink2](＞﹏＜)Oops, file not found or inaccessible.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return None

        user_data = users_data.get(username, {})
        if 'characters' in user_data and user_data['characters']:
            self.display.clear_screen()
            self.display.draw()
            print("[light_steel_blue]Select a character to play:[/]")
            for i, character in enumerate(user_data['characters'], start=1):
                print(f"{i}, {character['name']}")
            self.display.draw()
            print("[orchid1 italic bold]💡Hints:[/]")
            print("- Type a number to select a character to play")
            print("- Type 'back' or 'b' to go back to main menu")
            self.display.draw()
        else:
            print("[deep_pink2](＞﹏＜)Oops, no characters available for this user.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return None

        choice = input("# ")
        try:
            if choice.lower() == 'back' or choice.lower() == 'b':
                return 'back'
            elif choice.isdigit():
                choice = int(choice)
                character = user_data['characters'][choice - 1]
            else:
                print("[deep_pink2](＞﹏＜)Oops, please enter [/]'back' [deep_pink2]or a valid number.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                return None

            if 'game_state' in character and character['game_state']:
                game_state = character['game_state'][-1]
                current_room = game_state.get('current_room', "Maple Sanctuary")
                inventory = game_state.get('inventory', [])
                rooms = game_state.get('rooms', {})
                confidence = game_state.get('confidence', 100)
                return character, current_room, inventory, rooms, confidence
            else:
                print(f"[deep_pink2]No saved game state for character {character['name']}.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                return None
        # Handling index out of range error
        except IndexError:
            print("[deep_pink2](＞﹏＜)Oops, character index out of range, please try again.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
