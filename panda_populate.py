import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from panda.models import GameStudio, Game, Player, GameRating
from django.contrib.auth.models import User

def populate():

    blizzard_games = [
        "Overwatch",
        "World of Warcraft"
        ]

    EA_games = [
        "Star Wars Battlefront II",
        "Fifa 18",
        "TitanFall 2",
        "BattleField 1"
        ]

    PUBG_games = ["PLAYERUNKNOWN'S BATTLEGROUND"]

    valve_games = [
        "Team Fortress 2",
        "CS:GO"
        ]

    zenimax_games =["Elder Scrolls Online"]

    studios = {
        "Blizzard":{"games": blizzard_games},
        "EA games":{"games": EA_games},
        "PUBG Corporaton":{"games": PUBG_games},
        "Valve":{"games": valve_games},
        "Zenimax":{"games": zenimax_games}
        }

    users = [
        {"username":"BegsOnToast", "password":"Pa55word", "email":"Begs@Toast.com", "First":"Conor", "Last":"Begley"},
        {"username":"MattyBoi", "password":"WhosYourDa?", "email":"Mathew@greggs.co.uk", "First":"Mathew", "Last":"McBride"},
        {"username":"CrispyDarkMagic", "password":"ILoveAJAX", "email":"adam@sinnfein.ie", "First":"Adam", "Last":"Christie"},
        {"username":"Musket_Mosez", "password":"N@than", "email":"mo@momo.com", "First":"Mo", "Last":"Moses"}
        ]

    players = {
        "BegsOnToast": {"ratings":{"Star Wars Battlefront II": 4, "Elder Scrolls Online":3, "CS:GO":1}},
        "MattyBoi" : {"ratings":{"Star Wars Battlefront II": 3, "Elder Scrolls Online":4}},
        "CrispyDarkMagic": {"ratings":{"Elder Scrolls Online":3, "Team Fortress 2":5}},
        "Musket_Mosez":{"ratings":{"Fifa 18":3, "PLAYERUNKNOWN'S BATTLEGROUND":4}}
        }


    #Create studio and games owned by that studio
    for studio, studio_data in studios.items():
        s = add_studio(studio)

        for game in studio_data["games"]:
            add_game(s,game)

    #Create users and create player from user
    for user in users:
        u = add_user(user["username"], user["email"], user["password"],user["First"],user["Last"])
        create_player(u)

    #Make Ratings
    for player, player_data in players.items():
        p = Player.objects.get(user=User.objects.get(username=player))
        for game,rating in player_data["ratings"].items():
            g = Game.objects.get(name=game)
            p.make_game_rating(g,rating)

    #Pretty print games
    print("\n Games:")
    for s in GameStudio.objects.all():
        for g in Game.objects.filter(studio=s):
            print("- {0} - {1} : {2}".format(str(s), str(g), (g.average_rating())))

    #Pretty print players
    print("\n Players:")
    for p in Player.objects.all():
        print(str(p))

def add_studio(name):
    s = GameStudio.objects.get_or_create(name=name)[0]
    return s

def add_game(studio,name):
    g = Game.objects.get_or_create(studio=studio, name=name)[0]
    #g.save()
    return g

def add_user(username, email, password, first, last):
    u = User.objects.get_or_create(username=username, password=password, email=email)[0]
    u.first_name=first
    u.last_name=last
    u.save()
    return u

def create_player(user):
     p = Player.objects.get_or_create(user=user)
     return p


if __name__ == '__main__':
    print("Starting Panda population script...")
    populate()

