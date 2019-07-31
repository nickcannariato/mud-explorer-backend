from django.db import models
from django.contrib.auth.models import User
from mud_explorer.models import Room
import requests


class Graph:
    def __init__(self):
        self.rooms = dict()
        self.visited = set()

    def add(self, room):
        room_id = room.id
        if not self.rooms.get(room_id):
            self.rooms[room.id] = {room_id: room.gen_object()}

    def mark_visited(self, room_id):
        self.visited.add(room_id)

    def player_has_visited(self, room_id):
        return room_id in self.visited


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game_token = models.CharField(max_length=255)
    current_location = models.ForeignKey(Room,
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def update_location(self, room):
        self.location = room
