import datetime
import random

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ScoutsAPP.settings'

import django
django.setup()

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User, Group
from dev.models import (Player, Team, Waypoint, Location, Message,
  HuntedTag)


def cleanup(admin_user='bas'):
    from django.contrib.auth.models import User, Group
    from dev.models import Player, Team, Location

    User.objects.exclude(username=admin_user).delete()
    Group.objects.all().delete()
    Player.objects.all().delete()
    Team.objects.all().delete()
    Location.objects.all().delete()


def create_players(player_list):
    from django.contrib.auth.models import User
    from dev.models import Player

    for player in player_list:
        try:
            user = User.objects.create_user(player['username'],
              player['email'], player['password'])
        except KeyError:
            print('Invalid user definition: {:s}'.format(str(player)))
        except IntegrityError:
            print('User {:s} already exist.'.format(player['username']))
        except Exception as E:
            print(E)

        user = User.objects.get(username=player['username'])
        user.player.create(player_name=player['player_name'], user=user,
          team=None)

def create_team(team_name, player_list, team_class, location):

    try:
        team = Team.objects.get(team_name=team_name)
    except Exception as E:
        print(E)
        team = Team.objects.create(team_name=team_name,
          team_tag=random.randint(0, 9999))

    location = Location.objects.create(team=team, lat=location['lat'],
        lon=location['lon'])

    team.team_class = team_class
    team.team_location = location
    team.save()

    for player in player_list:
        user = User.objects.get(username=player['username'])
        team.players.add(user.player.get())

def create_waypoints(waypoints):
    for waypoint in waypoints:
        Waypoint.objects.create(lat=waypoint['lat'], lon=waypoint['lon'],
            score=waypoint['score']);

def create_messages(message_list):

    for message in message_list:
        try:
            sender = Team.objects.get(team_name=message['sender'])
            recipient = Team.objects.get(team_name=message['recipient'])
            Message.objects.create(sender=sender, recipient=recipient,
              subject=message['subject'], content=message['content'])
        except KeyError:
            print('Invalid message definition: {:s}'.format(str(user)))
        except:
            print('Something went wrong with the creation of a message.')


if __name__ == '__main__':
    # Cleanup:
    from django.contrib.auth.models import User, Group
    from dev.models import (Player, Team, Waypoint, Location, Message,
      HuntedTag)

    User.objects.exclude(username='bas').delete()
    Player.objects.all().delete()
    Team.objects.all().delete()
    Waypoint.objects.all().delete()
    Location.objects.all().delete()
    Message.objects.all().delete()

    # Create players
    players = list()
    for index in range(15):
        players.append({
            'username': 'TestUser{:d}'.format(index),
            'email': 'tu{:d}@test.nl'.format(index),
            'password': 'pwdtu{:d}'.format(index),
            'player_name': 'Player{:d}'.format(index)})

    create_players(players)

    # Create teams and initial locations
    locations = [{'lat': 52.0827881, 'lon': 4.5037963},
                 {'lat': 52.0800380, 'lon': 4.5052163},
                 {'lat': 52.0793850, 'lon': 4.5072543},
                 {'lat': 52.0931340, 'lon': 4.5020333},
                 {'lat': 52.0902860, 'lon': 4.5041803},
                 {'lat': 52.0875230, 'lon': 4.5112683}]

    create_team('Alpha', players[0:3], Team.HUNTER, locations[0])
    create_team('Bravo', players[3:6], Team.HUNTER, locations[1])
    create_team('Charlie', players[6:9], Team.HUNTER, locations[2])
    create_team('X-ray', players[9:11], Team.HUNTED, locations[3])
    create_team('Young', players[11:13], Team.HUNTED, locations[4])
    create_team('Zero', players[13:15], Team.HUNTED, locations[5])

    # Waypoints
    waypoints = [{'lat': 52.0796850, 'lon': 4.5109913, 'score': 50},
                 {'lat': 52.0842080, 'lon': 4.5149823, 'score': 20},
                 {'lat': 52.0886983, 'lon': 4.5076390, 'score': 30},
                 {'lat': 52.0861220, 'lon': 4.5009650, 'score': 40},
                 {'lat': 52.0768400, 'lon': 4.4949703, 'score': 40},
                 {'lat': 52.0780570, 'lon': 4.5018563, 'score': 30}]
    create_waypoints(waypoints)

    team_names = ['Alpha', 'Bravo', 'Charlie', 'X-ray', 'Young', 'Zero']
    messages = list()
    for team_name in team_names:
        messages.append({'sender': 'Alpha',
                         'recipient': team_name,
                         'subject': 'Welcome to hunted!',
                         'content': 'Welcome team {:s}, enjoy the game!'.format(team_name)})
    create_messages(messages)
