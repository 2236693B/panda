from django.test import TestCase
from panda.models import Player, PlayerRating, GameStudio, Game, GameRating
from django.contrib.auth.models import User
from django.urls import reverse

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

#Views tests
class IndexViewTests(TestCase):
    def test_index_view_with_no_games(self):  # If no games or players exist, an appropriate message should be displayed
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no games present.")
        self.assertContains(response, "There are no players present.")
        self.assertQuerysetEqual(response.context ['games'], [])
        self.assertQuerysetEqual(response.context['players'], [])

    def test_index_view_with_one_games(self):  # If no games or players exist, an appropriate message should be displayed
        game = create_game()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "There are no games present.")
        self.assertContains(response, "There are no players present.")
        self.assertContains(response, "Test Game")
        self.assertQuerysetEqual(response.context['players'], [])

    def test_index_view_with_two_games(self):  # If no games or players exist, an appropriate message should be displayed
        create_games()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "There are no games present.")
        self.assertContains(response, "There are no players present.")
        self.assertContains(response, "Test Game1")
        self.assertContains(response, "Test Game2")
        self.assertQuerysetEqual(response.context['players'], [])

    def test_index_view_with_more_than_five_games(self):  # If no games or players exist, an appropriate message should be displayed
        create_six_games()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "There are no games present.")
        self.assertContains(response, "There are no players present.")
        self.assertContains(response, "Test Game")
        self.assertContains(response, "Test Game1")
        self.assertContains(response, "Test Game2")
        self.assertContains(response, "Test Game3")
        self.assertContains(response, "Test Game4")
        self.assertNotContains(response, "Test Game5")
        self.assertQuerysetEqual(response.context['players'], [])

    def test_index_view_with_player(self):  # If no games or players exist, an appropriate message should be displayed
        create_player()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no games present.")
        self.assertNotContains(response, "There are no players present.")
        self.assertQuerysetEqual(response.context['games'], [])
        self.assertContains(response, "Test")

    def test_index_view_with_two_players(self):  # If no games or players exist, an appropriate message should be displayed
        create_players()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no games present.")
        self.assertNotContains(response, "There are no players present.")
        self.assertQuerysetEqual(response.context['games'], [])
        self.assertContains(response, "Test1")
        self.assertContains(response, "Test2")

    def test_index_view_with_more_than_six__players(self):  # If no games or players exist, an appropriate message should be displayed
        create_six_players()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no games present.")
        self.assertNotContains(response, "There are no players present.")
        self.assertQuerysetEqual(response.context['games'], [])
        self.assertContains(response, "Test")
        self.assertContains(response, "Test1")
        self.assertContains(response, "Test2")
        self.assertContains(response, "Test3")
        self.assertContains(response, "Test4")
        self.assertNotContains(response, "Test5")

    def test_index_view_with_players_and_games(self):  # If no games or players exist, an appropriate message should be displayed
        create_six_players()
        create_six_games()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "There are no games present.")
        self.assertNotContains(response, "There are no players present.")
        self.assertContains(response, "Test1")
        self.assertNotContains(response, "Test5")
        self.assertContains(response, "Test Game1")
        self.assertNotContains(response, "Test Game5")


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

#Helper functions

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

def create_six_players():
    player = create_player()
    player1,player2 = create_players()

    user3 = User(username="Test3", password="123456789", email="test3@test.com", first_name="Test", last_name="Three")
    user3.set_password(user3.password)
    user3.save()
    player3 = Player(user=user3)

    player3.save()

    user4 = User(username="Test4", password="123456789", email="test4@test.com", first_name="Test", last_name="Four")
    user4.set_password(user4.password)
    user4.save()
    player4 = Player(user=user4)

    player4.save()

    user5 = User(username="Test5", password="123456789", email="test5@test.com", first_name="Test", last_name="Five")
    user5.set_password(user5.password)
    user5.save()
    player5 = Player(user=user5)

    player5.save()

    return player,player1,player2, player3,player4,player5

def create_game():
    user = User(username="Studio", password="123456789", email="studio@test.com")
    user.set_password(user.password)
    user.save()
    studio = GameStudio(user=user, name = "Testing")
    studio.save()

    game = Game(studio=studio, name="Test Game")
    game.save()
    return game

def create_games():
    user1 = User(username="Studio1", password="123456789", email="studio@test.com")
    user1.set_password(user1.password)
    user1.save()
    studio1 = GameStudio(user=user1, name="Testing1")
    studio1.save()

    game1 = Game(studio=studio1, name="Test Game1")
    game1.save()

    user2 = User(username="Studio2", password="123456789", email="studio@test.com")
    user2.set_password(user1.password)
    user2.save()
    studio2 = GameStudio(user=user2, name="Testing2")
    studio2.save()

    game2 = Game(studio=studio2, name="Test Game2")
    game2.save()
    return game1, game2

def create_six_games():
    game = create_game()
    game1,game2 = create_games()
    user3 = User(username="Studio3", password="123456789", email="studio@test.com")
    user3.set_password(user3.password)
    user3.save()
    studio3 = GameStudio(user=user3, name="Testing3")
    studio3.save()

    game3 = Game(studio=studio3, name="Test Game3")
    game3.save()

    user4 = User(username="Studio4", password="123456789", email="studio@test.com")
    user4.set_password(user4.password)
    user4.save()
    studio4 = GameStudio(user=user4, name="Testing4")
    studio4.save()

    game4 = Game(studio=studio4, name="Test Game4")
    game4.save()

    user5 = User(username="Studio5", password="123456789", email="studio@test.com")
    user5.set_password(user5.password)
    user5.save()
    studio5 = GameStudio(user=user5, name="Testing5")
    studio5.save()

    game5 = Game(studio=studio5, name="Test Game5")
    game5.save()

    return game, game1, game2,game3, game4, game5






