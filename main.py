from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Item

print("\n\n")
print("NAME                HP                                MP")
print("                     ---------------------              ---------")
print(bcolors.BOLD + "values:    460/460  |" + bcolors.OKGREEN + " ████████████████     " + bcolors.ENDC + bcolors.BOLD
      + "|    " +
      "65/65  | " + bcolors.OKBlue + "████████" + bcolors.ENDC + "|")

print("                     ---------------------            ---------")
print("values:    460/460  |                     |    65/65  |        |")

print("                     ---------------------            ---------")
print("values:    460/460  |                     |    65/65  |        |")

# Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create Some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 5}, {"item": hipotion, "quantity": 15},
                {"item": superpotion, "quantity": 15}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 5}
    , {"item": grenade, "quantity": 5}]

player = Person(460, 65, 60, 34, player_spells, player_items)
enemy = Person(1200, 65, 45, 25, [], [])

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("================================================")
    player.choose_action()
    choice = input("Choose action:")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You Attacked for", dmg, "points of damage. Enemy HP:", enemy.get_hp())
    elif index == 1:
        player.choose_magic()
        player_magic = int(input("Choose Magic: ")) - 1

        if player_magic == -1:
            continue
        spell = player.magic[player_magic]
        magic_dmg = spell.generate_damage()
        cost = spell.cost
        current_mp = player.get_mp()

        if cost > current_mp:
            print(bcolors.FAIL + "Not Enough MP" + bcolors.ENDC)
            continue

        player.reduce_mp(cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBlue + "\n" + spell.name + "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
        elif spell.type == "black":
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBlue + "\n" + spell.name + "deals ", str(magic_dmg), "points of damage" + bcolors.ENDC)
    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choose Item :")) - 1

        if item_choice == -1:
            continue

        item = player.items[item_choice]["item"]
        if player.items[item_choice]["quantity"] == 0:
            print(bcolors.FAIL + "\n" + "None Left ..." + bcolors.ENDC)
            continue

        player.items[item_choice]["quantity"] -= 1

        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
        elif item.type == "elixer":
            player.hp = player.maxhp
            player.mp = player.maxmp
            print(bcolors.OKGREEN + "\n" + item.name + " fully restores for HP/MP", + bcolors.ENDC)
        elif item.type == "attack":
            enemy.take_damage(item.prop)
            print(bcolors.OKBlue + "\n" + item.name + "deals ", str(item.prop), "points of damage" + bcolors.ENDC)
    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy Attacked for", enemy_dmg)

    print("-------------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC)

    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
    print("Your MP:", bcolors.OKBlue + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You Win !" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You Lost" + bcolors.ENDC)
        running = False
