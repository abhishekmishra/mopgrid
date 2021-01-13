# MopGrid
A __simulator__ for a simple two dimensional space (or grid) which has various kinds of cells.

## MopGrid Space
The simplest space has 3 kinds of cells:
1. Empty Cell (Value 0)
2. Wall Cell (Value 1)
3. Dirty Cell (Value 2)

In general an agent can move to any 0 or even-numbered cell.
Any cell might also have one or more agents at the cell at any time. Usually the simulator might restrict the presence of more than one agent at a cell.

### File Format
A mopgrid space file format is a simple textual representation which can shows current state of a space, and optionally the simulator - so that a simulation can be restarted or replayed.

The file format has the following components:
1. Metadata: Program name, generation date etc. 
1. Cell Types: This is a space separated sequence of numbers. All possible values at a grid can be listed here for e.g. "0 1 2" - OR this can also be a range of values [0-2].
1. Agents: Names of agents which are present in the map. Agent names are alphanumeric to distinguish from cell values. for e.g. "A B C"
1. Grid/space Dimensions: Space separated list of dimension size. for e.g. "10 20" - which is a 10x20 grid
1. Grid state: Multiple lines of space separated values. Each line being a row (y-dimension) and values in line being the cells in columns (x-dimension).
1. Simulator state: Simulator can dump state at any time in this section to allow it to resume from this point.

Implementation-wise this file format can be a program which returns an object which has the above fields when run. For large grids with repeatable patterns this allows one to use a more compact format for the grid.

However this also makes visualization of the grid difficult which means a basic viewer would be necessary.

TODO: finalize file format

## Agent
An agent is a program which is placed in the simulator, and is allowed to move and perform certain actions. In the simple space example given above the agent can move to a neighbouring cell, and also clean it.

## Simulator
The simulator allows one or more agents to move around the grid using pre-defined commands,
and allows the agents to take some simple actions.
The simulator is a turn-based program, providing a single chance to issue a command in every turn or round. The requests for commands can be made in parallel or in a sequence (pre-configured or random)