from enum import Enum, auto
from mopgrid.simerrors import SimulationError, SimulationErrorCode
from mopgrid.space import Space, CellType, Coords
from mopgrid.agent_factory import AgentFactory
import json


class SimState(Enum):
    STOPPED = auto()
    RUNNING = auto()
    ABORTED = auto()


class ConsoleSimViewer:
    def sim_aborted(self):
        print("Sim Aborted");

    def sim_start(self, sim_num, sim_name):
        print("Sim #" + str(sim_num) + ":" + str(sim_name) + " started.")

    def sim_complete(self, sim_num, sim_name):
        print("Sim #" + str(sim_num) + ":" + str(sim_name) + " completed.")

    def show_state(self, sim_round, commands, space, agents_space):
        pass

    def show_message(self, message):
        pass


class Simulation:
    def __init__(self, config_file=None):
        self.agent_factory = AgentFactory()
        self.config_file = config_file
        self.config = None
        self._load_config()

        self.viewers = []
        self.aggregators = []
        self._state = SimState.STOPPED
        self.id = None
        self.name = None
        self.space = None
        self.agents = None
        self.abort = False

    def _load_config(self):
        if self.config_file:
            with open(self.config_file, "r") as f:
                self.config = json.loads(f.read())
        else:
            self.config = {
                "space": {
                    "config": {
                        "size": {
                            "row": 2,
                            "col": 2
                        },
                        "dirt_probability": 0.3,
                        "wall_probability": 0.1
                    }
                },
                "agents": [
                    {
                        "type": "simple",
                        "params": {}
                    },
                    # {
                    #     "type": "simple.bound",
                    #     "params": {}
                    # },
                    # {
                    #     "type": "simple.boundandwall",
                    #     "params": {}
                    # },
                    # {
                    #     "type": "spiral",
                    #     "params": {}
                    # },
                ]
            }

    def run(self):
        if self._state == SimState.STOPPED:
            self.prepare()
            self._run()
        else:
            raise SimulationError(message="simulation is already running",
                                  err_code=SimulationErrorCode.SIM_ERR_SIM_RUNNING)

    def prepare(self):
        space_config = self.config["space"]["config"]
        # create the space from config
        self.space = Space(size=Coords(space_config["size"]["row"],
                                       space_config["size"]["col"]),
                           dirty_prob=space_config["dirt_probability"],
                           wall_prob=space_config["wall_probability"])
        # create the agents from config
        self.agents = self.agent_factory.create_agents(self.config["agents"])
        for a in self.agents:
            agent_id = self.space.init_agent()
            a.agent_id = agent_id
            a.space_size = self.space.size

        print(self.agents)
        # create initial locations for agents in the space
        pass

    def _run(self):
        self.round = 0
        self._state = SimState.RUNNING

        for viewer in self.viewers:
            agent_commands = []
            viewer.show_state(self.round, agent_commands, self.space, self.agents)
        for viewer in self.viewers:
            viewer.sim_start(self.id, self.name)

        self._publish_stats()

        if len(self.agents) > 0:
            self.round = 1
            while self.space.has_dirty():
                if self.abort:
                    self.abort = False
                    self._state = SimState.ABORTED
                    break

                agent_commands = []
                for agent in self.agents:
                    location = self.space.where_am_i(agent_id=agent.agent_id)
                    dirty = self.space.is_dirty(location=location)
                    cmd = agent.next_command(location=location, dirty=dirty)
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
                        cmd.failure_reason = str(e)
                        agent_commands.append(cmd)
                        agent.command_result(success=False, failure_reason=str(e),
                                             err_code=SimulationErrorCode.SIM_ERR_UNKNOWN, location=cmd.location)
                for viewer in self.viewers:
                    viewer.show_state(self.round, agent_commands, self.space, self.agents)
                self._publish_stats()
                self.round += 1

        for viewer in self.viewers:
            viewer.sim_complete(self.id, self.name)

    def _publish_stats(self):
        pass


if __name__ == '__main__':
    sim = Simulation()
    sim.viewers.append(ConsoleSimViewer())
    sim.run()
