from django.test import TestCase
from panda.models import Player, PlayerRating, GameStudio, Game, GameRating
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

class GameRatingMethodTests(TestCase):

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

class PlayerRatingMethodTests(TestCase):
    def test_playerRating_method_makes_rating(self):
        player1, player2 = create_players()

        player1.make_player_rating(player2, 5)

        self.assertIs(PlayerRating.objects.filter(player=player1, rated_player=player2, value=5).exists(), True)

    def test_playerRating_method_updates_rating(self):
        player1, player2 = create_players()

        PlayerRating(player=player1, rated_player=player2, value=3)

        player1.make_player_rating(player2, 2)

        self.assertIs(PlayerRating.objects.filter(player=player1, rated_player=player2, value=5).exists(), False,
                      "Other rating remaining")
        self.assertIs(PlayerRating.objects.filter(player=player1, rated_player=player2, value=2).exists(), True,
                      "Rating not updating")

    def test_player_average_rating(self):
        player = create_player()
        player1, player2 = create_players()

        player1.make_player_rating(player, 4)
        player2.make_player_rating(player, 3)

        self.assertEqual(player.average_rating(), 3.5)


#Models helper funcitons

def create_player():
    user = User(username = "Test", password = "123456789", email = "test@test.com", first_name = "Te", last_name = "st")
    user.set_password(user.password)
    user.save()
    player = Player(user=user)

    player.save()

    return player

def create_players():
    user1 = User(username="Test1", password="123456789", email="test1@test.com", first_name="Test", last_name="One")
    user1.set_password(user1.password)
    user1.save()
    player1 = Player(user=user1)

    player1.save()

    user2 = User(username="Test2", password="123456789", email="test2@test.com", first_name="Test", last_name="Two")
    user2.set_password(user2.password)
    user2.save()
    player2 = Player(user=user2)

    player2.save()

    return player1,player2

def create_game():
    user = User(username="Studio", password="123456789", email="studio@test.com")
    user.set_password(user.password)
    user.save()
    studio = GameStudio(user=user, name = "Testing")
    studio.save()

    game = Game(studio=studio, name="Test Game")
    game.save()
    return game


#Views tests
class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):  # If no games or players exist, an appropriate message should be displayed
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no games present.")
        self.assertContains(response, "There are no players present.")
        self.assertQuerysetEqual(response.context ['games'], [])
        self.assertQuerysetEqual(response.context['players'], [])


class SteamAPITests(TestCase):
    def test_game_view_with_no_steam_id(self):  # Check News and World players not present with no steam id
        game = create_game()
        response = self.client.get('/panda/game/' + game.slug + '/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "News")
        self.assertNotContains(response, "World Players")

    def test_game_view_with_steam_id(self):  # Check News and World players present with valid steam api id
        game = create_game()
        game.steam_id = 440
        game.save()
        response = self.client.get('/panda/game/' + game.slug + '/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "News")
        self.assertContains(response, "World Players")
        self.assertNotEqual(response.context['news'], None)
        self.assertNotEqual(response.context['world_players'], None)


    def test_game_view_with_invalid_steam_id(self):  # Check News and World players present with invalid steam api id
        game = create_game()
        game.steam_id = 4
        game.save()
        response = self.client.get('/panda/game/' + game.slug + '/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "News")
        self.assertNotContains(response, "World Players")
        self.assertEqual(response.context['news'], None)
        self.assertEqual(response.context['world_players'], None)

class LoggedInUserViewTests(TestCase):
    def test_loggedIn_user_can_view_players(self):
        player1, player2 = create_players()
        self.client.login(username='Test1', password='123456789')
        response = self.client.get('/panda/player/test2/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, player1.user.username)

    def test_unloggedIn_user_player_view_redirects(self):
        response = self.client.get('/panda/player/test2/')
        self.assertEqual(response.status_code, 302)  #Redirects to login status code

        







