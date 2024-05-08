
from map import Map, paths, rooms
from monster import monsters
from user_management import UserManager
from user_management import SaveLoad
from rich import print
from rich.console import Console
import time
from colorama import Fore
import sys
import maskpass
import json
from display import Display
from character import Character
from leaderboard import Leaderboard


class GamePlay:
    def __init__(self):
        self.run = True
        self.menu1 = True
        self.menu2 = False
        self.play = False
        self.rules = False
        self.map = Map(3, 6, 0, 1, paths)
        self.current_room = "Maple Sanctuary"
        self.inventory = []
        self.confidence = 100
        self.bonus = 0
        self.username = ""
        self.character_name = ""
        self.room_info = rooms.get(self.current_room, {})
        self.message = ""
        self.rooms = rooms
        self.quit_game = False
        self.user_manager = UserManager()
        self.console = Console()
        self.save_load = SaveLoad()
        self.instruction = f"Welcome to the wood[green]{self.character_name}[/]!\n" \
                           f"Our wood is under attack by monsters\n" \
                           f"Each [salmon1]monster[/] can be defeated by [pink3]specific item(s)[/]\n" \
                           f"Please find those items and [red]defeat all monsters[/] to bring peace back to the wood...\n"\
                           f"If you don't have the [pink3]items needed[/] to attack the monster, your [indian_red]confidence[/] will be decreased, and when your [indian_red]confidence[/] is 0, you will lose the game."
        self.keyCommand = f"[cyan1]COMMAND                                               DESCRIPTIONS[/]\n" \
                          f"[bright_white][green]'go <east/west/north/south>'[/] or [green]'go <e/w/n/s>'[/]--------Move between areas\n" \
                          f"[green]'get <the name of the item>'[/] -------------------------Pick up the item\n" \
                          f"[green]'look'[/] or [green]'l'[/]-----------------------------------------See monster's details\n" \
                          f"[green]'attack'[/] or [green]'a'[/]---------------------------------------Attack the monster\n" \
                          f"[green]'selfie'[/] or [green]'s'[/]---------------------------------------View your character info\n" \
                          f"[green]'help'[/] or [green]'h'[/]-----------------------------------------See command information\n" \
                          f"[green]'quit'[/] or [green]'q'[/]-----------------------------------------Save and Exit the game[/]\n"
        self.history_message = ""
        self.short_hair_file_path = '../resource/short_hair.txt'
        self.long_hair_file_path = '../resource/long_hair.txt'
        self.display = Display()
        self.leaderboard = Leaderboard()

    def main_menu(self):
        self.display.clear_screen()
        print(self.display.print_ascii_art('../resource/main_menu.txt'))
        self.display.draw()
        print("1, [thistle3]LOG IN[/]\n"
              "2, [thistle3]SIGN UP[/]\n"
              "3, [thistle3]FORGET PASSWORD[/]\n"
              "4, [thistle3]QUIT[/]")
        self.display.draw()
        print("[orchid1 italic bold]💡Hints:[/]")
        print("- Type a number to choose menu option")
        self.display.draw()
        try:
            choice = self.display.colored_input("# ", color="sandy_brown")
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_registration()
            elif choice == "3":
                self.handle_password_reset()
            elif choice == "4":
                self.handle_quit_menu1()
            else:
                print("[deep_pink2]Invalid command[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        except Exception as e:
            print(f"[deep_pink2]An error occurred: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

    def handle_login(self, username=None, password=None):
        # Checking if the username and password are None,
        # if they are, then create new username and password
        if username is None and password is None:
            self.display.clear_screen()
            self.display.draw()
            print("[orchid1 italic bold]💡Hints:[/]")
            print("- Type 'back' or 'b' to go back to the main menu")
            self.display.draw()
            username = input("\033[93mEnter your username: \033[0m")
            if username.lower() == 'back' or username.lower() == 'b':
                self.menu1 = True
                self.menu2 = False
                return
            password = maskpass.askpass(prompt="\033[93mEnter your password: \033[0m", mask="*")
            if password.lower() == 'back' or password.lower == 'b':
                self.menu1 = True
                self.menu2 = False
                return

        self.display.draw()
        result = self.user_manager.login(username, password)
        if result == 'Logged in successfully.':
            self.username = username
            self.menu1 = False
            self.menu2 = True
        else:
            self.menu1 = True
            self.menu2 = False

    def handle_registration(self):
        self.user_manager.reload_data()
        self.display.clear_screen()
        self.display.draw()
        print("[orchid1 italic bold]💡Hints:[/]")
        print("- Type 'back' or 'b' to go back to main menu")
        self.display.draw()

        # Asking for user info
        while True:
            # Asking for username
            username = input("\033[93mChoose your username: \033[0m")
            if username.lower() == "back" or username.lower() == "b":
                self.menu1 = True
                self.menu2 = False
                return
            if not self.user_manager.username_verify(username):
                valid_password = False
                # Asking for password
                while not valid_password:
                    #https://pypi.org/project/maskpass/ for how to use maskpass
                    password = maskpass.askpass(prompt="\033[93mChoose your password(At least 6 characters): \033[0m", mask="*")
                    if password.lower() == "back" or password.lower() == "b":
                        self.menu1 = True
                        self.menu2 = False
                        return
                    if len(password) < 6:
                        print("[deep_pink2]Your password must be at least [green]6[/] characters long. Please try again.[/]")
                        maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                        self.display.clear_last_two_lines(3)
                        continue
                    # Confirming Password
                    confirm_password = maskpass.askpass(prompt="\033[93mConfirm your password: \033[0m", mask="*")
                    if confirm_password.lower() == "back" or confirm_password.lower() == "b":
                        self.menu1 = True
                        self.menu2 = False
                        return
                    if password != confirm_password:
                        print("[deep_pink2]Your password and confirmation do not match. Please try again.[/]")
                        maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                        
                        self.display.clear_last_two_lines(4)
                        continue
                    valid_password = True  # If password is valid, go to email

                # Asking for email address
                while True:
                    email = input("\033[93mEnter your email address: \033[0m")
                    self.display.draw()
                    if email.lower() == "back" or email.lower() == "b":
                        self.menu1 = True
                        self.menu2 = False
                        return
                    # Checking the email format
                    if '@' in email and '.' in email.split('@')[-1]:
                        break
                    else:
                        print("[deep_pink2](⋟﹏⋞)Oops, invalid email format. please enter a valid email address.[/]")
                        maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                        self.display.clear_last_two_lines(4)
                break

        self.user_manager.reload_data()
        registration_result = self.user_manager.create_user(username, password, email)

        if registration_result == "User created successfully.":
            self.handle_login(username=username, password=password)

        else:
            # Showing an error message if registration failed
            print(f"[deep_pink2]{registration_result}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            pass


    def handle_password_reset(self):
        self.user_manager.reset_password()

    def handle_quit_menu1(self):
        exit(0)

    def secondary_menu(self):
        self.display.clear_screen()
        self.display.draw()
        print("1, [thistle3]NEW GAME[/]\n"
              "2, [thistle3]LOAD GAME[/]\n"
              "3, [thistle3]LEADERBOARD[/]\n"
              "4, [thistle3]RULES[/]\n"
              "5, [thistle3]DELETE ACCOUNT[/]\n"
              "6, [thistle3]DELETE CHARACTERS[/]\n"
              "7, [thistle3]QUIT GAME[/]")
        self.display.draw()
        print("[orchid1 italic bold]💡Hints:[/]")
        print("- Type a number to choose menu option")
        print("- Type 'back' or 'b' to go back to main menu")
        self.display.draw()
        choice = self.display.colored_input("# ", color="sandy_brown")
        if choice == "1":
            self.handle_new_game()
        elif choice == "2":
            self.handle_load_game()
        elif choice == "3":
            self.handle_leaderboard()
        elif choice == "4":
            self.handle_rules()
        elif choice == "5":
            self.handle_delete_account()
        elif choice == "6":
            self.handle_delete_character()
        elif choice == "7":
            self.display.clear_screen()
            print(self.display.print_ascii_art('../resource/good_bye.txt'))
            print()
            maskpass.askpass(prompt="\033[92mPress 'Enter' to exit...\033[0m", mask=" ")
            self.handle_quit()
        elif choice.lower() == "back" or choice.lower() == "b":
            self.menu2 = False
            self.menu1 = True
        else:
            print("[deep_pink2]Invalid Input[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def handle_new_game(self):
        self.display.clear_screen()
        self.history_message = ''
        while True:
            self.display.clear_screen()
            self.display.draw()
            print("[orchid1 italic bold]💡Hints:[/]")
            print("- Type 'back' or 'b' to go back to the menu")
            self.display.draw()
            #Creating a new character when users start a new game
            name = self.display.colored_input("Enter your character's name: ", color="gold1").strip()
            if name.lower() == "back" or name.lower() == "b":
                self.menu2 = True
                return
            self.character_name = name
            user_data = self.user_manager.users.get(self.username, {'characters': []})
            # Checking if the name of character already exists
            if any(char['name'] == name for char in user_data['characters']):
                print("[deep_pink2]Error: Character name already exists. Please choose a different name.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            else:
                break

        while True:
            self.display.draw()
            hair_length = self.display.colored_input("Choose hair length ('Long/Short'): ", color="gold1").strip().lower()
            if hair_length.lower() == "back" or hair_length.lower() == "b":
                self.menu2 = True
                return
            elif hair_length not in ["short", "long"]:
                print("[deep_pink2](＞﹏＜)Oops, please type[/]'long/short'")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            else:
                break

        hair_color = 'Unknown'
        while hair_color == 'Unknown':
            self.display.draw()
            print(f"[gold1]Choose hair color:[/]")
            print("1: Cyan")
            print("2: Red")
            print("3: Yellow")
            color_options = {'1': 'cyan', '2': 'red', '3': 'yellow'}
            hair_color_choice = self.display.colored_input("Select option ('1, 2, or 3'): ", color="gold1").strip()
            hair_color = color_options.get(hair_color_choice, "Unknown")
            if hair_color_choice.lower() == "back" or hair_color_choice.lower() == "b":
                self.menu2 = True
                return
            elif hair_color == 'Unknown':
                print("[deep_pink2](＞﹏＜)Oops, please type a number[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        eye_color = 'Unknown'
        while eye_color == 'Unknown':
            self.display.draw()
            print(f"[gold1]Choose eye color:[/]")
            print("1: Cyan")
            print("2: Green")
            print("3: Red")
            color_options = {'1': 'cyan', '2': 'green', '3': 'red'}
            eye_color_choice = self.display.colored_input("Select option ('1, 2, or 3'): ", color="gold1").strip()
            eye_color = color_options.get(eye_color_choice, "Unknown")
            if eye_color_choice.lower() == "back" or eye_color_choice.lower() == "b":
                self.menu2 = True
                return
            elif eye_color == 'Unknown':
                print("[deep_pink2](＞﹏＜)Oops, please type a number[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        character_manager = Character(name, hair_length, hair_color, eye_color)
        result = character_manager.create_character(self.username, name, hair_length, hair_color, eye_color)

        if hair_length == 'short':
            print(self.display.print_ascii_art(self.short_hair_file_path, 'character', hair_color, eye_color))
        elif hair_length == 'long':
            print(self.display.print_ascii_art(self.long_hair_file_path, 'character', hair_color, eye_color))
        print(f'[italic]{result}[/]')
        print()
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        # Restarting the game
        self.confidence = 100
        self.current_room = 'Maple Sanctuary'
        self.rooms = {
            'Maple Sanctuary': {'East': 'Moonlit Timberland', 'Item': 'Confidence Booster'},
            'Moonlit Timberland': {'West': 'Maple Sanctuary', 'North': 'Maple Sanctuary', 'South': 'Dewdrop Dell',
                                   'East': 'Emerald Canopy', 'Item': 'Smart Planner'},
            'Whispering Pines': {'South': 'Moonlit Timberland', 'East': 'Pine Haven', 'Monster': 'Diet Monster'},
            'Dewdrop Dell': {'North': 'Moonlit Timberland', 'East': 'Redwood Haven', 'Monster': 'Balance Monster'},
            'Pine Haven': {'South': 'Emerald Canopy', 'East': 'Walnut Retreat', 'West': 'Whispering Pines',
                           'Item': 'Mirror'},
            'Emerald Canopy': {'West': 'Moonlit Timberland', 'North': 'Pine Haven', 'South': 'Redwood Haven',
                               'East': 'Cypress Cottage', 'Monster': 'Overthinking Monster'},
            'Redwood Haven': {'West': 'Dewdrop Dell', 'East': 'Silver Birch Copse', 'North': 'Emerald Canopy',
                              'Item': 'Clock'},
            'Walnut Retreat': {'West': 'Pine Haven', 'South': 'Cypress Cottage', 'Monster': 'Insecure Monster'},
            'Cypress Cottage': {'West': 'Emerald Canopy', 'South': 'Silver Birch Copse', 'North': 'Walnut Retreat',
                                'East': 'Forest Haven', 'Monster': 'Glass Ceiling Monster'},
            'Silver Birch Copse': {'West': 'Redwood Haven', 'North': 'Cypress Cottage',
                                   'Monster': 'Harassment Monster'},
            'Forest Haven': {'West': 'Cypress Cottage', 'Item': 'Book'},
            'Mystic Moss Grove': {'West': 'Silver Birch Copse', 'North': 'Forest Haven', 'Item': 'Pizza'},
            'Enchanted Thicket': {'West': 'Walnut Retreat', 'South': 'Forest Haven', 'Item': 'Key'},
            'Sunbeam Glade': {'West': 'Forest Haven', 'Item': 'Jumping Rope'}
        }
        self.inventory = []
        self.map.x, self.map.y = self.map.get_coordinates_from_room_name(self.current_room)
        self.bonus = 0
        self.message = ''
        self.leaderboard.save_score(self.character_name, self.username, self.bonus)
        self.save_load.save_game(self.username, self.character_name, self.current_room, self.inventory,
                                 self.confidence, self.rooms)
        self.game_introduction()
        self.menu2 = False
        self.play = True

    def handle_load_game(self):
        loaded_data = self.save_load.load_game(self.username)
        if loaded_data is not None:
            if loaded_data == 'back':
                self.play = False
                self.menu2 = True
            else:
                character, current_room, inventory, rooms, confidence = loaded_data
                self.character_name = character['name']
                loaded_bonus = self.user_manager.get_bonus(self.username, self.character_name)
                if loaded_bonus == 130:
                    self.display.draw()
                    print("This character achieved the highest level of bonus points.")
                    print("By loading the character, it will begin the new game.")
                    answer = self.display.colored_input("[deep_pink2]Do you want to restart the game?[/] [Y/N]\n"
                                                        "[gold1]Answer:[/] ").lower()
                    if answer == "y":
                        self.handle_reset_game()
                        self.play = True
                        self.menu2 = False
                    elif answer == "n":
                        return
                    else:
                        print("[deep_pink2]Invalid Input[/]")
                        maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                else:
                    self.character_name = character['name']
                    self.current_room = current_room
                    self.inventory = inventory
                    self.confidence = confidence
                    self.rooms = rooms
                    self.map.x, self.map.y = self.map.get_coordinates_from_room_name(self.current_room)
                    print(f"[dark_slate_gray2]Game loaded successfully for character '{character['name']}'.[/]")
                    maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
                    self.play = True
                    self.menu2 = False
        else:
            self.play = False
            self.menu2 = True
        loaded_score = self.leaderboard.load_score(self.character_name, self.username)
        if loaded_score is not None:
            self.bonus = loaded_score
        else:
            self.bonus = 0

    def handle_reset_game(self):
        self.confidence = 100
        self.current_room = 'Maple Sanctuary'
        self.rooms = rooms
        self.inventory = []
        self.map = Map(3, 6, 0, 1, paths)
        self.bonus = 0

        # Saving game state
        self.save_load.save_game(self.username, self.character_name, self.current_room, self.inventory,
                                   self.confidence, self.rooms)

        # Resetting and saving bonus and score
        self.user_manager.reset_bonus(self.username, self.character_name)
        self.leaderboard.reset_leaderboard_score(self.character_name)

    def handle_leaderboard(self):
        self.display.clear_screen()
        self.display.draw()
        self.leaderboard.load_leaderboard()
        self.display.draw()
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def handle_rules(self):
        self.display.clear_screen()
        print("Collect the right item(s) to defeat monsters. Find more hints by observing each monster\n")
        print(self.keyCommand)
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def handle_delete_account(self):
        while True:
            self.display.clear_screen()
            self.display.draw()
            print("[orchid1 italic bold]💡Hints:[/]")
            print("- Type 'Y' or 'y' to delete your account")
            print("- Type 'N' or 'n' to go back")
            self.display.draw()
            # Making sure the user really wants to delete the account
            print("[deep_pink2]Your account will be deleted. Are you sure you want to continue?[/] ('Y/N')")
            answer = self.display.colored_input("[gold1]Your answer:[/] ", ).lower()
            if answer == "y":
                self.user_manager.delete_account(self.username)
                self.menu2 = False
                self.menu1 = True
                break
            elif answer == "n":
                return
            else:
                self.display.draw()
                print("[deep_pink2]Invalid Input[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def handle_delete_character(self):
        deleted_character = self.user_manager.delete_character(self.username)
        if deleted_character:
            if deleted_character == 'back' or deleted_character == 'b':
                self.menu2 = True
            else:
                self.user_manager.delete_character(self.username)


    def handle_quit(self):
        quit()

    def game_introduction(self):
        self.display.clear_screen()
        print(self.display.print_ascii_art('../resource/welcome.txt'))
        self.display.draw()
        print(self.instruction)
        self.display.draw()
        print(self.keyCommand)
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def find_character_by_name(self, character_name):
        with open('users.json', 'r') as file:
            users_data = json.load(file)
        user_data = users_data.get(self.username, {})
        for character in user_data.get('characters', []):
            if character.get('name') == character_name:
                return character
        return None
    def game_loop(self):
        while self.play and self.confidence > 0:
            self.leaderboard.save_score(self.character_name, self.username, self.bonus)
            self.current_room = self.map.room_map.get((self.map.x, self.map.y), "Unknown room")
            self.room_info = self.rooms.get(self.current_room, {})
            # Showing the details of the map, the room info, the move and current location fot the user
            self.display.clear_screen()
            print("[orchid1 italic bold]Map of the wood:[/]")
            self.map.print_map()
            if self.history_message != "":
                print(self.history_message)
            print(f"You are in the '{self.current_room}'")
            self.display.draw()
            # Showing the details of user info
            print("[orchid1 italic bold]Your Details:[/]")
            print(f"Inventory : {self.inventory}")
            print(f"Your current confidence: {self.confidence}")
            self.display.draw()
            # When there are still monsters in the rooms, users can play the game
            if self.any_monsters_left():
                if "Monster" in self.room_info:
                    encountered_monster = self.room_info['Monster']
                    monster = monsters.get(encountered_monster)
                    print("[orchid1 italic bold]Room Details:[/]")
                    print(f"You encounter a '{encountered_monster}'!")
                    if len(encountered_monster.split()) == 3:
                        print(self.display.print_ascii_art(
                            f'../resource/{encountered_monster.split()[0].lower()}{encountered_monster.split()[1].lower()}_monster.txt', 'monsters'))
                    elif len(encountered_monster.split()) == 2:
                        print(
                            self.display.print_ascii_art(f'../resource/{encountered_monster.split()[0].lower()}_monster.txt', 'monsters'))
                    print(f"[bold italic]Monster's health: {monster.health}[/]")
                    self.display.draw()
                    print("[orchid1 italic bold]💡Hints:[/]")
                    print("[bright_white]- If you don't have the item(s) to attack the monster, you can go to other rooms and the monster won't attack you[/]")
                    print("[bright_white]- Type [green]'look'[/] or [green]'l'[/] to view the info of the monster and the items required to attack the monster[/]")
                    print("[bright_white]- Type [green]'attack'[/] or [green]'a'[/] to attack the monster[/]")

                elif "Item" in self.room_info:
                    item = self.room_info["Item"]
                    if len(item.split()) == 2:
                        ascii_item = self.display.print_ascii_art(
                            f'../resource/{item.split()[0].lower()}_{item.split()[1].lower()}.txt', 'items')
                    elif len(item.split()) == 1:
                        ascii_item = self.display.print_ascii_art(f'../resource/{item.split()[0].lower()}.txt', 'items')
                    print("[orchid1 italic bold]Room Details:[/]")
                    if item[0] in 'AEIOUaeiou':
                        print(f"You see an '{self.room_info['Item']}'!")
                        print(ascii_item)
                    else:
                        print(f"You see a '{self.room_info['Item']}'")
                        print(ascii_item)
                    self.display.draw()
                    print("[orchid1 italic bold]💡Hints:[/]")
                    print(f"[bright_white]- Type [green]'get {item.lower()}[/]' to get the item[/]")
                else:
                    print("[orchid1 italic bold]No Room Details:[/]")
                    print(f"[deep_pink2]Oops, there's nothing special here now.[/]\n")
                    if not self.message:
                        self.display.draw()
                        print("[orchid1 italic bold]💡Hints:[/]")

                if self.message != "":
                    print(self.message)
                    self.display.draw()
                    print("[orchid1 italic bold]💡Hints:[/]")
                print("[bright_white italic]- Type [green]'[gold1 bold]go[/] east/west/south/north'[/] or '[green][gold1 bold]go[/] e/w/s/n[/]' to move between areas.[/]")
                print("[bright_white italic]- Type [green]'selfie'[/] or [green]'s'[/] to view your character information.[/]")
                print("[bright white italic]- Type [green]'quit'[/] or [green]'q'[/] to quit the game")
                print("[bright_white italic]- Type [green]'help'[/] or [green]'h'[/] to view more command information[/]")
                self.display.draw()
                user_input = self.display.colored_input("Enter your command: ", color="gold1").lower().split(' ')
                self.process_command(user_input)
            # if no monster is left in the game
            else:
                self.play = False
                if not self.quit_game:
                    self.confidence = 100
                    self.current_room = 'Maple Sanctuary'
                    self.rooms = rooms
                    self.inventory = []
                    self.save_load.save_game(self.username, self.character_name, self.current_room, self.inventory,
                                               self.confidence, self.rooms)
                    self.handle_ending()

    def any_monsters_left(self):
        for room_info in self.rooms.values():
            if 'Monster' in room_info:
                return True
        return False

    def handle_ending(self):
        self.display.clear_screen()
        self.display.typing_effect("Congratulations! You have cured all the monsters in the wood.\n\n")
        time.sleep(1)
        self.display.typing_effect("The monsters want to have a word with you.\n")
        time.sleep(1)
        self.display.draw()
        self.display.typing_effect('Diet Monster says with enthusiasm, \n"The pizza is so yummy! '
                           'I can eat anything I like, \nbut to stay healthy and strong, I make sure to exercise with '
                           'your jumping rope too!"\n\n',
                           color_words={"pizza": Fore.YELLOW, "jumping rope": Fore.YELLOW})
        time.sleep(1)
        self.display.typing_effect('Balance Monster shares, \n"I\'m going to make plans with the smart planner to balance '
                           'my life, \nso it feels just right and not too much to handle!"\n\n',
                           color_words={"smart planner": Fore.YELLOW})
        time.sleep(1)
        self.display.typing_effect('Overthinking Monster says, \n"When I see myself in the mirror, I realize it\'s '
                           'time to take action, not just ponder. \nOtherwise, nothing will change, and I might miss '
                           'out on something wonderful!"\n\n', color_words={"mirror": Fore.YELLOW})
        time.sleep(1)
        self.display.typing_effect('The Insecure Monster shares, \n"When I read books, I focus on me. \nI\'ve learned '
                           'to love myself instead of worrying about what others think. My life deserves the best!"\n\n',
                           color_words={"books": Fore.YELLOW})
        time.sleep(1)
        self.display.typing_effect('Glass Ceiling Monster says, \n“With the key of awareness and action, I\'ve broken '
                           'through barriers. \nNow, I see a world where everyone, regardless of gender, can reach '
                           'their fullest potential. \nLet\'s build a future of equality and opportunity for all!”\n\n',
                           color_words={"key": Fore.YELLOW})
        time.sleep(1)
        self.display.typing_effect('The Harassment Monster cheers, \n"I never knew how strong you are. You can achieve '
                           'ANYTHING you set your mind to. \nDon\'t let anyone hurt you again. You\'ve got this!"\n\n',
                           color_words={"ANYTHING": Fore.YELLOW})
        self.display.draw()
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        self.display.clear_screen()
        self.display.typing_effect('You\'ve faced so much in life. \nEvery monster you encountered served as a valuable '
                           'teacher, shaping you into the amazing person you are today. \nEmbrace the strength '
                           'you\'ve gained from those challenges!\n\n')
        time.sleep(1)
        self.display.typing_effect('Thank you for playing our game and hope your confidence is 100%! ʕっ•ᴥ•ʔっ\n',
                           color_words={"ʕっ•ᴥ•ʔっ": Fore.CYAN})
        self.display.draw()
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        self.menu2 = True

    def process_command(self, user_input):
        if not user_input:
            return

        action = user_input[0]
        argument = " ".join(user_input[1:]).title() if len(user_input) > 1 else ""
        # Mapping the direction
        direction_map = {
            'e': 'east',
            'w': 'west',
            'n': 'north',
            's': 'south'
        }

        if action == "go":
            self.message = ""
            direction = argument.lower()
            direction_word = direction_map.get(direction, direction)
            result = self.map.move(direction)
            if result != "invalid input":
                self.current_room = self.map.room_map.get((self.map.x, self.map.y), "Unknown room")
                self.history_message = "You moved '" + direction_word + "'"
            else:
                print("[deep_pink2](⋟﹏⋞)Oops, please type [green]'go east/west/south/north'[/] or [green]type 'go e/w/s/n'[/] to move between areas[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")


        elif action == "get":
            item = argument
            current_room_items = self.rooms[self.current_room].get("Item", "")
            if item:
                # Checking if the item exists in the current room
                if item == current_room_items:
                    # Adding item to inventory if not already there
                    if item not in self.inventory:
                        if item.lower() == 'confidence booster':
                            if self.confidence < 100:
                                time.sleep(1)
                                print("[indian_red]Confidence +20[/]")
                                time.sleep(1)
                                self.message = "Your 'Confidence' is boosted!"
                                self.confidence += 20
                                self.rooms[self.current_room].pop("Item", None)
                            else:
                                print("[deep_pink2]You have full confidence, so you are confident enough to beat the monsters, no need to get the confidence booster.[/]")
                                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

                        else:
                            self.inventory.append(item)
                            self.message = f"'{item}' retrieved!"
                            self.display.draw()
                            print()
                            self.rooms[self.current_room].pop("Item", None)
                else:
                    if item in self.inventory:
                        print(f"[deep_pink2]You already have {item} in your inventory[/]")
                        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
                    else:
                        print(f"[deep_pink2]Invalid command, please enter the name of the item[/]")
                        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            else:
                # No item specified in the command
                print("[deep_pink2]Invalid command: No item specified.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")



        elif action == "look" or action == "l":
            self.display.clear_screen()
            monster_name = self.room_info.get("Monster")
            if monster_name:
                monster = monsters.get(monster_name)
                if monster:
                    if len(monster.name.split()) == 3:
                        print(self.display.print_ascii_art(
                            f'../resource/{monster.name.split()[0].lower()}{monster.name.split()[1].lower()}_monster.txt', 'monsters'))
                    elif len(monster.name.split()) == 2:
                        print(
                            self.display.print_ascii_art(f'../resource/{monster.name.split()[0].lower()}_monster.txt', 'monsters'))
                    print(f"{monster.description}\n")
                    time.sleep(1)
                    self.display.print_monster_info(monster.name, monster.health, monster.attack, monster.loot,
                                                         monster.items_required)
                    print()
                    time.sleep(1)
                    print(f"{monster.hint}\n")
                    time.sleep(1)

                    maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
                else:
                    print("[deep_pink2]There's no monster here.[/]")
            else:
                print("[deep_pink2]Sorry, there is nothing to look at. :([/]")


        elif action == "quit" or action == "q":
            self.display.clear_screen()
            print("(╬☉д⊙)Oh!")
            self.display.draw()
            print("[orchid1 italic bold]💡Hints:[/]")
            print("- Type 'Y' or 'y' to save and exit the game")
            print("- Type 'N' or 'n' to go back")
            self.display.draw()
            answer = self.display.colored_input("[deep_pink2]Save and Exit game? [/]'Y/N'\n[gold1]Your answer:[/]").upper()
            if answer == "Y":
                self.save_load.save_game(self.username, self.character_name, self.current_room, self.inventory,
                                           self.confidence, self.rooms)
                self.display.clear_screen()
                self.play = False
                self.menu2 = True
                self.quit_game = True
            elif answer == "N":
                pass
            else:
                print("[]Invalid Command")

        elif action == "help" or action == "h":
            self.display.clear_screen()
            print(self.keyCommand)
            maskpass.askpass(prompt="\033[92mPress 'Enter' to go back...\033[0m", mask=" ")

        elif action == "attack" or action == "a":
            self.display.clear_screen()
            monster_name = self.room_info.get("Monster")
            if monster_name:
                self.handle_monster_encounter(monster_name)
            else:
                print("There's no monster to attack here.")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        elif action == 'selfie' or action == 's':
            self.display.clear_screen()
            character = self.find_character_by_name(self.character_name)
            character_name = character['name']
            hair_length = character['hair_length']
            hair_color = character['hair_color']
            eye_color = character['eye_color']
            self.display.draw()
            print("[orchid1 italic bold]Your Character Details:[/]")
            if hair_length == 'short':
                print(self.display.print_ascii_art(self.short_hair_file_path,'character', hair_color, eye_color))
            elif hair_length == 'long':
                print(self.display.print_ascii_art(self.long_hair_file_path,'character', hair_color, eye_color))
            print(f"[gold1]Your Name:[/] {character_name.capitalize()}")
            print(f"[gold1]Your Hair Length[/]: {hair_length.capitalize()}")
            print(f"[gold1]Your Hair Color:[/] {hair_color.capitalize()}")
            print(f"[gold1]Your Eye Color:[/] {eye_color.capitalize()}")
            self.display.draw()
            print()
            maskpass.askpass(prompt="\033[92mPress 'Enter' to go back...\033[0m", mask=" ")


        else:
            print(f"[deep_pink2](⋟﹏⋞)Oops, invalid command, please type 'help' to see command options.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def handle_monster_encounter(self, monster_name):
        monster = monsters.get(monster_name)
        if not monster:
            print("There's no monster here.")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return

        # Checking if the user has required items
        has_required_items = all(item in self.inventory for item in monster.items_required)
        if has_required_items:
            damage = 100 // len(monster.items_required)
            monster.health -= damage
            print()
            print("₍₍٩( ᐛ )۶₎₎♪")
            print(f"{monster.name} has been attacked by you!")
            print()
            time.sleep(1)
            print(f"[indian_red]{monster.name} says:[/] [italic]I never thought you could be so strong and powerful! Maybe my time has come...[/]")
            print("[indian_red]_(´ཀ`」 ∠)_[/]")
            print()
            time.sleep(1)
            print(f"[indian_red]{monster.name} health -{damage}[/]")
            if len(monster.items_required) >= 2:
                if monster.health > 0:
                    time.sleep(1)
                    self.display.draw()
                    print("[orchid1 italic bold]💡Hints:[/]")
                    print(f"- You may need to attack {monster.name} multiple times till he dies.")
                    self.display.draw()

        else:
            time.sleep(1)
            print()
            print(f"[plum2]( ´•︵•` ) Oh no! You don't have the items in your inventory to attack the monster, {monster.name} will say something to attack you![/]")
            time.sleep(1)
            print()
            print(f"[hot_pink3]{monster.name} said:[/] {monster.replace_word(self.username, self.character_name)}\n")
            time.sleep(1)
            print(f"[indian_red]Your confidence -{monster.attack}")
            self.confidence -= monster.attack

        if monster.health == 0:
            time.sleep(1)
            print()
            print("╰(*°▽°*)╯")
            print(f"'{monster.name}' has been defeated.You've gained '{monster.loot}' and '{monster.bonus}' points.")
            self.display.draw()
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            self.rooms[self.current_room].pop("Monster", None)
            self.bonus += monster.bonus
            self.leaderboard.save_score(self.character_name, self.username, self.bonus)
        elif self.confidence == 0:
            time.sleep(1)
            self.display.clear_screen()
            print(self.display.print_ascii_art('../resource/game_over.txt'))
            print("[indian_red]Your confidence is 0, you are not self-assured enough to beat all the monsters in the wood, come back when you are stronger and more confident![/]\n")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to exit...\033[0m", mask=" ")
            self.confidence = 100
            self.current_room = 'Maple Sanctuary'
            self.rooms = rooms
            self.inventory = []
            self.save_load.save_game(self.username, self.character_name, self.current_room, self.inventory,
                                       self.confidence, self.rooms)
            self.menu2 = True
            self.play = False
        else:
            time.sleep(1)
            print(f"[bold italic]Monster's health: {monster.health}[/]")
            time.sleep(1)
            if self.confidence < 0:
                self.confidence = 0
            self.display.draw()
            time.sleep(1)
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def run_game(self):
        while self.run:
            if self.menu1:
                self.main_menu()
            elif self.menu2:
                self.secondary_menu()
            elif self.play:
                self.game_loop()


if __name__ == "__main__":
    game_play = GamePlay()
    game_play.run_game()
