import os
import json
import numpy as np
from enum import Enum


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    DIRTY = 2


class Coords:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Command:
    def __init__(self, agent_id, command, location=None):
        self.agent_id = agent_id
        self.command = command
        self.location = location
        self.status = False
        self.failure_reason = None


def clean_command(agent_id):
    return Command(agent_id=agent_id, command="clean")


def moveto_command(agent_id, x, y):
    return Command(agent_id=agent_id, command="move_to", location=Coords(row=x, column=y))


class Space:
    def __init__(self, size=Coords(10, 10), dirty_prob=0.3, wall_prob=0.2):
        self.size = size
        self.dirty_prob = dirty_prob
        self.wall_prob = wall_prob
        self.space = np.zeros([size.row, size.column], dtype=int)
        self.random_wall()
        self.random_dirty()

    def random_wall(self):
        for y in range(self.size.row):
            for x in range(self.size.column):
                pass

def sample_grid():
    gpath = os.path.join(os.getcwd(), "..", "test", "data", "sample0.json")
    with open(gpath, "r") as f:
        gstr = f.read()
        g = json.loads(gstr)
    return g


if __name__ == "__main__":
    g = sample_grid()
    print(g["metadata"])
