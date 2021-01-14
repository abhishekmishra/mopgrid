from enum import Enum, auto


class SimulationErrorCode(Enum):
    SIM_SUCCESS = auto()
    SIM_ERR_UNKNOWN = auto()
    SIM_ERR_AGENT_DOES_NOT_EXIST = auto()
    SIM_ERR_LOCATION_NOT_ADJACENT = auto()
    SIM_ERR_MOVE_TO_WALL = auto()
    SIM_ERR_AGENT_COLLISION = auto()
    SIM_ERR_LOCATION_NOT_DIRTY = auto()
    SIM_ERR_AGENT_NOT_AT_LOCATION = auto()
    SIM_ERR_NO_SUCH_AGENT = auto()
    SIM_ERR_OUT_OF_RANGE = auto()
    SIM_ERR_SIM_RUNNING = auto()


class SimulationError(Exception):
    def __init__(self, message, err_code, loc=None):
        self.err_code = err_code
        self.loc = loc
        self.message = message
