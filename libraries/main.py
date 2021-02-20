#Discord and Dungeons test environment!

from libraries.player_handling import Player
from libraries.enemy_handling import Enemy
from libraries.character_creation_handling import CreateCharacter
from libraries.story_handling import Story
from libraries import map_rendering, main_functions
import sys

#NOT USED AND BROKEN ANYMORE

INACCESSABLE = [(1,0),(5,0),(6,0),(1,1),(3,1),(6,1),(1,3),(4,3),(5,3),(0,4),(3,4),(4,4),(5,4),(1,6),(4,6)]
SPECIAL = [(0,0),(0,6),(6,6)]

#Not used anymore

print('Welcome to Discord and Dungeons test environment!')
print('Enjoy the experience :)\n\n')

while True:
    try:
        user_ID = int(input('Please enter your ID: '))
    except ValueError:
        print('\nA user ID must be a number! Try again.')
    else:
        break

player_object = Player(user_ID)
if not player_object.check_if_exists():
    print('\nYou don\'t have a user file existing!')
    print('Available options: ')
    print('1.Create Character')
    print('2.Exit')
    choice = input('\nWhat is your choice? ')
    while choice not in ('1', '2'):
        print('\nInvalid choice try again!')
        choice = input('What is your choice? ')
    if choice == '2':
        sys.exit()
    elif choice == '1':
        character = CreateCharacter(user_ID)
        character.create_character()
        del character
        print('Character created!')
        print('Checking again.')
        if not player_object.check_if_exists():
            print('\nYou don\'t have a user file existing!')
            print('\nExiting due error. Contact the developer :)')
            sys.exit()

if player_object.check_if_exists():
    print('''
    \nYou have a user file existing!
    Available options: 
    1.Fight random monster
    2.Show map and who is in the same area
    3.Show stats & inventory
    4.Get money
    5.Merchant
    6.Move
    7.Add XP and check for level-up.
    8.Heal Up
    9.Story
    10.Exit
    ''')

while True:
    choice = input('\nWhat is your choice? ')
    if choice not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
        print('\nInvalid choice.')
        continue
    if choice == '1':
        enemy_object = Enemy(user_ID)
        enemy_object.create_enemy()
        main_functions.fight(player_object, enemy_object)
    elif choice == '2':
        x, y = player_object.get_coords()
        map_rendering.show_map(7, 7, INACCESSABLE, SPECIAL, (x, y))
        main_functions.get_players_in_location(x, y, user_ID)
    elif choice == '3':
        print('\nYour stats:')
        player_stats = player_object.get_stats()
        main_functions.display_stats(*player_stats, player_object.get_level())

        print('\nYour inventory:')
        inventory = player_object.get_inventory()
        main_functions.display_inventory(*inventory)
    elif choice == '4':
        while True:
            try:
                amount = int(input('How much to add? '))
            except ValueError:
                print('Must be a number!\n')
            else:
                break
        player_object.modify_money(amount)
    elif choice == '5':
        main_functions.merchant(0, user_ID)
    elif choice == '6':
        new_x = int(input('What is the x coordinate? '))
        new_y = int(input('What is the y coordinate? '))
        player_object.move(new_x, new_y)
    elif choice == '7':
        xp = int(input('How much XP to add? '))
        player_object.add_xp(xp)
    elif choice == '8':
        player_object.add_health(10)
    elif choice == '9':
        player_story = Story(user_ID)
    elif choice == '10':
        break





