from collections import deque, Counter

# An implementation of Dinic's Algorithm:
# https://en.wikipedia.org/wiki/Dinic%27s_algorithm

class Room(object):
    def __init__(self, index, is_sink=False):
        self.index = index
        self.is_sink = is_sink
        self.residuals = Counter()
        self.flows = Counter()
        self.distance = None

    def __repr__(self):
        residual_repr = { r.index : o for r, o in self.residuals.items() }
        flow_repr = { r.index : o for r, o in self.flows.items() }

        return "Room({}, d={}, f={}, r={})".format(
            self.index,
            self.distance,
            flow_repr,
            residual_repr
        )

    @property
    def level_graph_neighbours(self):
        return [ r for r in self.residuals if r.distance == self.distance + 1 ]

    def push(self, incoming):
        if self.is_sink:
            return incoming

        outgoing = 0

        for room in self.level_graph_neighbours:
            if outgoing == incoming:
                break

            to_push = min(
                incoming - outgoing,
                self.residuals[room] - self.flows[room]
            )

            flow = room.push(to_push)
            self.flows[room] += flow
            outgoing += flow

        return outgoing

    def update_residuals(self):
        for room, flow in self.flows.items():
            self.residuals[room] -= flow
            room.residuals[self] += flow

        self.flows = Counter()

def get_distances(rooms, source):
    """Breadth-first search for distance from source to sink"""
    for r in rooms:
        r.distance = None

    source.distance = 0
    search_q = deque([source])

    while search_q:
        cur_room = search_q.popleft()

        for room, res in cur_room.residuals.items():
            if res == 0:
                continue

            if room.distance is not None:
                continue

            room.distance = cur_room.distance + 1
            search_q.append(room)

def construct_rooms(entrances, exits, path):
    room_count = len(path)

    rooms = [ Room(i) for i in range(room_count) ]

    for i, room in enumerate(rooms):
        if i in exits:
            continue

        rooms[i].residuals = Counter({
            rooms[j] : o for j, o in enumerate(path[i]) if o > 0
        })

    source = Room("s")
    source.residuals = Counter({ rooms[i] : float("inf") for i in entrances })

    sink = Room("t", is_sink=True)
    for i in exits:
        rooms[i].residuals = Counter({ sink : float("inf") })

    rooms += [ source, sink ]

    return rooms, source, sink

def answer(entrances, exits, path):
    total_flow = 0
    rooms, source, sink = construct_rooms(entrances, exits, path)

    while True:
        get_distances(rooms, source)

        if sink.distance is None:
            break

        total_flow += source.push(float("inf"))

        for room in rooms:
            room.update_residuals()

    return total_flow
