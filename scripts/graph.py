import requests
import json
import time
from collections import deque


class Graph:
    def __init__(self):
        self.rooms = dict()
        self.visited = set()

    def add(self, room):
        if room.id not in self.rooms:
            self.rooms[room.id] = room
        else:
            return None

    def visit(self, room):
        self.visited.add(room.id)

    def has_been_visited(self, room):
        return room.id in self.visited

    def save(self):
        out_dict = dict()
        for key, room in self.rooms.items():
            out_dict[key] = eval(str(room))

        with open('output.json', 'w') as please_work:
            please_work.write(json.dumps(out_dict))

    def total_unexplored_rooms(self):
        unexplored = list()
        for key, room in self.rooms.items():
            exits = [room.get_room_in_direction(d) for d in room.get_exits()]
            if '?' in exits:
                unexplored.append(key)

        return len(unexplored)


class Room:
    def __init__(self, id, title, description, x, y):
        self.id = id
        self.title = title
        self.description = description
        self.x = x
        self.y = y
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None

    def __str__(self):
        exits = dict()
        for x in self.get_exits():
            exits[x] = "?" if type(self.get_room_in_direction(
                x)) == str else self.get_room_in_direction(x).id

        return f'[{(self.x, self.y)}, {exits}]'

    def __repr__(self):
        exits = dict()
        for x in self.get_exits():
            exits[x] = '?' if type(self.get_room_in_direction(
                x)) == str else self.get_room_in_direction(x).id

        return f"[{(self.x, self.y)}, {exits}]"

    def get_exits(self):
        exits = []
        if self.n_to is not None:
            exits.append("n")
        if self.s_to is not None:
            exits.append("s")
        if self.w_to is not None:
            exits.append("w")
        if self.e_to is not None:
            exits.append("e")
        return exits

    def get_exits_string(self):
        return f"Exits: [{', '.join(self.get_exits())}]"

    def connect_rooms(self, direction, connecting_rooms):
        if direction == "n":
            self.n_to = connecting_rooms
            connecting_rooms.s_to = self
        elif direction == "s":
            self.s_to = connecting_rooms
            connecting_rooms.n_to = self
        elif direction == "e":
            self.e_to = connecting_rooms
            connecting_rooms.w_to = self
        elif direction == "w":
            self.w_to = connecting_rooms
            connecting_rooms.e_to = self
        else:
            print("INVALID ROOM CONNECTION")
            return None

    def get_room_in_direction(self, direction):
        if direction == "n":
            return self.n_to
        elif direction == "s":
            return self.s_to
        elif direction == "e":
            return self.e_to
        elif direction == "w":
            return self.w_to
        else:
            return None

    def getCoords(self):
        return [self.x, self.y]


class Player:
    def __init__(self, name, token, starting_room):
        self.name = name
        self.token = token
        self.current_room = starting_room

    def travel(self, id):
        self.current_room = graph.rooms[id]


def bft():
    visited = set()
    queue = deque()
    queue.append([{player.current_room.id: None}])

    while len(queue) > 0:
        path = queue.popleft()
        vert = list(path[-1])[0]

        if vert not in visited:
            for new_exit in graph.rooms[vert].get_exits():
                new_path = list(path)

                if graph.rooms[vert].get_room_in_direction(new_exit) != '?':
                    output = {graph.rooms[vert].get_room_in_direction(new_exit).id: new_exit
                              }
                else:
                    output = {'?': new_exit}

                new_path.append(output)
                queue.append(new_path)

                if graph.rooms[vert].get_room_in_direction(new_exit) == '?':
                    return [
                        list(directions.values())[0] for directions in new_path[1:]
                    ]
            visited.add(vert)


BASE_URL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv'
headers = {
    'Authorization': 'Token 735f59e052bf0edf98fa68005e65388a08f729b6'
}
print('first pay', headers)
res = requests.get(f"{BASE_URL}/init", headers=headers).json()
print('first res', res)
id = res.get('room_id')
title = res.get('title')
cooldown = res.get('cooldown')
description = res.get('description')
coords = res.get('coordinates')
print(coords, title, 'First Print')
x, y = eval(coords)
exits = res.get('exits')

# Create room and mark exits with questionmark
first_room = Room(id, title, description, x, y)
first_room.n_to = "?" if "n" in exits else None
first_room.s_to = "?" if "s" in exits else None
first_room.e_to = "?" if "e" in exits else None
first_room.w_to = "?" if "w" in exits else None

graph = Graph()
player = Player('Leigh-Ann',
                '735f59e052bf0edf98fa68005e65388a08f729b6',
                first_room)

graph.add(first_room)
time.sleep(cooldown)

prev_direction = None
new_path = bft()

while graph.total_unexplored_rooms() > 0:
    for index, direction in enumerate(new_path):
        next_room = player.current_room.get_room_in_direction(
            direction) if player.current_room.get_room_in_direction(direction) != '?' else None

        if next_room is not None:
            payload = {
                'direction': direction,
                'next_room_id': str(next_room.id)
            }
        else:
            payload = {
                'direction': direction
            }
        print('second pay', payload, headers)
        res = requests.post(f"{BASE_URL}/move/",
                            headers=headers, json=payload).json()
        print('Second res', res)
        id = res.get('room_id')
        title = res.get('title')
        cooldown = res.get('cooldown')
        description = res.get('description')
        coords = res.get('coordinates')
        print(coords, title, 'Second Print')
        x, y = eval(str(coords))
        exits = res.get('exits')

        if id not in graph.rooms:
            new_room = Room(id, title, description, x, y)
            new_room.n_to = "?" if "n" in exits else None
            new_room.s_to = "?" if "s" in exits else None
            new_room.e_to = "?" if "e" in exits else None
            new_room.w_to = "?" if "w" in exits else None
            graph.add(new_room)
        else:
            new_room = graph.rooms[id]

        if player.current_room.get_room_in_direction(direction) == '?':
            player.current_room.connect_rooms(direction, new_room)

        player.travel(id)
        prev_direction = direction
        graph.save()
        time.sleep(cooldown)
    new_path = bft()
    print(new_path)
    print(new_room)
