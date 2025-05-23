class Player:
    def __init__(self, location, inventory):
        self.location = location
        self.inventory = inventory
        self.isPlaying = True
    
    def inventory_list(self):
        return [item.name for item in self.inventory]


class Location:
    def __init__(self, name, description, connections, items):
        self.name = name
        self.description = description
        self.connections = connections
        self.items = items

    def items_list(self):
        return [item.name for item in self.items]


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Weapon(Item):
    def __init__(self, name, description, damage):
        super().__init__(name, description) 
        self.damage = damage

class Event: 
    def __init__(self, trigger, running = False, counter = 0, list = {}):
        self.trigger = trigger
        self.running = running
        self.counter = counter
        self.list = list


def create_game_world():
    locations = {
            "safehouse": Location(
                "Safehouse",
                "A secure and inconspicuous hideout equipped with the basics for planning missions.",
                ["warehouse", "city_center"],
                [
                    Item("blueprints", "Detailed blueprints of a high-security building"),
                    Item("disguise_kit", "A kit with wigs, glasses, and other tools for creating a new identity"),
                    Item("encrypted_phone", "A phone with state-of-the-art encryption software"),
                ],
            ),
            "warehouse": Location(
                "Warehouse",
                "An abandoned warehouse filled with crates and hidden passageways.",
                ["safehouse", "corporate_office"],
                [
                    Item("grappling_hook", "A compact grappling hook for scaling walls"),
                    Item("crowbar", "A sturdy crowbar, perfect for prying open locks"),
                    Item("tracking_device", "A small, discreet GPS tracking device"),
                ],
            ),
            "corporate_office": Location(
                "Corporate Office",
                "A sleek, modern office with tight security and cutting-edge technology.",
                ["warehouse", "penthouse"],
                [
                    Item("keycard", "An access card for restricted areas"),
                    Item("security_badge", "A fake security badge with convincing details"),
                    Item("microchip", "A tiny microchip containing sensitive information"),
                ],
            ),
            "city_center": Location(
                "City Center",
                "A bustling downtown area filled with civilians, shops, and hidden threats.",
                ["safehouse", "penthouse"],
                [
                    Item("watch", "A wristwatch with hidden gadgets like a laser cutter"),
                    Item("binoculars", "Compact binoculars with night vision"),
                    Item("smoke_grenade", "A small grenade that emits a thick smoke screen"),
                ],
            ),
            "penthouse": Location(
                "Penthouse",
                "A luxurious penthouse with floor-to-ceiling windows and a breathtaking view.",
                ["corporate_office", "city_center"],
                [
                    Item("safe", "A high-tech safe that may contain classified documents"),
                    Item("camera", "A hidden camera for gathering intelligence"),
                    Item("briefcase", "A locked briefcase with an unknown but important payload"),
                ],
            ),
        }

    return locations

#
commands = {}

# Help command
def help(command, player, locations):
    print("")
    print("Available Commands:")
    for name, cmd in commands.items():
        print(cmd["help"])
        
commands["help"] = {"run":help, "help": "- help -> Show available commands"}

def goto(command, player, locations):
    print("")
    if len(command) < 1:
        print("Please specify a location to go to.")
        return
    current_location = locations[player.location]

    location_to_go = get_match(command, current_location.connections)

    if location_to_go:
        player.location = location_to_go
        run_command(["look"], player, locations)
    else:
        print(f"You cannot go there from here.")
commands["go"] = {"run":goto, "help": "- go to [location] -> Move to a connected location"}
commands["walk"] = {"run":goto, "help": "- walk to [location] -> Move to a connected location"}
commands["run"] = {"run":goto, "help": "- run to [location] -> Move to a connected location"}

def grab(command, player, locations):
    print("")
    if len(command) < 1:
        print("Please specify an item to grab.")
        return

    current_location = locations[player.location]
    
    name_of_item = get_match(command, current_location.items_list())
    item_to_grab = [item for item in current_location.items if item.name == name_of_item]
    if len(item_to_grab) == 0:
        print(f"That item is not here.")
        return
    item_to_grab = item_to_grab[0]

    if item_to_grab:
        player.inventory.append(item_to_grab)
        current_location.items.remove(item_to_grab)
        print(f"You picked up the {name_of_item}.")
    else:
        print(f"There is no {name_of_item} here.")
commands["grab"] = {"run":grab, "help": "- grab [item] -> Move to a connected location"}
commands["pick"] = {"run":grab, "help": "- pick up [item] -> Pick up an item in the current location"}

