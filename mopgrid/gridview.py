#!/usr/bin/python3
import threading
import time
import PySimpleGUI as sg

# based on https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Multithreaded_Long_Tasks.py


def run_simulation(window):
    window.write_event_value('-THREAD-', '** DONE **')


def the_gui():
    """
    Starts and executes the GUI
    Reads data from a Queue and displays the data to the window
    Returns when the user exits / closes the window
    """
    sg.theme('Light Brown 3')

    layout = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 400), graph_top_right=(400, 0),
                        background_color='white', key='graph')],
              [sg.Button('Run Sim', bind_return_key=True)],
              [sg.Button('Click Me'), sg.Button('Exit')], ]

    window = sg.Window('mopgrid', layout)
    window.Finalize()

    graph = window['graph']
    circle = graph.DrawCircle(
        (75, 75), 25, fill_color='black', line_color='white')
    point = graph.DrawPoint((75, 75), 10, color='green')
    oval = graph.DrawOval((25, 300), (100, 280),
                          fill_color='purple', line_color='purple')
    rectangle = graph.DrawRectangle((25, 300), (100, 280), line_color='purple')
    line = graph.DrawLine((0, 0), (100, 100))

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
