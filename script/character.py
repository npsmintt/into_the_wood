import maskpass
from user_management import UserManager
from rich import print
from display import Display


class Character:
    def __init__(self, name, hair_length, hair_color, eye_color):
        self.name = name
        self.hair_length = hair_length
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.user_manager = UserManager()
        self.logged_in_user = None
        self.display = Display()

    def create_character(self, username, name, hair_length, hair_color, eye_color):
        self.logged_in_user = username
        user_data = self.user_manager.users.get(username)
        #Using Python generator expressios: https://peps.python.org/pep-0289/
        if any(char['name'] == name for char in user_data['characters']):
            print("[deep_pink2](＞﹏＜)Oops: character name already exists.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        #Adding the info of the new created character to the json file
        new_character = Character(name, hair_length, hair_color, eye_color)
        user_data['characters'].append(new_character.to_dict())
        #Scenarios where users are creating characters without their logged in accounts
        if not user_data or 'characters' not in user_data:
            print("[deep_pink2](＞﹏＜)Oops, you must be logged in to create a character.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        if username != self.logged_in_user:
            print("[deep_pink2](＞﹏＜)Oops, you can only create characters for your logged-in account.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        #Saving the character information for the current user
        self.user_manager.save_users()
        #Showing the character information for the current user
        return f"Character '{name}' has '{hair_length}' and '{hair_color}' hair, and her eyes are '{eye_color}'"
    #Jason file formatting
    def to_dict(self):
        return {
            'name': self.name,
            'hair_length': self.hair_length,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color
        }
