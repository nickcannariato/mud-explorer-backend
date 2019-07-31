from django.db import models


class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    terrain = models.CharField(max_length=255, blank=True)
    elevation = models.IntegerField(default=0)
    x = models.IntegerField()
    y = models.IntegerField()
    n_to = models.CharField(max_length=255)
    s_to = models.CharField(max_length=255)
    e_to = models.CharField(max_length=255)
    w_to = models.CharField(max_length=255)

    def get_exits(self):
        exit_dir = list()
        if self.n_to is not None:
            exit_dir.append('n')
        if self.s_to is not None:
            exit_dir.append('s')
        if self.e_to is not None:
            exit_dir.append('e')
        if self.w_to is not None:
            exit_dir.append('w')
        return exit_dir

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
        return {"x": self.x, "y": self.y}

    def gen_room_list(self):
        return [
            self.get_coords(),
            self.get_exits()
        ]

    def get_room_in_dir(self, direction):
        if direction == 'n':
            return self.n_to
        elif direction == 's':
            return self.s_to
        elif direction == 'e':
            return self.e_to
        elif direction == 'w':
            return self.w_to

    def __str__(self):
        return f'"{self.id}": {self.gen_room_list()}'
