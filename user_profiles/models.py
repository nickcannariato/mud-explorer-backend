import time
from queue import Queue
from django.db import models
from django.contrib.auth.models import User
from mud_explorer.models import Room
import requests


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game_token = models.CharField(max_length=255)
    encumbrance = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    current_location = models.ForeignKey(Room,
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def update_location(self, room):
        self.current_location = room
        self.save()

    def bfs(self, rooms_dict):
        visited = set()
        queue = Queue()
        queue.put([self.current_location[id]])

        while not queue.empty():
            path = queue.get()
            vert = path[0]
            if vert not in visited:
                for new_room in rooms_dict[vert]:
                    new_path = list(path)
                    k = rooms_dict[vert].get_room_in_dir(new_room)
                    new_path.append(
                        {k.id: new_room} if k != '?' else {'?': new_room}
                    )
                    queue.put(new_path)

                    if k == '?':
                        return [list(path.values()[0]) for path in new_path[1:]]

                visited.add(vert)

        return None

    def get_num_unexplored(self, rooms_dict):
        output = []
        for key, value in rooms_dict.items():
            potential_exits = [value.get_room_in_dir(direction)
                               for direction in value.get_exits()]

            if '?' in potential_exits:
                output.append(key)
        return len(output)

    def map_rooms(self):
        rooms = dict()
        visited = set()
        res = requests.get(f"{BASE_URL}/init").json()

        id = res.get('room_id')
        title = res.get('title')
        description = res.get('description')
        elevation = res.get('elevation')
        terrain = res.get('terrain')
        x, y = eval(res.get('coordinates'))
        cooldown = res.get('cooldown')
        exits = res.get('exits')

        rooms[id] = {'id': id, 'title': title, 'description': description,
                     'elevation': elevation, 'terrain': terrain, 'x': x, 'y': y}
        rooms[id]['n_to'] = "?" if "n" in exits else None
        rooms[id]['s_to'] = "?" if "s" in exits else None
        rooms[id]['e_to'] = "?" if "e" in exits else None
        rooms[id]['w_to'] = "?" if "w" in exits else None
        first_room = rooms[id]

        self.update_location(first_room)
        time.sleep(cooldown)

        newpath = self.bfs(rooms)

        while self.get_num_unexplored(rooms) > 0:
            for index, direction in enumerate(newpath):
                if self.current_location.get_room_in_dir(direction) != '?':
                    next_room = self.current_location.get_room_in_dir(
                        direction)
                else:
                    next_room = None

                if next_room is not None:
                    payload = {
                        'direction': direction,
                        'next_room_id': str(next_room.id)
                    }
                else:
                    payload = {'direction': direction}

                res = requests.post(f'{BASE_URL}/move', json=payload).json()

                id = res.get('room_id')
                title = res.get('title')
                description = res.get('description')
                elevation = res.get('elevation')
                terrain = res.get('terrain')
                x, y = eval(res.get('coordinates'))
                cooldown = res.get('cooldown')
                exits = res.get('exits')

                if id not in rooms:
                    new_room = Room(id=id, x=x, y=y, title=title,
                                    description=description, elevation=elevation, terrain=terrain)
                    new_room.n_to = "?" if "n" in exits else None
                    new_room.s_to = "?" if "s" in exits else None
                    new_room.e_to = "?" if "e" in exits else None
                    new_room.w_to = "?" if "w" in exits else None
                    new_room.save()

                    rooms[new_room.id] = new_room
                    self.update_location(rooms[new_room.id])