def drop(command, player, locations):
    print("")
    if len(command) < 1:
        print("Please specify an item to drop.")
        return
    
    name_of_item = get_match(command, player.inventory_list())
    item_to_drop = [item for item in player.inventory if item.name == name_of_item]
    if len(item_to_drop) == 0:
        print(f"That item is not in your inventory.")
        return
    item_to_drop = item_to_drop[0]
    if item_to_drop:
        player.inventory.remove(item_to_drop)
        locations[player.location].items.append(item_to_drop)
        print(f"You dropped the {name_of_item}.")
    else:
        print(f"You are not carrying a {name_of_item}.")
commands["drop"] = {"run":drop, "help": "- drop [item] -> Drop an item from your inventory"}

def look(command, player, locations):
    if get_match(command, ["inventory"]):
        inventory(command, player, locations)
        return
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
commands["look"] = {"run":look, "help": "- look -> Describe the current location"}

def inventory(command, player, locations):
    print("")
    if len(player.inventory) > 0:
        print("You are carrying:")
        for item in player.inventory:
            print(f"- {item.name}")
    else:
        print("Your inventory is empty.")
commands["inventory"] = {"run":inventory, "help": "- inventory -> Show what items you're carrying"}

def quit(command, player, locations):
    print("Thanks for playing!")
    player.isPlaying = False
commands["quit"] = {"run":quit, "help": "- quit -> Exit the game"}

def blank(command, player, locations):
    print("Invalid command. Type 'help' to see available commands.")
commands["blank"] = {"run":blank, "help": ""}


events = []

# this event triggers if the player tries to grab the briefcase, the briefcase explodes and is destroyed
def briefcase_trap(self, command, player, locations):
    if (not (self.counter == 0)) or get_match(command, ["briefcase"]) == None:
        return False
    # add health to player object and have the explosion reduce health
    print("the briefcase explodes!!")
    # this line is clunky, fix it, it removes the briefcase from the room
    locations[player.location].items.remove([item for item in locations[player.location].items if item.name == "briefcase"][0])
    self.counter += 1
    return True
events.append(Event(briefcase_trap))

# this event triggers if the player tries to enter the corporate office
def penthouse_tripwire(self, command, player, locations):
    if (not (self.counter == 0)) or get_match(command, ["penthouse"]) == None:
        return False
    print("the tripwire is triggered! (but it did nothing)")
    self.counter += 1
    return True
events.append(Event(penthouse_tripwire))


# if the player is in the warehouse and tries to leave, this event triggers
def warehouse_collapse(self, command, player, locations):
    # return true if it triggers
    if self.running:
        if not(get_match(command, ["run", "exit"]) == None):
            print("you barely make it out as warehouse collapses behind you")
            player.location = "safehouse"
            self.running = False
            return True
        if not(get_match(command, ["desk", "hide"]) == None):
            print("you hide under a desk as the warehouse collapses around you. You get crushed and die")
            player.isPlaying = False
            self.running = False
            return True
        print("the walls are collapsing, hurry! do you run for the exit or hide under a desk?")
        return True
    if (not (self.counter == 0)) or get_match(command, ["go","walk","run"]) == None or (not player.location == "warehouse"):
        return False
    print("the walls begin to cave in as the warehouse begins to collapse, do you run for the exit or hide under a desk?")
    self.running = True
    self.counter += 1
    return True
events.append(Event(warehouse_collapse))


def run_events(command, player, locations):
    for event in events:
        if event.trigger(event, command, player, locations):
            return True
    return False
    

def processInput(input_text, player, locations):
    input_text = input_text.lower().strip()
    if input_text == "":
        input_text = "blank"
    input_arr = input_text.split()
    command = bring_action_to_front(input_arr, player, locations)
    return command

def bring_action_to_front(command, player, locations):
    for token in command:
        if token in commands:
            command.remove(token)
            command.insert(0, token)
            return command
    return ["blank"] + command

def run_command(command, player, locations):
    action = command.pop(0)
    commands[action]["run"](command, player, locations)

def get_match(tokens, list_to_check):
    for item in list_to_check:
        for token in tokens:
            if token == item:
                return token

    for item in list_to_check:
        split_item = item.split("_")
        for token in tokens:
            if token in split_item:
                return item
    return None

# Main game loop
def play_game():
    # Set up the game world
    locations = create_game_world()
    player = Player(location="safehouse", inventory=[])

    # Intro message for the game
    print("\nWelcome to the Text Adventure Game!")
    print("Type 'help' to see available commands.\n")
    run_command(["look"], player, locations)

    # Keep game running until player quits
    while player.isPlaying:
        input_text = input("\nWhat do you want to do? ")
        command = processInput(input_text, player, locations)

        # commands are only run if an event didn't run
        if not run_events(command, player, locations):
            run_command(command, player, locations)

# Start the game
play_game()
