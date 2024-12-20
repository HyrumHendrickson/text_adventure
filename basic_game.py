class Player:
    def __init__(self, location, inventory):
        self.location = location
        self.inventory = inventory
        self.isPlaying = True


class Location:
    def __init__(self, name, description, connections, items):
        self.name = name
        self.description = description
        self.connections = connections
        self.items = items


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def create_game_world():
    locations = {
        "forest": Location(
            "Forest",
            "A dark and mysterious forest with tall, ancient trees.",
            ["cave", "village"],
            [
                Item("mushroom", "A glowing mushroom that seems to pulse with an eerie light"),
                Item("stick", "A sturdy wooden stick, good for defense or crafting"),
                Item("berries", "A handful of wild berries, some look edible"),
            ],
        ),
        "cave": Location(
            "Cave",
            "A dark, cold cave with echoing sounds and damp stone walls.",
            ["forest", "castle"],
            [
                Item("torch", "An old rusty torch that might still provide light"),
                Item("rock", "A sharp-edged rock that could be used as a tool or weapon"),
                Item("rope", "A long, slightly frayed rope"),
            ],
        ),
        "castle": Location(
            "Castle",
            "A big, scary castle with tall walls and crumbling stone towers.",
            ["cave", "tower"],
            [
                Item("sword", "An ancient sword with a worn leather grip"),
                Item("shield", "A rusty iron shield with faded emblems"),
                Item("helmet", "A dented steel helmet"),
            ],
        ),
        "village": Location(
            "Village",
            "A small, abandoned village with broken huts and overgrown paths.",
            ["forest", "tower"],
            [
                Item("map", "An old, faded map showing some landmarks"),
                Item("bucket", "A wooden bucket with a cracked base"),
                Item("herbs", "A bundle of dried herbs, might be useful for healing"),
            ],
        ),
        "tower": Location(
            "Tower",
            "A crumbling stone tower overlooking the surrounding lands.",
            ["castle", "village"],
            [
                Item("book", "A dusty book filled with strange runes"),
                Item("key", "A heavy iron key with ornate carvings"),
                Item("lantern", "A brass lantern, slightly tarnished but functional"),
            ],
        ),
    }
    return locations


# Help command
def show_help():
    print("")
    print("Available Commands:")
    print("- go [location]    : Move to a connected location")
    print("- grab [item]      : Pick up an item in the current location")
    print("- drop [item]      : Drop an item from your inventory")
    print("- inventory        : Show what items you're carrying")
    print("- look             : Describe the current location")
    print("- help             : Show this help menu")
    print("- quit             : Exit the game")


def move_to_location(player, locations, destination):
    print("")
    current_location = locations[player.location]
    if destination in current_location.connections:
        player.location = destination
        new_location = locations[destination]
        look_around(player, locations)
    else:
        print(f"You cannot go to {destination} from here.")


def pick_up_item(player, locations, item_name):
    print("")
    current_location = locations[player.location]
    item_to_grab = None
    for item in current_location.items:
        if item.name.lower() == item_name.lower():
            item_to_grab = item
            break

    if item_to_grab:
        player.inventory.append(item_to_grab)
        current_location.items.remove(item_to_grab)
        print(f"You picked up the {item_name}.")
    else:
        print(f"There is no {item_name} here.")


def drop_item(player, locations, item_name):
    print("")
    item_to_drop = None
    for item in player.inventory:
        if item.name.lower() == item_name.lower():
            item_to_drop = item
            break

    if item_to_drop:
        player.inventory.remove(item_to_drop)
        locations[player.location].items.append(item_to_drop)
        print(f"You dropped the {item_name}.")
    else:
        print(f"You are not carrying a {item_name}.")


def show_inventory(player):
    print("")
    if len(player.inventory) > 0:
        print("You are carrying:")
        for item in player.inventory:
            print(f"- {item.name}")
    else:
        print("Your inventory is empty.")


def look_around(player, locations):
    print("")
    current_location = locations[player.location]
    print(f"You are in the {current_location.name}")
    print(current_location.description)
    print("")
    print("Connections:")
    for connection in current_location.connections:
        print(f"- {connection}")
    print("")
    print("Items here:")
    for item in current_location.items:
        print(f"- {item.name}")


def processInput(command, player, locations):

    # removes whitespace and converts the command to an array
    command = command.strip().split()

    # checks if the command is empty
    if len(command) == 0:
            return

    # get the first word of the command as the action (e.g., "go", "grab", "drop", etc.)
    action = command[0]

    # check the action and call the appropriate function
    if action == "go" and len(command) > 1:
        move_to_location(player, locations, command[1])
    elif action == "grab" and len(command) > 1:
        pick_up_item(player, locations, command[1])
    elif action == "drop" and len(command) > 1:
        drop_item(player, locations, command[1])
    elif action == "inventory":
        show_inventory(player)
    elif action == "look":
        look_around(player, locations)
    elif action == "help":
        show_help()
    elif action == "quit" or action == "exit":
        print("Thanks for playing!")
        player.isPlaying = False
    else:
        print("I don't understand that command.")


# Main game loop
def play_game():
    # Set up the game world
    locations = create_game_world()
    player = Player(location="forest", inventory=[])

    # Intro message for the game
    print("\nWelcome to the Text Adventure Game!")
    print("Type 'help' to see available commands.\n")
    look_around(player, locations)

    # Keep game running until player quits
    while player.isPlaying:
        command = input("\nWhat do you want to do? ")
        processInput(command, player, locations)
        

# Start the game
play_game()
