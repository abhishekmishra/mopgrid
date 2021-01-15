import os
import json
import numpy as np
from enum import IntEnum
import random
from mopgrid.simerrors import SimulationError, SimulationErrorCode


class CellType(IntEnum):
    EMPTY = 0
    WALL = 1
    DIRTY = 2


class Coords:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "[" + str(self.row) + ", " + str(self.col) + "]"


class AgentState:
    def __init__(self, agent_id, loc):
        self.agent_id = agent_id
        self.loc = loc

    def move_to(self, to_loc):
        self.loc = to_loc


class Command:
    def __init__(self, agent_id, command, location=None):
        self.agent_id = agent_id
        self.command = command
        self.location = location
        self.status = False
        self.failure_reason = None


def clean_command(agent_id, loc):
    return Command(agent_id=agent_id, command="clean", location=loc)


def moveto_command(agent_id, loc):
    return Command(agent_id=agent_id, command="move_to", location=loc)


class Space:
    def __init__(self, size=Coords(10, 10), dirty_prob=0.3, wall_prob=0.2):
        self.size = size
        self.dirty_prob = dirty_prob
        self.wall_prob = wall_prob
        self.space = np.zeros([size.row, size.col], dtype=int)
        self.agent_space = np.zeros([size.row, size.col], dtype=int)
        self.random_wall()
        self.random_dirty()
        self.agents = {}

    def random_wall(self):
        for y in range(self.size.row):
            for x in range(self.size.col):
                r = random.random()
                if r <= self.wall_prob:
                    self.space[y, x] = CellType.WALL

    def random_dirty(self):
        for y in range(self.size.row):
            for x in range(self.size.col):
                if self.space[y, x] != CellType.WALL:
                    r = random.random()
                    if r <= self.dirty_prob:
                        self.space[y, x] = CellType.DIRTY

    def query(self, loc):
        return self.space[loc.row, loc.col]

    def is_dirty(self, loc):
        return self.query(loc) == CellType.DIRTY

    def is_wall(self, loc):
        return self.query(loc) == CellType.WALL

    def is_clean(self, loc):
        return not self.is_dirty(loc)

    def has_agent(self, loc):
        val = self.query(loc)
        if val > 2 and val % 2 == 1:
            return True
        else:
            return False

    def can_place_agent(self, loc):
        if self.query(loc) == CellType.EMPTY or self.is_dirty(loc):
            return True
        return False

    def where_am_i(self, agent_id):
        a = self.agents[agent_id]
        if a is not None:
            return a.loc
        else:
            return None

    def init_agent(self):
        count_tries = 0
        while count_tries < 10:
            row = random.randint(0, self.size.row - 1)
            col = random.randint(0, self.size.col - 1)
            loc = Coords(row, col)

            if self.can_place_agent(loc):
                agent_id = -1
                if len(self.agents.keys()) == 0:
                    agent_id = 3
                else:
                    agent_id = max(self.agents.keys()) + 2
                print("agent added = " + str(agent_id))
                self.agents[agent_id] = AgentState(agent_id, loc)
                self.agent_space[loc.row, loc.col] = agent_id
                return agent_id
            count_tries += 1

    def check_range(self, loc):
        if loc.row < 0 or loc.row >= self.size.row or loc.col < 0 or loc.col >= self.size.col:
            raise SimulationError("Row/col is out of range: " + str(loc),
                                  SimulationErrorCode.SIM_ERR_OUT_OF_RANGE, loc)

    def move_to(self, agent_id, to_loc):
        self.check_range(to_loc)
        if agent_id in self.agents:
            a = self.agents[agent_id]
            if abs(to_loc.row - a.loc.row) < 2 and abs(to_loc.col - a.loc.col) < 2:
                if not self.is_wall(to_loc):
                    if self.is_clean(to_loc) or self.is_dirty(to_loc):
                        self.agent_space[a.loc.row, a.loc.col] = CellType.EMPTY
                        self.agent_space[to_loc.row, to_loc.col] = agent_id
                        a.move_to(to_loc)
                    else:
                        raise SimulationError("There is already an agent there!",
                                              SimulationErrorCode.SIM_ERR_AGENT_COLLISION, to_loc)
                else:
                    raise SimulationError("Cannot move into a wall!",
                                          SimulationErrorCode.SIM_ERR_MOVE_TO_WALL, to_loc)
            else:
                raise SimulationError("New location is not adjacent!",
                                      SimulationErrorCode.SIM_ERR_LOCATION_NOT_ADJACENT, to_loc)
        else:
            raise SimulationError("Agent does not exist!",
                                  SimulationErrorCode.SIM_ERR_NO_SUCH_AGENT, to_loc)

    def clean(self, agent_id, to_loc):
        self.check_range(to_loc)
        if agent_id in self.agents:
            a = self.agents[agent_id]
            if a.loc.row == to_loc.row and a.loc.col == to_loc.col:
                if self.is_dirty(to_loc):
                    self.space[to_loc.row, to_loc.col] = CellType.EMPTY
                else:
                    raise SimulationError("Location is not dirty!", SimulationErrorCode.SIM_ERR_LOCATION_NOT_DIRTY,
                                          to_loc)
            else:
                raise SimulationError("Agent is not at the location to clean!",
                                      SimulationErrorCode.SIM_ERR_AGENT_NOT_AT_LOCATION, to_loc)
        else:
            raise SimulationError("Agent does not exist!",
                                  SimulationErrorCode.SIM_ERR_NO_SUCH_AGENT, to_loc)

    def total_dirty(self):
        count = 0
        for i in range(self.size.row):
            for j in range(self.size.col):
                if self.is_dirty(Coords(i, j)):
                    count += 1
        return count

    def has_dirty(self):
        # can improve by returning after finding first dirty cell
        return self.total_dirty() > 0


def sample_grid():
    gpath = os.path.join(os.getcwd(), "..", "test", "data", "sample0.json")
    with open(gpath, "r") as f:
        gstr = f.read()
        g = json.loads(gstr)
    return g


if __name__ == "__main__":
    s = Space()
    print(s.space)
