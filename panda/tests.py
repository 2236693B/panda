from django.test import TestCase
from panda.models import Player, PlayerRating, GameStudio, Game, GameRating
from django.contrib.auth.models import User

class RatingMethodTests(TestCase):

    def test_gameRating_method_makes_rating(self):

        player = create_player()
        game=create_game()
        player.make_game_rating(game, 5)

        self.assertIs(GameRating.objects.filter(player=player,rated=game,value=5).exists(), True)

    def test_gameRating_method_updates_rating(self):

        player = create_player()
        game=create_game()

        GameRating(player=player, rated=game, value = 3)

        player.make_game_rating(game, 2)

        self.assertIs(GameRating.objects.filter(player=player,rated=game,value=5).exists(), False, "Other rating remaining")
        self.assertIs(GameRating.objects.filter(player=player, rated=game, value=2).exists(), True, "Rating not updating")

    def test_game_average_rating(self):

        player1,player2 = create_players()

        game = create_game()

        player1.make_game_rating(game,4)
        player2.make_game_rating(game, 3)

        self.assertEqual(game.average_rating(), 3.5)

    def test_playerRating_method_makes_rating(self):

        player1,player2 = create_players()

        player1.make_player_rating(player2, 5)

        self.assertIs(PlayerRating.objects.filter(player=player1,rated_player=player2,value=5).exists(), True)

    def test_playerRating_method_updates_rating(self):
        player1,player2 = create_players()

        PlayerRating(player=player1, rated_player=player2, value = 3)

        player1.make_player_rating(player2, 2)

        self.assertIs(PlayerRating.objects.filter(player=player1,rated_player=player2,value=5).exists(), False, "Other rating remaining")
        self.assertIs(PlayerRating.objects.filter(player=player1, rated_player=player2, value=2).exists(), True, "Rating not updating")

    def test_game_average_rating(self):

        player = create_player()
        player1,player2 = create_players()

        player1.make_player_rating(player,4)
        player2.make_player_rating(player, 3)

        self.assertEqual(player.average_rating(), 3.5)

#Models helper funcitons

def create_player():
    user = User(username = "Test", password = "123456789", email = "test@test.com", first_name = "Te", last_name = "st")
    user.save()
    player = Player(user=user)

    player.save()

    return player

def create_players():
    user = User(username="Test1", password="123456789", email="test1@test.com", first_name="Test", last_name="One")
    user.save()
    player1 = Player(user=user)

    player1.save()

    user = User(username="Test2", password="123456789", email="test2@test.com", first_name="Test", last_name="Two")
    user.save()
    player2 = Player(user=user)

    player2.save()

    return player1,player2

def create_game():
    user = User(username="Studio", password="123456789", email="studio@test.com")
    user.save()
    studio = GameStudio(user=user, name = "Testing")
    studio.save()

    game = Game(studio=studio, name="Test Game")
    game.save()
    return game


#Views tests

#TODO steam API
#     ?
