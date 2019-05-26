from machine import Machine, Plot
import numpy as np


class MyPlot(Plot):
    width = 64
    steps = width + 2
    copies = 1
    char = "."

    def __call__(self, plane, loop, step, *args, **kwargs):
        if step < self.width:
            plane[step] = "+"
            plane[:step - 1] = ["_"] * (step - 1)
            # plane[:int(step / 4)] = [self.char] * int(step / 4)
        else:
            plane[:] = self.full_line("+")


if __name__ == "__main__":
    machine = Machine(MyPlot, delay=0.02)
    machine.run()
