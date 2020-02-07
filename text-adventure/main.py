name = input("What is your name: ")
name = name.strip()
if name == "":
    name = "Paul"
print("\nIt's 2053. You are " + name + ", a former US mail carrier. You are currently a prisoner on board an American spacestation for snooping through government secrets that were sent through the mail. As you wake up in your cell from your daily nap, you notice that no one is in the facility. More importantly, every cell door is open! You cautiously walk out.")
print("You should look around to see why everyone is gone and why.")

#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'game.json'
item_file = 'items.json'
inventory = []


# Load the contents of the files into the game and items dictionaries. You can largely ignore this
# Sorry it's messy, I'm trying to account for any potential craziness with the file location
def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        with open(os.path.join(__location__, item_file)) as json_file: items = json.load(json_file)
        return (game,items)
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)


def check_inventory(item):
    for i in inventory:
        if i == item:
            return True
    return False

def render(game,items,current):
    c = game[current]
    print("\nYou are at the " + c["name"])
    print(c["desc"])

    #check for items
    for item in c["items"]:
        if not check_inventory(item["item"]):
            print(item["desc"])

    #display item information
    for i in inventory:
        if i in items:
            if current in items[i]["exits"]:
                print(items[i]["exits"][current])
                inventory.remove(i)


    #print available exits
    print("\nAvailable exits:")
    for e in c["exits"]:
        print(e["exit"].lower())

def get_input():
    response = input("\nWhat do you want to do? ")
    response = response.upper().strip()
    return response

def update(game,items,current,response):
    if response == "INVENTORY":
        print("\nYou are carrying:")
        if len(inventory) == 0:
            print("Nothing")
            return current
        else:
            for i in inventory:
                print(i.lower())
        return current

    c = game[current]
    for e in c["exits"]:
        if response == e["exit"]:
            return e["target"]

    for item in c["items"]:
        if response == "GET " + item["item"] and not check_inventory(item["item"]):
            print()
            print(item["take"])
            inventory.append(item["item"])
            return current
        elif response == "TAKE " + item["item"] and not check_inventory(item["item"]):
            print()
            print(item["take"])
            inventory.append(item["item"])
            return current

    for i in inventory:
        if i in items:
            for action in items[i]["actions"]:
                if response == action + " " + i:
                    print()
                    print(items[i]["actions"][action])
                    return current

    if response[0:3] == "GET":
        print("You can't take that!")
    elif response in ["NORTH","SOUTH","EAST","WEST","NW","NE","SW","SE","UP","DOWN"]:
        print("You can't go that way!")
    else:
        print("I don't understand what you're trying to do.")
            
    return current
    

# The main function for the game
def main():
    current = 'PBLOC'  # The starting location
    end_game = ['SHIP']  # Any of the end-game locations

    (game,items) = load_files()

    while True:
        render(game,items,current)

        for e in end_game:
            if current == e:
                print("You win!")
                break #break out of the while loop

        response = get_input()

        if response == "QUIT" or response == "Q":
            break #break out of the while loop

        current = update(game,items,current,response)

    print("Thanks for playing!")

# run the main function
if __name__ == '__main__':
	main()