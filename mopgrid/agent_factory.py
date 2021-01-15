import random
from enum import IntEnum

from mopgrid.simerrors import SimulationErrorCode
from mopgrid.space import Coords, clean_command, moveto_command


class Direction(IntEnum):
    N = 0
    E = 1
    W = 2
    S = 3


def _new_location(loc):
    direction = random.randint(0, 3)
    print(direction)
    if direction == Direction.E:
        return Coords(row=loc.row, col=loc.col + 1)
    elif direction == Direction.W:
        return Coords(row=loc.row, col=loc.col - 1)
    elif direction == Direction.N:
        return Coords(row=loc.row - 1, col=loc.col)
    elif direction == Direction.S:
        return Coords(row=loc.row + 1, col=loc.col)


class SimpleCleaningAgent:
    def __init__(self, params=None):
        self.params = params
        self.cmd_success = True
        self.failure_reason = None
        self.err_code = None
        self.loc = None
        self.agent_id = None
        self.space_size = None

    def command_result(self, success, failure_reason, err_code, loc):
        self.cmd_success = success
        self.failure_reason = failure_reason
        self.err_code = err_code
        if self.err_code == SimulationErrorCode.SIM_SUCCESS:
            self.loc = loc

    def next_command(self, loc, is_dirty):
        if is_dirty:
            return clean_command(agent_id=self.agent_id, loc=loc)
        else:
            new_loc = _new_location(loc)
            return moveto_command(agent_id=self.agent_id,
                                  loc=new_loc)


class AgentFactory:
    def __init__(self):
        self._agent_types = {
            "simple": {
                "module": "mopgrid.agent_factory",
                "class": "SimpleCleaningAgent"
            }
        }

    def _get_agent(self, name, params):
        agent_config = self._agent_types[name]
        if agent_config:
            mod = __import__(agent_config["module"], fromlist=[agent_config["class"]])
            klass = getattr(mod, agent_config["class"])
            return klass(params=params)

    def create_agents(self, agent_config):
        agent_ls = []
        for c in agent_config:
            agent = self._get_agent(c["type"], c["params"])
            agent_ls.append(agent)
        return agent_ls
