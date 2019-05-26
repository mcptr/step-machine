from machine import Machine, Plot, Colors


class MyPlot(Plot):
    width = 16
    steps = 4
    copies = 4
    spacing = 1
    default_color = Colors.BLUE

    def plot_pattern_1(self, plane, loop, step, *args, **kwargs):
        plane[step] = Colors.white("@")
        plane[-step - 1] = "@"

    def plot_pattern_2_left(self, plane, loop, step, *args, **kwargs):
        if step == 0:
            plane[1] = Colors.orange("+")
        elif step == 1:
            plane[2] = Colors.orange("+")
        elif step == 2:
            plane[3] = Colors.orange("+")
        elif step == 3:
            plane[4] = Colors.orange("+")

        if step and step < 4:
            plane[0] = Colors.red("*")

    def plot_pattern_2_right(self, plane, loop, step, *args, **kwargs):
        if step == 0:
            plane[-2] = Colors.orange("+")
        elif step == 1:
            plane[-3] = Colors.orange("+")
        elif step == 2:
            plane[-4] = Colors.orange("+")
        elif step == 3:
            plane[-5] = Colors.orange("+")

        if step and step < 4:
            plane[-1] = Colors.red("*")

    def plot_middle(self, plane, loop, step, *args, **kwargs):
        size = len(plane)
        middle = int(size / 2)

        if step % 2 == 0 and middle > 0:
            plane[middle] = Colors.green("\\")
            plane[middle - 1] = Colors.green("/")
        else:
            plane[middle] = Colors.green("/")
            plane[middle - 1] = Colors.green("\\")

    def plot_binding(self, plane, loop, step, *args, **kwargs):
        return
        # if step == 0:
        #     plane[-1] = "\\"
        # elif step == 1:
        #     plane[-3] = "+"
        # elif step == 2:
        #     plane[-4] = "+"
        # elif step == 3:
        #     plane[-5] = "+"

    def __call__(self, plane, loop, step, *args, **kwargs):
        self.plot_pattern_1(plane, loop, step, *args, **kwargs)
        self.plot_pattern_2_left(plane, loop, step, *args, **kwargs)
        self.plot_middle(plane, loop, step, *args, **kwargs)
        self.plot_pattern_2_right(plane, loop, step, *args, **kwargs)
        self.plot_binding(plane, loop, step, *args, **kwargs)


if __name__ == "__main__":
    machine = Machine(MyPlot, delay=0.1)
    machine.run()
