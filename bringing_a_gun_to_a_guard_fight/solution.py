import itertools
from fractions import gcd

class Vector(tuple):
    def __add__(self, other):
        return Vector(d1 + d2 for d1 in self for d2 in other)

    def __sub__(self, other):
        return Vector(d1 - d2 for d1 in self for d2 in other)

    def __mul__(self, scale):
        return Vector(d * scale for d in self)

    def __div__(self, scale):
        return Vector(float(d) / scale for d in self)

    def __abs__(self):
        return sum(d ** 2 for d in self) ** 0.5

    def __neg__(self):
        return Vector(-d for d in self)

    def angle_ref_vector(self):
        """Returns a Vector dependent only on this Vector's angle, to compare
        with other vectors of different lengths."""
        if abs(self) == 0:
            return self
        return self / abs(reduce(gcd, self))

def answer(dimensions, captain_position, badguy_position, distance):
    bounds = (distance / d + 1 for d in dimensions)
    bound_ranges = (range(-b, b + 1) for b in bounds)
    repeats = list(itertools.product(*bound_ranges))

    def offset_dim(args):
        """Get a single dimension of a vector from shooter to shootee."""
        room_size, pos, origin, repeat = args
        offset = repeat * room_size - origin
        if repeat % 2 == 0:
            offset += pos
        else:
            # Mirror positions on odd repeats
            offset += room_size - pos
        return offset

    def get_angles(person_pos):
        angles = {}
        for repeat in repeats:
            dims = map(
                offset_dim,
                zip(dimensions, person_pos, captain_position, repeat)
            )
            v = Vector(dims)
            angle = v.angle_ref_vector()
            shot_dist = abs(v)

            if shot_dist == 0 or shot_dist > distance:
                continue

            # Only add if empty, or existing entry is further away.
            if angle not in angles or angles[angle] > shot_dist:
                angles[angle] = shot_dist
        return angles

    captain_angles = get_angles(captain_position)
    badguy_angles = get_angles(badguy_position)

    return sum(1 for a in badguy_angles if (
        a not in captain_angles
        or captain_angles[a] > badguy_angles[a]
    ))
