import sys
from rich.console import Console
from rich import print as rprint
import maskpass


class Map:
    def __init__(self, height, width, player_x, player_y, paths):
        self.height = height
        self.width = width
        self.x = player_x
        self.y = player_y
        self.paths = paths
        self.console = Console()
        self.room_map = {
            (0, 0): 'Whispering Pines',
            (0, 1): 'Maple Sanctuary',
            (1, 1): 'Moonlit Timberland',
            (0, 2): 'Dewdrop Dell',
            (1, 0): 'Pine Haven',
            (2, 1): 'Emerald Canopy',
            (1, 2): 'Redwood Haven',
            (2, 0): 'Walnut Retreat',
            (3, 1): 'Cypress Cottage',
            (2, 2): 'Silver Birch Copse',
            (3, 0): 'Enchanted Thicket',
            (4, 1): 'Forest Haven',
            (3, 2): 'Mystic Moss Grove',
            (5, 1): 'Sunbeam Glade'
        }

    def get_coordinates_from_room_name(self, room_name):
        reverse_map = {name: coords for coords, name in self.room_map.items()}
        default_coords = (0, 0)
        return reverse_map.get(room_name, default_coords)

    def move(self, direction):
        new_x, new_y = self.x, self.y

        if direction == "n" or direction == "north":
            new_y -= 1
            if new_y >= 0:
                # Check if moving from the second row to the first row
                if self.y == 1 and new_y == 0:
                    new_x -= 1  # Decrease x when moving north from second to first row
                # Check if moving from the third row to the first row
                if self.y == 2 and new_y == 1:
                    new_x += 1

                if new_x >= 0 and ((new_x, new_y), (self.x, self.y)) in self.paths:
                    self.x, self.y = new_x, new_y
                else:
                    self.console.print("Cannot go north", style="deep_pink2")
                    maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            else:
                self.console.print("Out of bound, cannot go north", style='deep_pink2')
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        elif direction == "s" or direction == "south":
            new_y += 1
            if new_y < self.height:
                # Check if moving from the first row to the second row
                if self.y == 0 and new_y == 1:
                    new_x += 1  # Increase x when moving south from first to second row

                # Check if moving from the second row to the third row
                if self.y == 1 and new_y == 2:
                    new_x -= 1  # Decrease x when moving south from second to third row

                if new_x < self.width and ((self.x, self.y), (new_x, new_y)) in self.paths:
                    self.x, self.y = new_x, new_y
                else:
                    self.console.print("Cannot go south", style="deep_pink2")
                    maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            else:
                print(self.x, self.y)
                self.console.print("Out of bound, cannot go south", style="deep_pink2")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        elif direction == "e" or direction == "east":
            new_x += 1
            # Check for a horizontal path to the right
            if new_x < self.width and ((self.x, self.y), (new_x, self.y)) in self.paths:
                self.x = new_x
            else:
                self.console.print("Out of bound, cannot go east", style="deep_pink2")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        elif direction == "w" or direction == "west":
            new_x -= 1
            # Check for a horizontal path to the left
            if new_x >= 0 and ((new_x, self.y), (self.x, self.y)) in self.paths:
                self.x = new_x
            else:
                self.console.print("Out of bound, cannot go west", style="deep_pink2")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        else:
            return "invalid input"
    #print_map is based on the tutorials at https://stackoverflow.com/questions/11703727/python-drawing-ascii-map
    def print_map(self):
        for y in range(self.height):
            # Adding an initial offset for the first and third rows
            if y in [0, 2]:
                sys.stdout.write("    ")
            for x in range(self.width):
                # Printing rooms in each row
                if y != 1 and x < 4:  # First and third rows have 4 rooms
                    if self.x == x and self.y == y:
                        rprint("[""[yellow1]u[/]""]", end="")  # User's current position
                    else:
                        sys.stdout.write("[ ]")  # Other rooms
                    # Horizontal paths for these rows
                    sys.stdout.write("-" if x < 3 else " ")

                elif y == 1 and x < 6:  # Second row has 6 rooms

                    if self.x == x and self.y == y:
                        rprint("[""[yellow1]u[/]""]", end="")
                    else:
                        sys.stdout.write("[ ]")  # Other rooms
                    # Horizontal paths for this row
                    sys.stdout.write("-" if x < 5 else " ")
            sys.stdout.write("\n")  # New line after each row of rooms

            # Printing vertical paths only between the first and second rows, and the second and third rows
            if y == 0 or y == 1:
                # The second row
                sys.stdout.write("     ")
                for x in range(1, 5):  # Four vertical paths
                    sys.stdout.write("|   ")
                sys.stdout.write("\n")


paths = [
    # Horizontal paths
    ((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0)),  # First row

    ((0, 1), (1, 1)), ((1, 1), (2, 1)), ((2, 1), (3, 1)
                                         ), ((3, 1), (4, 1)), ((4, 1), (5, 1)),  # Second row

    ((0, 2), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (3, 2)),  # Third row

    # Vertical paths
    ((1, 1), (0, 0)), ((2, 1), (1, 0)), ((3, 1), (2, 0)), ((
        4, 1), (3, 0)),  # Northward paths (second to first row
    ((0, 0), (1, 1)), ((1, 0), (2, 1)), ((2, 0), (3, 1)), ((
        3, 0), (4, 1)),  # Southward paths (first to second row
    ((0, 2), (1, 1)), ((1, 2), (2, 1)), ((2, 2), (3, 1)), ((
        3, 2), (4, 1)),  # Northward paths (third to second row
    ((1, 1), (0, 2)), ((2, 1), (1, 2)), ((3, 1), (2, 2)), ((
        4, 1), (3, 2)),  # Southward paths (second to third row
]

rooms = {
    'Maple Sanctuary': {'East': 'Moonlit Timberland', 'Item': 'Confidence Booster'},
    'Moonlit Timberland': {'West': 'Maple Sanctuary', 'North': 'Maple Sanctuary', 'South': 'Dewdrop Dell',
                           'East': 'Emerald Canopy',  'Item': 'Smart Planner'},
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
    'Silver Birch Copse': {'West': 'Redwood Haven', 'North': 'Cypress Cottage', 'Monster': 'Harassment Monster'},
    'Forest Haven': {'West': 'Cypress Cottage', 'Item': 'Book'},
    'Mystic Moss Grove': {'West': 'Silver Birch Copse', 'North': 'Forest Haven', 'Item': 'Pizza'},
    'Enchanted Thicket': {'West': 'Walnut Retreat', 'South': 'Forest Haven', 'Item': 'Key'},
    'Sunbeam Glade': {'West': 'Forest Haven', 'Item': 'Jumping Rope'},
}
