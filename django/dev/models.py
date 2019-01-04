from django.contrib.auth.models import User, Group
from django import forms

from django.db import models
from django.urls import reverse


#class Game(models.Model):
#    pass
    # Teams: many to many relation to group objects

    # GameData

    # GameRules


class Team(models.Model):
    HUNTER = 0
    HUNTED = 1

    team_name = models.CharField(max_length=80, unique=True)
    team_class = models.IntegerField(default=0, choices=((0, 'Hunter'), (1, 'Hunted')))
    team_score = models.IntegerField(default=0)
    team_location = models.ForeignKey('Location', on_delete=models.CASCADE,
      related_name='teams', null=True)
    team_tag = models.IntegerField()

    def __str__(self):
        return self.team_name


class Player(models.Model):
    player_name = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
      related_name='player')
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
      related_name='players', null=True)

    def __str__(self):
        return self.player_name


class Waypoint(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    score = models.IntegerField()
    activation_time = models.DateTimeField(null=True)

    def __str__(self):
        return '({:0.2f}, {:0.2f}) - '.format(
          self.lat, self.lon) + ' ' + self.activation_time.strftime('%H:%M')


class Location(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
      related_name='locations', null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Team ' + str(self.team) + ', ({:0.2f}, {:0.2f}) - '.format(
          self.lat, self.lon) + ' ' + self.datetime.strftime('%H:%M')


class Message(models.Model):
    sender = models.ForeignKey(Team, on_delete=models.CASCADE,
        related_name='sender')
    recipient = models.ForeignKey(Team, on_delete=models.CASCADE,
        related_name='recipient')
    send_date = models.DateTimeField('date sended', auto_now_add=True)
    subject = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
 
    def get_absolute_url(self):
        return reverse('message-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'MSG: ' + str(self.sender) + ' -> ' + str(self.recipient)


class HuntedTag(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    hunted = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='hunted')
    hunter = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='hunter')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='locations')
    validation_tag = models.IntegerField()

    def __str__(self):
        hunter_name = str(self.hunter)
        hunted_name = str(self.hunted)
        location_str = str(self.location)
        return hunter_name + ', ' + hunted_name + ', ' + location_str