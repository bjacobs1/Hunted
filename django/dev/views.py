from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django import forms

import json

from .forms import MessageCreateForm
from .models import Message, Player, Team, Waypoint, Location


class MessageListView(LoginRequiredMixin, ListView):
    login_url = '/dev/login'
    model = Message

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Message.objects.all().order_by('-send_date')
        elif user.is_authenticated:
            team = Player.objects.get(user=user).team
            message_query = Message.objects.filter(recipient=team)
            return message_query.order_by('-send_date')
        else:
            return None


class MessageDetailView(LoginRequiredMixin, DetailView):
    login_url = '/dev/login'
    model = Message

    def get_queryset(self):
        queryset = super(MessageDetailView, self).get_queryset()

        user = self.request.user
        if user.is_superuser:
            return queryset
        elif user.is_authenticated:
            team = Player.objects.get(user=user).team
            return queryset.filter(recipient=team)
        else:
            return Message.objects.none()


class MessageCreateView(LoginRequiredMixin, CreateView):
    login_url = '/dev/login'
    model = Message
    form_class = MessageCreateForm
    success_url = '/dev/message/all'

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        player = Player.objects.get(user=user)
        form.instance.sender_id = player.team.pk
        return super(MessageCreateView, self).form_valid(form)


class LocationAJAXView(LoginRequiredMixin, ListView):
    login_url = '/dev/login'
    model = Waypoint

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Team.objects.all()
        else:
            team = Player.objects.get(user=user).team
            if team.team_class == Team.HUNTER:
                return Team.objects.filter(team_class=Team.HUNTED)
            else:
                return Team.objects.none()

    def get(self, request):
        teams = list(self.get_queryset())
        data = list()
        for team in teams:
            location = Location.objects.get(id=team.team_location_id)
            data.append({'team_name': team.team_name, 'lat':location.lat, 'lon': location.lon})

        return JsonResponse(json.dumps(data), status=200, safe=False)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            lat, lon = request.POST['lat'], request.POST['lon']

            team = Player.objects.get(user=user).team
            location = team.locations.create(lat=lat, lon=lon)
            team.team_location = location
            team.save()

        # Always return an empty HttpResponse on an ajax call.
        return HttpResponse('')


class WaypointAJAXView(LoginRequiredMixin, ListView):
    login_url = '/dev/login'
    model = Waypoint

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Waypoint.objects.all()
        elif user.is_authenticated:
            team = Player.objects.get(user=user).team
            print(team.team_class)
            if team.team_class == Team.HUNTED:
                print('Hunted team.')
                return Waypoint.objects.all()
            else:
                return Waypoint.objects.none()

    def get(self, request):
        queryset = self.get_queryset()
        data = serializers.serialize("json", queryset)
        return JsonResponse(data, status=200, safe=False)


class MapView(LoginRequiredMixin, TemplateView):
    login_url = '/dev/login'
    template_name = 'dev/map.html'


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/dev/login'
    template_name = 'dev/index.html'