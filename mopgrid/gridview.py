#!/usr/bin/python3
import threading
import time
import PySimpleGUI as sg
import mopgrid.space


# based on https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Multithreaded_Long_Tasks.py


def run_simulation(window):
    window.write_event_value('-THREAD-', '** DONE **')


GRAPH_WIDTH = 400
GRAPH_HEIGHT = 400


def draw_grid_lines(graph, row, col):
    for i in range(row + 1):
        y = i * ((GRAPH_HEIGHT - 1) / row)
        graph.DrawLine((0, y), (GRAPH_WIDTH, y))

    for i in range(col + 1):
        x = i * ((GRAPH_WIDTH - 1) / col)
        graph.DrawLine((x, 0), (x, GRAPH_HEIGHT))


def cell_loc(w, h, x, y):
    cell_h = (GRAPH_HEIGHT - 1) / h
    cell_w = (GRAPH_WIDTH - 1) / w
    return x * cell_w, y * cell_h, cell_w, cell_h


def draw_wall(graph, w, h, x, y):
    cell_h = (GRAPH_HEIGHT - 1) / h
    cell_w = (GRAPH_WIDTH - 1) / w
    graph.DrawRectangle((x * cell_w, y * cell_h),
                        ((x + 1) * cell_w, (y + 1) * cell_h),
                        fill_color='black')


def draw_dirty(graph, w, h, x, y):
    cell_h = (GRAPH_HEIGHT - 1) / h
    cell_w = (GRAPH_WIDTH - 1) / w
    graph.DrawRectangle((x * cell_w, y * cell_h),
                        ((x + 1) * cell_w, (y + 1) * cell_h),
                        fill_color='yellow')


def draw_grid(graph, grid):
    grid_details = grid["space"]
    width = grid_details["size"]["col"]
    height = grid_details["size"]["row"]
    cells = grid_details["cells"]
    agents = grid_details["agents"]
    draw_grid_lines(graph, height, width)
    for x in range(width):
        for y in range(height):
            cell = cells[y][x]
            if cell == 1:
                draw_wall(graph, width, height, x, y)
            elif cell == 2:
                draw_dirty(graph, width, height, x, y)
    for agent, loc in agents.items():
        print(agent, loc)
        if loc is not None:
            cx, cy, cell_w, cell_h = cell_loc(width, height, loc['col'], loc['row'])
            font_size = round(min(cell_w, cell_h))
            print(font_size)
            graph.DrawText(agent, location=(cx + (cell_w/2), cy + (cell_h/2)), color='red',
                           text_location=sg.TEXT_LOCATION_CENTER, font=(None, font_size))


def the_gui():
    """
    Starts and executes the GUI
    Reads data from a Queue and displays the data to the window
    Returns when the user exits / closes the window
    """
    sg.theme('Light Brown 3')

    layout = [[sg.Graph(canvas_size=(GRAPH_WIDTH, GRAPH_HEIGHT), graph_bottom_left=(0, GRAPH_HEIGHT),
                        graph_top_right=(GRAPH_WIDTH, 0),
                        background_color='white', key='graph')],
              [sg.Button('Run Sim', bind_return_key=True)],
              [sg.Button('Click Me'), sg.Button('Exit')], ]

    window = sg.Window('mopgrid', layout)
    window.Finalize()

    graph = window['graph']

    grid = mopgrid.space.sample_grid()
    draw_grid(graph, grid)

    # circle = graph.DrawCircle(
    #     (75, 75), 25, fill_color='black', line_color='white')
    # point = graph.DrawPoint((75, 75), 10, color='green')
    # oval = graph.DrawOval((25, 300), (100, 280),
    #                       fill_color='purple', line_color='purple')
    # rectangle = graph.DrawRectangle((25, 300), (100, 280), line_color='purple')
    # line = graph.DrawLine((0, 0), (100, 100))

    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event.startswith('Do'):
            print('Starting simulation')
            threading.Thread(target=run_simulation, args=(
                window,), daemon=True).start()
        elif event == 'Click Me':
            print('Your GUI is alive and well')
        elif event == '-THREAD-':
            print('Got a message back from the thread: ', values[event])

    # if user exits the window, then close the window and exit the GUI func
    window.close()


if __name__ == '__main__':
    the_gui()
    print('Exiting Program')
