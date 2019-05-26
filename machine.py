# The whole program can be reduced to the basic idea as follows:
#
# loop = 0
# steps = 8
# line_size = 16
#
# while True:
#     loop += 1
#     line = [" ", ] * line_size
#     for step in range(0, steps):
#         your_function(line, loop, step)
#         print(line)

#
# The code below is a little more elaborate implementation
# of such a line-input-step text-based-animation machine.
#
# It scrolls a 2D plane (a surface, a fabric).
# The scrolling happens line by line. Th scrolling direction is
# considered y axis.
# A single line is constitutes x axis.
# Only a single line can be modified in each step.
# Y is always 0, the only motion can be done along x axis, in 1D.
#
# The machine output can be programmed by using a Plot.
# The basic Plot definition is given below.
# A Plot is treated as a callable (hence custom implementation
# of the __call__ method).
# Such a plot receives a single line of the plane (x-axis),
# the sequential loop iteration number and current step in the
# sequence.
#
# The plot can use colors. Example of a custom Plot (pattern)
# is at the bottom of this file.
# Others may be found in the "examples/" directory.
#
# The Plot is initialized by the Machine and is given
# a reference to the machine instance itself.
# This means that by manipulating self.machine within the plot
# the properties of the machine can be accessed and modified.
# For instance, the speed of the machine could be controlled.


import time
import logging
import os

# setup logging. logs DEBUG if run with DEBUG=1 in the environment.
logging.basicConfig(
    level=(logging.DEBUG
           if bool(os.environ.get("DEBUG", 0))
           else logging.INFO),
    format=" ".join([
        "%(asctime)s [%(levelname)s] %(name)s",
        "%(module)s::%(funcName)s %(message)s"
    ])
)


class Colors:
    """Colors for the output."""

    WHITE = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'

    # These are supposed to be used as Colors.green("my text"), Colors.red("!")
    white = (lambda txt: '\033[0m' + txt + Colors.WHITE)
    red = (lambda txt: '\033[31m' + txt + Colors.WHITE)
    green = (lambda txt: '\033[32m' + txt + Colors.WHITE)
    orange = (lambda txt: '\033[33m' + txt + Colors.WHITE)
    blue = (lambda txt: '\033[34m' + txt + Colors.WHITE)
    purple = (lambda txt: '\033[35m' + txt + Colors.WHITE)


class Plot:
    """
    Basic plot definition.
    Members:
    width - x-axis length is the width.
    steps - the number of lines after which the pattern repeats (next loop).
    copies - how many copies of a line to output
    char - default text character
    spacing - spacing between output line elements
    """
    width = 16
    steps = 8
    copies = 1
    char = "."
    spacing = 1
    default_color = Colors.WHITE
    color = Colors.WHITE

    def __init__(self, machine):
        """
        Arguments:
        - machine - the actual machine the plot is being run on
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.machine = machine
        self.log.debug("Initializing")
        self.log.debug("Machine: %s", self.machine)
        self.set_color(self.default_color)

    def __call__(self, plane, loop, step, *args, **kwargs):
        """
        The default plotting function
        plane - a line, list of n=self.width points on the x-axis.
        loop - current loop number
        step - current step in current loop

        plane is supposed to be modified in-place.
        """
        pass

    def set_color(self, color):
        self.color = color

    def reset_color(self):
        self.color = self.default_color

    def full_line(self, char=None):
        return [char or self.char] * self.width


class Machine:
    """
    Basic machine.
    """
    def __init__(self, plot_class=Plot, **kwargs):
        """
        Initializes the plot and sets defaults.
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.plot = plot_class(self)
        self.delay = kwargs.pop("delay", 0)  # seconds

    def run(self):
        """
        Starts running until halted.
        Runs n=steps (lines) through the plot callable and prints them.
        """
        self.log.debug("Plotting")
        loop = 0
        j_char = " " * self.plot.spacing + ""
        while True:
            for step in range(self.plot.steps):
                plane = [self.plot.color + self.plot.char] * self.plot.width
                self.plot(plane, loop, step)
                plane = j_char.join([j_char.join(plane)] * self.plot.copies)
                print("%s%2d %2d\t%s" % (Colors.WHITE, loop, step, plane))
                time.sleep(self.delay)
            loop += 1


if __name__ == "__main__":
    import random

    class HelloWorldPlot(Plot):
        _DATA = "hello world!"
        width = len(_DATA)
        steps = len(_DATA) + 2

        def __call__(self, plane, loop, step, *args, **kwargs):
            """
            plane is an array of n points, where n = len(plane).
            the body of this method is executed for every step.
            """
            self.log.debug("example plot")
            if step >= self.steps - 2:
                return

            color = random.choice([Colors.white, Colors.red,
                                   Colors.green, Colors.blue])
            plane[0] = color(self._DATA[step])

            if self._DATA[step] in [" ", "!"]:
                return

            plane[1:] = [color(txt) for txt in self._DATA[1:]]

            # self.machine.delay = 0.5

    machine = Machine(HelloWorldPlot, delay=0.1)
    machine.run()
