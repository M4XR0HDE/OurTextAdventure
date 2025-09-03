import sqlite3
import os
#from map import #placeholder for now

class Player:
    def add_item(self, item):
        self.inventory.append(item)
        if isinstance(item, Item):
            print(f"{item.name} has been added to {self.name}'s inventory.")
        else:
            print(f"{item} has been added to {self.name}'s inventory.")

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            if isinstance(item, Item):
                print(f"{item.name} has been removed from {self.name}'s inventory.")
            else:
                print(f"{item} has been removed from {self.name}'s inventory.")
        else:
            if isinstance(item, Item):
                print(f"{item.name} not found in inventory.")
            else:
                print(f"{item} not found in inventory.")
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.health = 100
        self.location = "Starting Room"
        self.base_attack = 5
        self.attack = self.base_attack
        self.equipped_weapon = None
        # Start with stick equipped
        self.inventory.append(stick)
        self.equip_weapon("Stick")

    def show_inventory(self):
        print(f"{self.name}'s Inventory:")
        for item in self.inventory:
            if isinstance(item, Item):
                equipped = " (equipped)" if self.equipped_weapon == item else ""
                print(f" - {item.name}{equipped}")
            else:
                print(f" - {item}")
        if self.equipped_weapon:
            print(f"Equipped weapon: {self.equipped_weapon.name} (+{self.equipped_weapon.value} attack)")

    def equip_weapon(self, item_name):
        for item in self.inventory:
            if isinstance(item, Item) and item.name == item_name:
                if self.equipped_weapon:
                    print(f"You already have {self.equipped_weapon.name} equipped. Remove it first.")
                    return
                self.equipped_weapon = item
                self.attack = self.base_attack + (item.value if item.value else 0)
                print(f"You equipped {item.name}. Attack is now {self.attack}.")
                return
        print(f"{item_name} not found in inventory.")

    def unequip_weapon(self):
        if self.equipped_weapon:
            print(f"You unequipped {self.equipped_weapon.name}.")
            # Put weapon back in inventory if not already there
            if self.equipped_weapon not in self.inventory:
                self.inventory.append(self.equipped_weapon)
            self.equipped_weapon = None
            self.attack = self.base_attack
        else:
            print("No weapon is currently equipped.")

    def attack(self, target):
        if target.health > 0:
            damage = self.attack
            target.health -= damage
            print(f"{self.name} attacks {target.name} for {damage} damage.")
            if target.health <= 0:
                print(f"{target.name} has been defeated.")
        else:
            print(f"{target.name} is already defeated.")

class Enemy:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.location = "Enemy Room"

    def attack(self, target):
        if target.health > 0:
            damage = self.attack_power
            target.health -= damage
            print(f"{self.name} attacks {target.name} for {damage} damage.")
            if target.health <= 0:
                print(f"{target.name} has been defeated.")
        else:
            print(f"{target.name} is already defeated.")

class Item:
    def __init__(self, name, description, usage, effect=None, value=None):
        self.name = name
        self.description = description
        self.usage = usage
        self.effect = effect
        self.value = value

    def show_info(self):
        print(f"Item: {self.name}")
        print(f"Description: {self.description}")
        print(f"Usage: {self.usage}")

def heal_player(player, amount):
    player.health += amount
    print(f"You feel rejuvenated! Health increased by {amount}. Current health: {player.health}")

stick = Item(
    name="Stick",
    description="It's useless but it's something.",
    usage="Use to deal 5 damage.",
    value=5
)

sword = Item(
    name="Sword",
    description="A sharp steel sword. Useful for fighting enemies.",
    usage="Use to increase attack damage by 20.",
    value=20
)

big_healing_flask = Item(
    name="Big Healing Flask",
    description="A large flask filled with a glowing red liquid. Restores health when used.",
    usage="Use to restore 50 health points.",
    effect=lambda player: heal_player(player, 50),
    value=50
)

