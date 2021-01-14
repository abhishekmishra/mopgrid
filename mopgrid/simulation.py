from enum import Enum, auto
from mopgrid.simerrors import SimulationError, SimulationErrorCode


class SimState(Enum):
    STOPPED = auto()
    RUNNING = auto()
    ABORTED = auto()


class Simulation:
    def __init__(self, config=None):
        self.config = config
        if config is None:
            self._load_default_config()

        self.viewers = []
        self.aggregators = []
        self._state = SimState.STOPPED
        self.id = None
        self.name = None
        self.space = None
        self.agents = None
        self.abort = False

    def _load_default_config(self):
        pass

    def run(self):
        if self._state == SimState.STOPPED:
            self.prepare()
            self._run()
        else:
            raise SimulationError(message="simulation is already running",
                                  err_code=SimulationErrorCode.SIM_ERR_SIM_RUNNING)

    def prepare(self):
        # create the space from config
        self.space = None
        # create the agents from config
        self.agents = []
        # create initial locations for agents in the space
        pass

    def _run(self):
        self.round = 0
        self._state = SimState.RUNNING

        for viewer in self.viewers:
            agent_commands = []
            viewer.show_state(self.round, agent_commands, self.space, self.agents)
        for viewer in self.viewers:
            viewer.signal_start(self.id, self.name)

        self._publish_stats()

        if len(self.agents) > 0:
            self.round = 1
            while self.space.has_dirty_cell():
                if self.abort:
                    self.abort = False
                    self._state = SimState.ABORTED
                    break

                agent_commands = []
                for agent in self.agents:
                    (row, col) = self.space.where_am_i(id=agent.id)
                    dirty = self.space.is_dirty(location=(row, col))
                    cmd = agent.next_command(location=(row, col), dirty=dirty)
                    try:
                        if cmd.command == "clean":
                            self.space.clean(cmd.agent_id, cmd.location)
                        elif cmd.command == "move_to":
                            self.space.move_to(cmd.agent_id, cmd.location)
                        cmd.status = True
                        cmd.failure_reason = None
                        agent_commands.append(cmd)
                        agent.command_result(success=True, failure_reason=None,
                                             err_code=SimulationErrorCode.SIM_SUCCESS, location=cmd.location)
                    except SimulationError as se:
                        cmd.status = False
                        cmd.failure_reason = se.message
                        agent_commands.append(cmd)
                        agent.command_result(success=False, failure_reason=se.message, err_code=se.err_code,
                                             location=se.loc)
                    except Exception as e:
                        cmd.status = False
                        cmd.failure_reason = e.message
                        agent_commands.append(cmd)
                        agent.command_result(success=False, failure_reason=e.message,
                                             err_code=SimulationErrorCode.SIM_ERR_UNKNOWN, location=cmd.location)
                for viewer in self.viewers:
                    viewer.show_state(self.round, agent_commands, self.space, self.agents)
                self._publish_stats()
                self.round += 1

        for viewer in self.viewers:
            viewer.signal_complete(self.id, self.name)

    def _publish_stats(self):
        pass
