from django.db import models


class Room(models.Model):
    """
    A representation of a room on the server.

    :id: - The `room_id`
    :x: - The `x` coordinate on the map
    :y: - The `y` coordinate on the map
    :n: - The id of the room to the north (if any)
    :s: - The id of the room to the south (if any)
    :e: - The id of the room to the east (if any)
    :w: - The id of the room to the west (if any)
    """
    id = models.IntegerField(primary_key=True)
    x = models.IntegerField()
    y = models.IntegerField()
    n = models.IntegerField(blank=True, null=True)
    s = models.IntegerField(blank=True, null=True)
    e = models.IntegerField(blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)

    @classmethod
    def create(cls, id, x, y, n, s, e, w):
        return cls(id=id, x=x, y=y, n=n, s=s, e=e, w=w)