class Map:
    def __init__(self):
        self.rooms = {
            "Starting Room": {
                "description": "You are in a dimly lit room.",
                "exits": {"north": "Treasure Room", "south": "Armory"}
            },
            "Treasure Room": {
                "description": "You see a pile of gold coins.",
                "exits": {"south": "Starting Room"}
            },
            "Armory": {
                "description": "You are in the armory. There are weapons on the wall and two Skeletons guarding the room.",
                "exits": {"north": "Starting Room"},
                "items": [sword],
                "Enemies": ["Skeleton", "Skeleton"]
            }
        }
        self.rooms["Starting Room"]["Enemies"] = ["Goblin"]
        self.rooms["Treasure Room"]["items"] = [big_healing_flask]

    def get_room(self, room_name):
        return self.rooms.get(room_name)


#character naming loop
while 1:
    player_name = input("Enter your player's name: ")
    if player_name.strip():
        break
    print("Player name cannot be empty. Please try again.")
#if player_name not in (placeholder to look through savegame)
#if exist load savegame
#else
player = Player(player_name)

# Initializing game elements
game_map = Map()
enemies = [
    Enemy("Goblin", health=50, attack_power=5),
    Enemy("Ogre", health=100, attack_power=20),
    Enemy("Spider", health=10, attack_power=2)
]
# Place Goblin in Starting Room
enemies[0].location = "Starting Room"
os.system('cls' if os.name == 'nt' else 'clear')

