import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from panda.models import GameStudio, Game, Player, Comment
from django.contrib.auth.models import User
import datetime

def populate():

    blizzard_games = {
        'Overwatch':
            { 'catergory':'FPS', 'URL':'https://playoverwatch.com/en-gb/', 'date':datetime.datetime.strptime('24-05-2016', '%d-%m-%Y'), 'picture':'game_images/overwatch.jpg',
        'PC':True, 'Playstation':True,'Xbox':True,'Nintendo':False, 'Mobile':False, 'id':None,
        'extract':'''In a time of global crisis, an international task force of heroes banded together to restore peace to a war-torn world: OVERWATCH.
        Overwatch ended the crisis, and helped maintain peace in the decades that followed, inspiring an era of exploration, innovation, and discovery.
        But, after many years, Overwatch’s influence waned, and it was eventually disbanded.
        Now, conflict is rising across the world again, and the call has gone out to heroes old and new. Are you with us?''',
        'recommend': ['Team Fortress 2', 'CS:GO'], },

        'World of Warcraft':
            {'catergory':'MMO', 'URL':'https://worldofwarcraft.com/en-gb/', 'date':datetime.datetime.strptime('23-11-2004', '%d-%m-%Y'), 'picture':'game_images/wow.jpg',
        'PC':True, 'Playstation':False,'Xbox':False,'Nintendo':False, 'Mobile':False, 'id':None,
        'extract':'''Explore the world of Azeroth, a place of never-ending adventure and action. Experience epic stories and quests. Face deadly dragons, find mythical artifacts,
        or just visit a nice, quiet corner of the world to do some fishing.Pledge allegiance to one of two warring factions, the Alliance or the Horde. Join or create a hand-picked group
        or guild of adventurers like yourself, and take on Azeroth's foes as one of twelve unique classes and thirteen races. Level up and amass power at your own pace.''',
         'recommend': ['Elder Scrolls Online'], },
        }

    EA_games = {
        "Star Wars Battlefront II":
            {'catergory':'FPS', 'URL':'https://www.ea.com/en-gb/games/starwars/battlefront/battlefront-2', 'date':datetime.datetime.strptime('17-11-2017', '%d-%m-%Y'), 'picture':'game_images/battlefront.png',
        'PC':True, 'Playstation':True,'Xbox':True,'Nintendo':False, 'Mobile':False, 'id':None,
        'extract':'''Heroes are born on the battlefront, and in Star Wars Battlefront 2, you're able to experience it for yourself. Play as heroes from all three eras of Star Wars in massive battles across iconic locations,
        and take part in a thrilling single-player story as Iden Versio fights to avenge the Emperor.''',
        'recommend': ['Battlefield 1', 'Titanfall 2'], },

        "Fifa 18":
            {'catergory':'SPO', 'URL':'https://www.easports.com/fifa', 'date':datetime.datetime.strptime('29-09-2017', '%d-%m-%Y'), 'picture': 'game_images/fifa.jpg',
        'PC':True, 'Playstation':True,'Xbox':True,'Nintendo':True, 'Mobile':True, 'id':None,
        'extract':'''Powered by Frostbite, FIFA 18 blurs the line between the virtual and real worlds, bringing to life the players, teams and atmospheres of The World’s Game. Move with Real Player Motion Technology - an all-new
        animation system that creates a new level of responsiveness and player personality - to unlock dramatic moments in the world’s most immersive atmospheres. Then go on a global journey as Alex Hunter along with a star-
        studded cast of characters, including Cristiano Ronaldo and other European football stars. ''',
        'recommend': [], },

        "Titanfall 2":
            {'catergory':'FPS', 'URL':'https://www.ea.com/en-gb/games/titanfall/titanfall-2', 'date':datetime.datetime.strptime('28-10-2016', '%d-%m-%Y'), 'picture':'game_images/titanfall.png',
        'PC':True, 'Playstation':True,'Xbox':True,'Nintendo':False, 'Mobile':False, 'id':None,
        'extract':'''Call down your Titan and get ready for an exhilarating first-person shooter experience in Titanfall™ 2! The sequel introduces a new single player campaign that explores the bond between Pilot and Titan.
        Or blast your way through an even more innovative and intense multiplayer experience - featuring 6 new Titans, deadly new Pilot abilities, expanded customization, new maps, modes, and much more. ''',
        'recommend': ['Battlefield 1', 'Star Wars Battlefront II'],},

        "Battlefield 1":
            { 'catergory':'FPS', 'URL':'https://www.battlefield.com/en-gb', 'date':datetime.datetime.strptime('21-10-2016', '%d-%m-%Y'), 'picture':'game_images/battlefield.jpg',
        'PC':True, 'Playstation':True,'Xbox':True,'Nintendo':False, 'Mobile':False, 'id':None,
        'extract':'''Discover a world at war through an adventure-filled campaign, or join in epic team-based multiplayer battles with up to 64 players. Fight as infantry or take control of amazing vehicles on land,
        air and sea.''', 'recommend' : ['Titanfall 2', 'Star Wars Battlefront II'],}


        }

    PUBG_games = {
        "PLAYERUNKNOWN'S BATTLEGROUNDS" :
            {'catergory':'FPS', 'URL':'https://www.playbattlegrounds.com/main.pu', 'date':datetime.datetime.strptime('21-12-2017', '%d-%m-%Y'), 'picture':'game_images/pubg.jpg',
        'PC':True, 'Playstation':False,'Xbox':True,'Nintendo':False, 'Mobile':False, 'id': 578080,
        'extract':'''Our BATTLE ROYALE game-mode will put up to 100 players on a remote island
        for a winner-takes-allshowdown where strategic gameplay is as important as shooting skills.
        Players will enter a last-man-standing battle where they try to locate weapons, vehicles and supplies in a graphically and tactically rich battleground
        that eventually forces players into a shrinking play zone as they engage in a tense and spectacular fight to the death.''', 'recommend' : ['Overwatch'],}
        }

    valve_games = {
        "Team Fortress 2":
            { 'catergory':'FPS', 'URL':'http://www.teamfortress.com/', 'date':datetime.datetime.strptime('10-10-2007', '%d-%m-%Y'), 'picture': 'game_images/teamfortress.jpg',
        'PC':True, 'Playstation':False,'Xbox':False,'Nintendo':False, 'Mobile':False, 'id':440,
        'extract':'''The most highly-rated free game of all time! One of the most popular online action games of all time, Team Fortress 2 delivers constant free updates—new game modes, maps, equipment and, most importantly,
        hats.Nine distinct classes provide a broad range of tactical abilities and personalities, and lend themselves to a variety of player skills.''',
        'recommend': ['Overwatch', 'CS:GO'], },

        "CS:GO":
            {'catergory':'FPS', 'URL':'http://blog.counter-strike.net/', 'date':datetime.datetime.strptime('21-08-2012', '%d-%m-%Y'), 'picture':'game_images/csgo.jpg',
        'PC':True, 'Playstation':False,'Xbox':False,'Nintendo':False, 'Mobile':False, 'id': 730,
        'extract':'''Counter-Strike: Global Offensive (CS: GO) will expand upon the team-based action gameplay that it pioneered when it was launched 14 years ago.CS: GO features new maps, characters, and weapons and delivers
        updated versions of the classic CS content (de_dust2, etc.). In addition, CS: GO will introduce new gameplay modes, matchmaking, leader boards, and more.''',
        'recommend': ['Overwatch', 'Team Fortress 2'], }
        }

    zenimax_games ={
        "Elder Scrolls Online":
            { 'catergory':'ROL', 'URL':'https://www.elderscrollsonline.com/en-gb/', 'date':datetime.datetime.strptime('4-04-2014', '%d-%m-%Y'), 'picture':'game_images/eso.jpg',
        'PC':True, 'Playstation':False,'Xbox':False,'Nintendo':False, 'Mobile':False, 'id': 306130,
        'extract':'''The award-winning fantasy role-playing series, The Elder Scrolls goes online – no game subscription required. Experience this multiplayer role-playing game on your own or together with your friends,
        guild mates, and thousands of alliance members. Explore dangerous caves and dungeons in Skyrim, or craft quality goods to sell in the city of Daggerfall. Embark upon adventurous quests across Tamriel and engage in
        massive player versus player battles, or spend your days at the nearest fishing hole or reading one of many books of lore. The choices are yours in the persistent world of The Elder Scrolls Online: Tamriel Unlimited.''',
        'recommend': ['World of Warcraft'], }
        }

    mojang_games ={
        'Minecraft':
            { 'catergory':'ADV', 'URL':'https://minecraft.net/en-us/', 'date':datetime.datetime.strptime('17-04-2009', '%d-%m-%Y'), 'picture':'game_images/minecraft.jpg',
        'PC':True, 'Playstation':True,'Xbox':True,'Nintendo':True, 'Mobile':True, 'id':None,
        'extract':'''Endless exploration. Create and explore your very own world where the only limit is what you can imagine.Build almost anything. Crafting has never been faster, easier or more fun. More fun with friends
        Play with up to four players in split screen for free, or invite hundreds of friends to a massive gameplay server or your own private Realm!''',
        'recommend' : [],}
        }
    epic_games = {
        'Fortnite Battle Royal':
            {'catergory': 'ADV', 'URL': 'https://www.epicgames.com/fortnite/',
             'date': datetime.datetime.strptime('25-07-2017', '%d-%m-%Y'), 'picture': 'game_images/fortnite.jpg',
             'PC': True, 'Playstation': True, 'Xbox': True, 'Nintendo': False, 'Mobile': True, 'id': None,
             'extract': '''As a battle royale game, Fortnite Battle Royale features up to 100 players, alone or in small squads, attempting to be the last player alive by killing other players or evading them, while staying within a 
             constantly shrinking safe zone to prevent taking lethal damage from being outside it. Players must scavenge for weapons and armor to gain the upper hand on their opponents. The game adds the construction element 
             from Fortnite; players can break down most objects in the game world to gain resources they can use to build fortifications as part of their strategy. ''',
             'recommend': [],},}

    riot_games = {
        'League of Legends':
            {'catergory': 'MOB', 'URL': 'https://euw.leagueoflegends.com/en/',
             'date': datetime.datetime.strptime('27-10-2009', '%d-%m-%Y'), 'picture': 'game_images/league.jpg',
             'PC': True, 'Playstation': False, 'Xbox': False, 'Nintendo': False, 'Mobile': False, 'id': None,
             'extract': '''n League of Legends, players assume the role of an unseen "summoner" that controls a "champion" with unique abilities and battle against a team of other players or computer-controlled champions. The 
             goal is usually to destroy the opposing team's "nexus", a structure which lies at the heart of a base protected by defensive structures, although other distinct game modes exist as well. Each League of Legends 
             match is discrete, with all champions starting off fairly weak but increasing in strength by accumulating items and experience over the course of the game.The champions and setting blend a variety of elements, 
             including high fantasy, steampunk, and Lovecraftian horror.''',
             'recommend': [],},}

    studios = {
        "Blizzard":{"username":"bli55ard", "password":"snow", "email":"info@Blizzard.com","games": blizzard_games, 'picture': 'studio_images/Blizzard.png' , 'twitter': 'Blizzard_Ent' ,
                    'bio':'''Blizzard Entertainment® is a premier developer and publisher of entertainment software. After establishing the Blizzard Entertainment label in 1994, the company 
                    quickly became one of the most popular and well-respected makers of computer games. By focusing on creating well-designed, highly enjoyable entertainment experiences, Blizzard
                     Entertainment has maintained an unparalleled reputation for quality since its inception.'''},

        "EA games":{"username":"EA", "password":"WeLoveDLC", "email":"info@EA.com","games": EA_games,'picture':'studio_images/ea.jpg', 'twitter': 'EA' ,
                    'bio': '''Electronic Arts Inc. is a leading global interactive entertainment software company. EA delivers games, content and online services for Internet-connected consoles, 
                    personal computers, mobile phones and tablets.'''},

        "PUBG Corporaton":{"username":"PUBG", "password":"BattleRoyale", "email":"info@PUBG.com","games": PUBG_games, 'picture': 'studio_images/PUBG.jpg', 'twitter':'PUBATTLEGROUNDS',
                           'bio':'''This is BATTLE ROYALE. Our game-mode will put up to 100 players on a remote island for a winner-takes-allshowdown where strategic gameplay is as important 
                           as shooting skills. Players will enter a last-man-standing battle where they try to locate weapons, vehicles and supplies in a graphically and tactically rich 
                           battlegroundthat eventually forces players into a shrinking play zone as they engage in a tense and spectacular fight to the death.'''},

        "Valve":{"username":"V@lv3", "password":"Money$$$", "email":"info@don'tcare.com","games": valve_games, 'picture': 'studio_images/valve.png' , 'twitter':'steam_games' ,
                 'bio': '''When you give smart talented people the freedom to create without fear of failure, amazing things happen. We see it every day at Valve. In fact, some of our best 
                 insights have come from our biggest mistakes. And we’re ok with that! Since 1996, this approach has produced award-winning games, leading-edge technologies, and a groundbreaking
                  social entertainment platform. We’re always looking for creative risk-takers who can keep that streak alive.'''},

        "Zenimax":{"username":"Zen1m@x", "password":"ESO", "email":"info@Bethesdaripoff.com","games": zenimax_games, 'picture': 'studio_images/zenimax.png' , 'twitter':None,
                   'bio':'''ZeniMax creates and publishes original interactive entertainment content for consoles, the PC, and handheld/wireless devices. Its Bethesda Softworks division, founded in 1986 in the early days of the industry, has a long history of success as a publisher of award-winning video games. In addition, the ZeniMax group includes some of the most acclaimed development studios in the world. The 
                   Company's growing library of intellectual properties includes such major franchises as The Elder Scrolls®, Fallout®, Dishonored®, DOOM®, QUAKE®, Wolfenstein®, Prey®, The Evil Within®, and 
                   RAGE®.'''},

        "Mojang":{"username":"m0j@ng", "password":"micrcosoft$$", "email":"money@microsoft.com","games": mojang_games , 'picture': 'studio_images/mojang.png' ,'twitter':'Mojang',
                  'bio':'''Mojang AB is a games studio based in Stockholm, Sweden. We were founded in 2009 by Markus “Notch” Persson. He’s also the creator of our best-selling game to date: 
                  Minecraft. Since then, we’ve released our second game, the card-collecting tactical battler Scrolls, and have dabbled in publishing with Oxeye Game Studio’s awesome side-
                  scrolling robo-blaster Cobalt. We’re developing more games, too, but we’re not ready to talk about those quite yet.'''},

        "Epic Games": {"username": "epic", "password": "ItsInTheName", "email": "epic@games.com",
                   "games": epic_games, 'picture': 'studio_images/epic_games.png', 'twitter': 'EpicGames',
                   'bio': '''Epic Games, Inc. (formerly Potomac Computer Systems and later Epic MegaGames, Inc.) is an American video game and software development corporation based in Cary, North Carolina. 
                    Epic Games develops Unreal Engine, a commercially available game engine which also powers their internally developed video games, such as the Unreal, Gears of War and Infinity Blade series. In 2014, Unreal Engine was named
                    the "most successful videogame engine" by Guinness World Records.'''},

        "Riot Games": {"username": "LoL", "password": "DotaIsStupid", "email": "info@league.com",
                   "games": riot_games, 'picture': 'studio_images/riot.jpg', 'twitter': 'riotgames',
                   'bio': '''Riot Games is an American video game developer, publisher, and eSports tournament organizer established in 2006. Their main office is based in West Los Angeles, California. They currently have 
                   additional game development studios and offices located in Berlin, Dublin, Hong Kong, Istanbul, Mexico City, Moscow, New York City, St. Louis, Santiago, São Paulo, Seoul, Shanghai, Singapore, Sydney, Taipei, 
                   and Tokyo. The company is primarily known for League of Legends, which was released in North America and Europe on October 27, 2009. The company developed a free mobile game called Blitzcrank's Poro Roundup, 
                   which was released on iOS, and Android in August 2015. Riot is also involved in League of Legends' competitive eSports scene by organizing the League of Legends World Championship and Championship Series for 
                   Europe and North America, as well as coordinating the filming and broadcasting of those events. They also sanction leagues organized by third parties in other regions across the world.'''},
        }

    players = {
        'BegsOnToast':
            {'username':'BegsOnToast', 'password':'Pa55word', 'email':'Begs@Toast.com', 'First':'Conor', 'Last':'Begley', 'picture':'profile_images/toast.jpg',
            'Bio':
                '''Second Electronic and Software Engineering Student looking for some casual gamers for either PC(I\'ve an ok spec laptop) or Playstation''',
            'Steam':'BegsOnToast', 'PSN':'Begs_On_Toast','Xbox':'BegsOnToast', 'Nintendo':None,
            'game_ratings':{'Star Wars Battlefront II': 4, 'Elder Scrolls Online':3, 'CS:GO':0},
            'game_comments':{'Star Wars Battlefront II': 'Stellar game', 'Elder Scrolls Online':'Top quailty Skyrim remake', 'CS:GO':'Terrible game and terrible graphics'},
            'player_ratings' : {'MattyBoi':3 , 'CrispyDarkMagic':4 , 'Musket_Mosez':3},
            'plays_casual': ['Star Wars Battlefront II', 'CS:GO', 'Minecraft'],
            'plays_comp' : ['Elder Scrolls Online'],
            'approved': True,
            },

        'MattyBoi' :
            {'username':'MattyBoi', 'password':'WhosYourDa?', 'email':'Mathew@greggs.co.uk', 'First':'Mathew', 'Last':'McBride', 'picture':'profile_images/greggs.jpg',
            'Bio':
                '''Two Words : I f*cking love Gregggggggggggggggs''',
            'Steam':'Pedro', 'PSN':None,'Xbox':None, 'Nintendo':None,
            'game_ratings':{'Star Wars Battlefront II': 3, 'Elder Scrolls Online':4},
            'game_comments':{'Star Wars Battlefront II': 'Ooof. Great game', 'Elder Scrolls Online':'Great laugh lad'},
            'player_ratings' : {'BegsOnToast':5 , 'CrispyDarkMagic':1 , 'Musket_Mosez':3},
            'plays_casual': ['Star Wars Battlefront II','Elder Scrolls Online', 'World of Warcraft'],
            'plays_comp':  ['Minecraft'],
            'approved': True,
            },

        'CrispyDarkMagic':
            {'username':'CrispyDarkMagic', 'password':'ILoveAJAX', 'email':'adam@sinnfein.ie', 'First':'Adam', 'Last':'Christie', 'picture':'profile_images/krispies.jpg',
            'Bio':
                '''Hearty Irish Lad looking for some likeminded players. Top of the morning to ya''',
            'Steam':'Chrispie', 'PSN':None, 'Xbox':None, 'Nintendo':None,
            'game_ratings':{'Elder Scrolls Online':3, 'Team Fortress 2':5},
            'game_comments': {'Elder Scrolls Online':'Not a patch on Skyrim', 'Team Fortress 2':'First'},
            'player_ratings' : {'BegsOnToast':5 , 'MattyBoi':0 , 'Musket_Mosez':2},
            'plays_casual': ['Elder Scrolls Online', 'CS:GO', 'Minecraft'],
            'plays_comp' : ['Team Fortress 2','World of Warcraft'],
            'approved' : True,
            },

        'Musket_Mosez':
            {'username':'Musket_Mosez', 'password':'N@than', 'email':'mo@momo.com', 'First':'Mo', 'Last':'Moses', 'picture':'profile_images/musket.png',
            'Bio':
                '''Pro-gamer yo!''',
            'Steam':None, 'PSN':None,'Xbox':None, 'Nintendo':None,
            'game_ratings':{'Fifa 18':3, 'PLAYERUNKNOWN\'S BATTLEGROUNDS':4},
            'game_comments':{'Fifa 18':'Gotta love a bit of footie', 'PLAYERUNKNOWN\'S BATTLEGROUNDS':'Tough game but worth the challenge'},
            'player_ratings' : {'BegsOnToast':5 , 'MattyBoi':2 , 'CrispyDarkMagic':2, 'PhoniX':4 },
            'plays_casual': ['Minecraft'],
            'plays_comp': ['PLAYERUNKNOWN\'S BATTLEGROUNDS', 'Fifa 18', 'Minecraft'],
            'approved': True,
            },

        'T0bbl3r':
            {'username':'T0bbl3r', 'password':'C00lDub3', 'email':'tobz@hotmail.com', 'First':'Toby', 'Last':'Jones','picture':'profile_images/toby.png',
            'Bio':
                '''Add me if you got a KD greater than 0.8KD boiiiii. Only play console and not PC crap!!!''',
            'Steam':None, 'PSN':'T0bbl3r','Xbox':'T0bzz', 'Nintendo':'TobMan',
            'game_ratings':{'Fifa 18':4, 'PLAYERUNKNOWN\'S BATTLEGROUNDS':4,'Star Wars Battlefront II': 5,'Overwatch':4},
            'game_comments':{'Fifa 18':'Great edition to the Fifa series. Ultimate team for the win!', 'PLAYERUNKNOWN\'S BATTLEGROUNDS':'Great fun. Real life huner games','Star Wars Battlefront II': 'Pew pew!','Overwatch':'Genre defining FPS'},
            'player_ratings' : {'BegsOnToast':5 , 'Amiek88':4 },
            'plays_casual': ['Star Wars Battlefront II','PLAYERUNKNOWN\'S BATTLEGROUNDS', 'Minecraft'],
            'plays_comp': ['Overwatch', 'Fifa 18'],
            'approved': False,
            },

        'PhoniX':
            {'username':'PhoniX', 'password':'dhhwhw67576@;6%b', 'email':'danylo@danylo.com', 'First':'Danylo', 'Last':'Kravets', 'picture':'profile_images/phonix.png',
            'Bio':
                '''Hard core gamers only. PC MAster Race. Looking to get in MLG. Need Team''',
            'Steam':'PhoniX', 'PSN':None,'Xbox':None, 'Nintendo':None,
            'game_ratings':{'CS:GO':5, 'PLAYERUNKNOWN\'S BATTLEGROUNDS':4},
            'game_comments': {'CS:GO':'Only real gamers play this. Reuires Skill and Intelligence', 'PLAYERUNKNOWN\'S BATTLEGROUNDS':'Up and comming game, shows potenial'},
            'player_ratings' : {'Musket_Mosez':4 },
            'plays_casual': ['Minecraft'],
            'plays_comp': ['CS:GO', 'PLAYERUNKNOWN\'S BATTLEGROUNDS'],
            'approved': False,
            },

        'Amiek88':
            {'username':'Amiek88', 'password':'Hello1234', 'email':'amiex@gmail.com', 'First':'Amie', 'Last':'King', 'picture':'profile_images/amy.png',
            'Bio':
                '''New here. Absolutely love minecraft!''',
            'Steam':'Amiek88', 'PSN':None,'Xbox':None, 'Nintendo':'Amiexoxo',
            'game_ratings':{'Minecraft':5},
            'game_comments': {'Minecraft':'Such a fun game. Everyone should play it'},
            'player_ratings' : {'T0bbl3r':3 },
            'plays_casual': [ 'Minecraft'],
            'plays_comp'  : [],
            'approved': False,
            },
        }


    #Create admin users
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@test.com', 'ProjectPanda123')

    #Create users for studio, studio and games owned by that studio

    for studio, studio_data in studios.items():
        u = add_studio_user(studio_data["username"], studio_data["password"], studio_data["email"])
        s = add_studio(studio, studio_data, u)

        for game, game_data in studio_data["games"].items():
            add_game(s,game, game_data)

    #Create users and create player from user
    for player, player_data in players.items():
        u = add_player_user(player_data["username"], player_data["email"], player_data["password"],player_data["First"],player_data["Last"])
        add_player(u, player_data)

    #Make Ratings
    for player, player_data in players.items():
        p = Player.objects.get(user=User.objects.get(username=player))

        for game,rating in player_data["game_ratings"].items():
            g = Game.objects.get(name=game)
            p.make_game_rating(g,rating)

        for pla,rating in player_data["player_ratings"].items():
            rated_p= Player.objects.get(user = User.objects.get(username=pla))
            p.make_player_rating(rated_p,rating)

    #Make Comments
    for player, player_data in players.items():
        p = Player.objects.get(user=User.objects.get(username=player))

        for game,comment in player_data["game_comments"].items():
            make_comment(p, game, comment)

    #Pretty print games
    print("\n Games:")
    for s in GameStudio.objects.all():
        for g in Game.objects.filter(studio=s):
            print("- {0} - {1} : {2}".format(str(s), str(g), (str(g.rating))))

    #Pretty print players
    print("\n Players:")
    for p in Player.objects.all():
        print("{0} : {1}".format(str(p),str(p.rating)))

