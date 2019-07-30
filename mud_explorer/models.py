from django.db import models


class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    terrain = models.CharField(max_length=255, blank=True)
    elevation = models.IntegerField(default=0)
    x = models.IntegerField()
    y = models.IntegerField()
    n_to = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="south")
    s_to = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="north")
    e_to = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="west")
    w_to = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="east")

    def get_exits(self):
        exit_coords = dict()
        if self.n_to is not None:
            exit_coords['n'] = {
                'id': self.n_to.id,
                'x': self.n_to.x,
                'y': self.n_to.y
            }
        if self.s_to is not None:
            exit_coords['s'] = {
                'id': self.s_to.id,
                'x': self.s_to.x,
                'y': self.s_to.y
            }
        if self.e_to is not None:
            exit_coords['e'] = {
                'id': self.e_to.id,
                'x': self.e_to.x,
                'y': self.e_to.y
            }
        if self.w_to is not None:
            exit_coords['w'] = {
                'id': self.w_to.id,
                'x': self.w_to.x,
                'y': self.w_to.y
            }
        return exit_coords

    def connect_room_nodes(self, direction, room_node):
        if direction == 'n':
            self.n_to, room_node.s_to = room_node, self
        elif direction == 's':
            self.s_to, room_node.n_to = room_node, self
        elif direction == 'e':
            self.e_to, room_node.w_to = room_node, self
        elif direction == 'w':
            self.w_to, room_node.e_to = room_node, self
        else:
            return None

    def get_coords(self):
        return self.x, self.y

    def __str__(self):
        return f'"{self.id}": {self.title}'
