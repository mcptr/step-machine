from machine import Machine, Plot, Colors
import numpy as np


class MyPlot(Plot):
    width = 65
    steps = width // 2
    copies = 1
    char = "."
    spacing = 0
    default_color = Colors.BLUE

    def __call__(self, plane, loop, step, *args, **kwargs):
        char = Colors.white("@") if loop % 2 == 0 else Colors.green("@")
        pos = ((self.width // 2) - step)
        plane[pos] = char
        pos = ((self.width // 2) + step)
        plane[pos] = char

        char = Colors.orange("@") if loop % 2 == 0 else Colors.red("@")
        plane[step] = char
        plane[-step] = char


if __name__ == "__main__":
    machine = Machine(MyPlot, delay=0.02)
    machine.run()
