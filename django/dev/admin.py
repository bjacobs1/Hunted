from django.contrib import admin

# Register your models here.
from .models import Player, Team, Location, Message, HuntedTag, Waypoint

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Waypoint)
admin.site.register(Location)
admin.site.register(Message)
admin.site.register(HuntedTag)