#main loop
while 1:
    if player.health <= 0:
        print(f"{player.name} has been defeated.")
        input("Game Over")
        break
    room = game_map.get_room(player.location)
    available_actions = ["move", "attack", "inventory", "look", "quit"]
    show_collect = False
    action = input(f"What would you like to do? ({', '.join(available_actions)}) ")
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"you are in {player.location}")
    # Find enemies in the current room
    current_enemies = [enemy for enemy in enemies if enemy.location == player.location]

    if current_enemies:
        print("Enemies here:")
        for enemy in current_enemies:
            if enemy.health > 0:
                print(f" - {enemy.name} (HP: {enemy.health})")
            else:
                print(f" - {enemy.name} (HP: 0) (defeated)")
                current_enemies.remove(enemy)

    if action == "move":
        room = game_map.get_room(player.location)
        if room:
            print(f"Available exits: {', '.join(room['exits'].keys())}")
            direction = input("Which direction? ")
            if direction in room["exits"]:
                new_room = room["exits"][direction]
                player.location = new_room
                print(f"You move {direction} to the {new_room}.")
            else:
                print("You can't go that way.")
        else:
            print("You are in an unknown location and cannot move.")

    elif action == "attack":
        target_name = input("Who would you like to attack? ")
        target = next((enemy for enemy in current_enemies if enemy.name == target_name), None)
        if target:
            player.attack(target)
            if target.health > 0:
                target.attack(player)
        else:
            print("Target not found.")

    elif action == "inventory":
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            print(f"Current Health: {player.health}")
            player.show_inventory()
            inv_action = input("Inventory options: use, throw, info, equip, unequip, back > ")
            os.system('cls' if os.name == 'nt' else 'clear')
            if inv_action == "use":
                item_name = input("Enter the name of the item to use: ")
                player.use_item(item_name)
            elif inv_action == "throw":
                if player.inventory:
                    print("Your inventory:")
                    for item in player.inventory:
                        if isinstance(item, Item):
                            print(f" - {item.name}")
                        else:
                            print(f" - {item}")
                    item_name = input("Which item would you like to throw away? ")
                    found_item = None
                    for item in player.inventory:
                        if (isinstance(item, Item) and item.name == item_name) or (item == item_name):
                            found_item = item
                            break
                    if found_item:
                        # Prevent throwing equipped weapon
                        if isinstance(found_item, Item) and player.equipped_weapon == found_item:
                            print("You can't throw away an equipped item. Please unequip it first.")
                        else:
                            print("Do you want to place it in the room or throw it at an enemy?")
                            throw_choice = input("Type 'room' to place in room, 'enemy' to throw at enemy: ").strip().lower()
                            if throw_choice == "room":
                                player.remove_item(found_item)
                                room = game_map.get_room(player.location)
                                if room is not None:
                                    if "items" not in room:
                                        room["items"] = []
                                    room["items"].append(found_item)
                                    print(f"{item_name} has been placed in the room.")
                            elif throw_choice == "enemy":
                                if current_enemies:
                                    print("Enemies here:")
                                    for enemy in current_enemies:
                                        print(f" - {enemy.name} (HP: {enemy.health})")
                                    target_name = input("Which enemy do you want to throw the item at? ")
                                    target = next((enemy for enemy in current_enemies if enemy.name == target_name), None)
                                    if target:
                                        print(f"You throw {item_name} at {target.name}. You lost the item!")
                                        player.remove_item(found_item)
                                        # Apply item effect or weapon damage to enemy
                                        if isinstance(found_item, Item):
                                            if found_item.effect:
                                                # If effect expects player, try enemy
                                                try:
                                                    found_item.effect(target)
                                                except Exception:
                                                    print("Item effect could not be applied to enemy.")
                                            elif found_item.value:
                                                # Treat value as damage
                                                target.health -= found_item.value
                                                print(f"{target.name} takes {found_item.value} damage from the thrown weapon!")
                                                if target.health <= 0:
                                                    print(f"{target.name} has been defeated.")
                                    else:
                                        print("Enemy not found.")
                                else:
                                    print("No enemies to throw the item at.")
                            else:
                                print("Invalid choice. Item not thrown.")
                    else:
                        print("Item not found in inventory.")
                else:
                    print("Your inventory is empty.")
            elif inv_action == "info":
                item_name = input("Enter the name of the item to view info: ")
                found_item = None
                for item in player.inventory:
                    if isinstance(item, Item) and item.name == item_name:
                        found_item = item
                        break
                if found_item:
                    found_item.show_info()
                else:
                    print("Item not found or has no info.")
            elif inv_action == "equip":
                item_name = input("Enter the name of the weapon to equip: ")
                player.equip_weapon(item_name)
            elif inv_action == "unequip":
                player.unequip_weapon()
                print("Weapon unequipped.")
            elif inv_action == "back":
                break
            else:
                print("Invalid inventory option.")

    elif action == "look":
        room = game_map.get_room(player.location)
        if room:
            print(room["description"])
            if "items" in room and room["items"]:
                print("Items in this room:")
                for item in room["items"]:
                    if isinstance(item, Item):
                        print(f" - {item.name}")
                    else:
                        print(f" - {item}")
                show_collect = True
        else:
            print("You see nothing special.")
        # After look, if items are present, offer collect
        if show_collect:
            collect_action = input("Would you like to collect an item? (yes/no): ").strip().lower()
            if collect_action == "yes":
                print("Items available to collect:")
                for item in room["items"]:
                    print(f" - {item.name}" if isinstance(item, Item) else f" - {item}")
                item_name = input("Which item would you like to collect? ")
                found_item = None
                for item in room["items"]:
                    if (isinstance(item, Item) and item.name == item_name) or (item == item_name):
                        found_item = item
                        break
                if found_item:
                    player.add_item(found_item)
                    room["items"].remove(found_item)
                else:
                    print("Item not found.")

    elif action == "collect":
        room = game_map.get_room(player.location)
        if room and "items" in room and room["items"]:
            print("Items available to collect:")
            for item in room["items"]:
                if isinstance(item, Item):
                    print(f" - {item.name}")
            item_name = input("Which item would you like to collect? ")
            found_item = None
            for item in room["items"]:
                if (isinstance(item, Item) and item.name == item_name) or (item == item_name):
                    found_item = item
                    break
            if found_item:
                player.add_item(found_item)
                room["items"].remove(found_item)
            else:
                print("Item not found.")
        else:
            print("There are no items to collect here.")
        if room and "items" in room and room["items"]:
            print("Items available to collect:")
            for item in room["items"]:
                if isinstance(item, Item):
                    item.show_info()
                else:
                    print(f" - {item}")
                item_name = input("Which item would you like to collect? ")
                found_item = None
                for item in room["items"]:
                    if (isinstance(item, Item) and item.name == item_name) or (item == item_name):
                        found_item = item
                        break
                if found_item:
                    player.add_item(found_item)
                    room["items"].remove(found_item)
                else:
                    print("Item not found.")

    elif action == "quit":
        print("See ya next time!")
        break
    else:
        print("Invalid action.")