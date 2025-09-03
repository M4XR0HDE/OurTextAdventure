class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.health = 100
        self.location = "Starting Room"

    def show_inventory(self):
        print(f"{self.name}'s Inventory:")
        for item in self.inventory:
            print(f" - {item}")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{item} has been added to {self.name}'s inventory.")

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{item} has been removed from {self.name}'s inventory.")
        else:
            print(f"{item} not found in inventory.")

    def current_location(self):
        print(f"{self.name} is currently at {self.location}.")

    def move(self, direction):
        print(f"{self.name} moves {direction}.")