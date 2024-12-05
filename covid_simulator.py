import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from infection_handler import InfectionHandler
from constants import STATES, COLORS, SIZE, BOX_SIZE
from movement_handler import MovementHandler
from data_stream import DataStream

class CovidSimulator(object):
    def __init__(self, numpoints=100, num_infected=5,
                amount_of_movement=0.15, radius_of_possible_infection=1, 
                probability_of_getting_infected=0.1):

        self.numpoints = numpoints
        self.scat = None
        self.handles = None
        self.labels = None
        self.stream = DataStream(numpoints, num_infected, amount_of_movement, radius_of_possible_infection, probability_of_getting_infected)
        self.fig, self.ax = plt.subplots()
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, init_func=self.setup_plot, blit=True)

    # TODO move everything related to the plot to a new class - PlotManager
    def setup_plot(self):
        xy, s, c = next(self.stream)
        self.scat = self.ax.scatter(xy[:, 0], xy[:, 1], c=c, s=s, vmin=0, vmax=1, cmap="jet", edgecolor="k", alpha=0.9)
        L = int(BOX_SIZE / 2)
        self.ax.axis([-L, L, -L, L])
        self.handles, self.labels = self.get_handles_for_legend()
        self.ax.legend(self.handles, self.labels, loc="upper left", title="disease stages", fontsize=12)
        self.ax.set_zorder(-1)
        return self.scat, # intentional trailing comma

    def get_handles_for_legend(self):
        num_states = len(STATES)
        colors = np.zeros(num_states)
        x, y = np.arange(num_states), np.arange(num_states)
        color_names = [None] * num_states
        for status, num in STATES.items():
            colors[num] = COLORS[status]
            color_names[num] = status

        scat = plt.scatter(x, y, c=colors, s=SIZE * np.ones(num_states), vmin=0, vmax=1, label=color_names, cmap="jet", edgecolor="k")
        handles, labels =  scat.legend_elements(prop="colors", alpha=0.6)

        handle_labels = []
        for i in range(len(labels)):
            handle_color = float(labels[i].split('{')[-1].split('}')[0]) # TODO what is this?
            idx = np.argmin((handle_color - colors)**2)
            handle_labels.append(color_names[idx])

        return handles, handle_labels

    def update(self, i):
        """Update the scatter plot."""
        xy, sizes, colors = next(self.stream)
        self.scat.set_offsets(xy)
        self.scat.set_sizes(sizes)
        self.scat.set_array(colors)
        return self.scat,


if __name__ == '__main__':
    CovidSimulator(numpoints=300)
    plt.show()