def add_studio_user(username, password, email):
    u = User.objects.get_or_create(username=username, email=email)[0]
    u.set_password(password) #Hashes password
    u.save()
    return u

def add_studio(name, data, u):
    s = GameStudio.objects.get_or_create(name=name, user = u)[0]
    s.bio = data['bio']
    s.TwitterHandle = data['twitter']
    s.picture = data['picture']
    s.save()
    return s

def add_game(studio,name,game_data):
    g = Game.objects.get_or_create(studio=studio, name=name)[0]
    g.extract = game_data["extract"]
    g.picture = game_data["picture"]
    g.site = game_data["URL"]
    g.date = game_data["date"]
    g.catergory = game_data["catergory"]
    g.Playstation = game_data["Playstation"]
    g.Xbox = game_data["Xbox"]
    g.PC = game_data["PC"]
    g.Nintendo = game_data["Nintendo"]
    g.Mobile = game_data["Mobile"]
    g.steam_id = game_data['id']

    for game in game_data['recommend']:
        g.recommend.add(Game.objects.get(name=game))
    g.save()
    return g

def add_player_user(username, email, password, first, last):
    u = User.objects.get_or_create(username=username, email=email)[0]
    u.set_password(password) #Hashes password
    u.first_name=first
    u.last_name=last
    u.save()
    return u

def add_player(user, player_data):
     p = Player.objects.get_or_create(user=user)[0]
     p.Bio = player_data['Bio']
     p.Steam = player_data['Steam']
     p.PSN = player_data['PSN']
     p.Xbox = player_data['Xbox']
     p.Nintendo = player_data['Nintendo']
     p.picture = player_data['picture']
     p.approved = player_data['approved']
     p.save()

     for game in player_data["plays_casual"]:
         g = Game.objects.get(name = game)
         g.players.add(p)

     for game in player_data["plays_comp"]:
         g = Game.objects.get(name = game)
         g.comp_players.add(p)

     return p

def make_comment (player, game, comment):
    c = Comment.objects.get_or_create(player = player, comment = comment)[0]
    g = Game.objects.get(name=game)
    g.comments.add(c)


if __name__ == '__main__':
    print("Starting Panda population script...")
    populate()

