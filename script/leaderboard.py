import utils
import json
from rich import print
from rich.console import Console
import maskpass
from display import Display


class Leaderboard:
    def __init__(self):
        self.logged_in_user = None
        self.console = Console()
        self.display = Display()
        self.leaderboard_file = 'leaderboard.json'
        self.leaderboard = utils.load_data(self.leaderboard_file)

    def save_score(self, name, username, bonus):
        data = []
        try:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("[deep_pink2](＞﹏＜)File not found. A new file will be created.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        except json.JSONDecodeError:
            print("[deep_pink2](＞﹏＜)Error reading the JSON file. Starting a new leaderboard.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        except Exception as e:
            print(f"[deep_pink2](＞﹏＜)An unexpected error occurred: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

        entry_found = False
        for entry in data:
            if entry.get("Player") == username and entry.get("Character name") == name:
                entry["score"] = bonus
                entry_found = True
                break

        if not entry_found:
            data.append({"Player": username, "Character name": name, "score": bonus})
        try:
            with open("leaderboard.json", 'w') as file:
                #https://docs.python.org/3/library/json.html
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"[deep_pink2](＞﹏＜)An error occurred while writing to the file: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def load_score(self, name, username):
        try:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
            for entry in data:
                if entry.get("Player") == username and entry.get("Character name") == name:
                    return entry.get("score", 0)
        except FileNotFoundError:
            print("[deep_pink2](＞﹏＜)Leaderboard file not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        except json.JSONDecodeError:
            print("[deep_pink2](＞﹏＜)Error reading the JSON file.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        except Exception as e:
            print(f"[deep_pink2](＞﹏＜)An unexpected error occurred: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def load_leaderboard(self):
        try:
            with open('leaderboard.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("[deep_pink2](＞﹏＜)Error: File not found or inaccessible.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return
        except json.JSONDecodeError:
            print("[deep_pink2](＞﹏＜)Error: JSON file is not properly formatted.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return
        except Exception as e:
            print(f"[deep_pink2](＞﹏＜)An unexpected error occurred: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return
        data.sort(key=lambda x: x.get("score", 0), reverse=True)
        print("LEADERBOARD\n"
              "NAME                SCORE")
        for entry in data:
            # Retrieving the character name, username, score from the entry.
            # If it doesn't exist, use "Unknown" or 0.
            name = entry.get("Character name", "Unknown")
            username = entry.get("Player", "Unknown")
            score = entry.get("score", 0)
            print(f"{name} ({username})".ljust(20) + f"{score}")

    def reset_leaderboard_score(self, character_name):
        try:
            with open('leaderboard.json', 'r') as file:
                leaderboard_data = json.load(file)

            # Resetting the score for the character
            for entry in leaderboard_data:
                if entry["Character name"] == character_name:
                    entry["score"] = 0

            # Saving the updated data to leaderboard.json
            with open('leaderboard.json', 'w') as file:
                json.dump(leaderboard_data, file, indent=4)

        except IOError:
            print("[deep_pink](＞﹏＜)Error: File not found or inaccessible.[/]")

    def delete_leaderboard(self, username):
        self.leaderboard = utils.load_data(self.leaderboard_file)
        self.leaderboard = [entry for entry in self.leaderboard if entry.get("Player") != username]
        utils.save_data(self.leaderboard, self.leaderboard_file)
