import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from infection_handler import InfectionHandler
from constants import STATES, COLORS, SIZE, BOX_SIZE
from movement_handler import MovementHandler

class CovidSimulator(object):
    def __init__(self, numpoints=100, num_infected=5, max_num_steps=500, 
                amount_of_movement=0.15, radius_of_possible_infection=1, 
                probability_of_getting_infected=0.1):

        self.numpoints = numpoints
        self.stream = self.data_stream()
        self.amount_of_movement = amount_of_movement
        self.radius_of_possible_infection = radius_of_possible_infection
        self.probability_of_getting_infected = probability_of_getting_infected
        self.counter = 0
        self.max_num_steps = max_num_steps
        self.num_infected = num_infected
        self.current_stages_of_individuals = np.zeros(self.numpoints).astype("int")
        self.fig, self.ax = plt.subplots()
        self.scat = None
        self.handles = None
        self.labels = None
        self.infected_matrix = None
        # self.identities_of_infected = None
        # self.identities_of_recovered = None

        # self.infected_matrix = np.zeros((self.numpoints,self.numpoints))
        # self.current_stages_of_individuals = np.zeros(self.numpoints).astype("int")
        # self.identities_of_infected = np.random.randint(0, self.numpoints, num_infected)

        # set the rows of the infected to 1
        # self.infected_matrix[self.identities_of_infected, :] = 1
        # self.current_stages_of_individuals[self.identities_of_infected] = 1

        # self.disease_state_handler = DiseaseStateHandler(numpoints)
        self.movement_handler = MovementHandler(numpoints, amount_of_movement)
        self.infection_handler = InfectionHandler(numpoints, num_infected, radius_of_possible_infection, probability_of_getting_infected)
        # self.initialize_infected(num_infected)

        self.stream = self.data_stream()
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

    # TODO move this to infection mamanger
    # def initialize_infected(self, num_infected):
    #     self.infected_matrix = np.zeros((self.numpoints,self.numpoints))
    #     self.current_stages_of_individuals = np.zeros(self.numpoints) #.astype("int")
    #     self.identities_of_infected = np.random.randint(0, self.numpoints, num_infected)
    #     self.infected_matrix[self.identities_of_infected, :] = 1
    #     self.current_stages_of_individuals[self.identities_of_infected] = 1

    def initialize_data_stream(self):
        xy = (np.random.random((self.numpoints, 2)) - 0.5) * BOX_SIZE
        sizes = SIZE * np.ones(self.numpoints)
        colors = COLORS['not_infected'] * np.ones(self.numpoints)
        return xy, sizes, colors 

    def data_stream(self):
        xy, sizes, colors = self.initialize_data_stream()
        while True:
            disease_states = self.infection_handler(xy)
            # disease_states = self.disease_state_handler(newly_infected)
            # disease_states = self.update_status(xy)
            xy = self.movement_handler(xy, disease_states)
            colors = self.update_colors(disease_states)
            # yield np.c_[xy[:,0], xy[:,1], sizes, colors]
            yield xy, sizes, colors

    # def update_positions(self, xy):
    #     mobile_individuals = np.expand_dims((self.current_stages_of_individuals != STATES["immobilized"]).astype(int), 1)
    #     xy += self.amount_of_movement * mobile_individuals * (np.random.random((self.numpoints, 2)) - 0.5) 
    #     return xy

    def update_colors(self, disease_states):
        colors = np.zeros(self.numpoints)
        for stage_name, stage_num in STATES.items():
            colors[disease_states == stage_num] = COLORS[stage_name]
            # colors += COLORS[stage_name] * (self.current_stages_of_individuals == stage_num)
        return colors

    # def get_newly_infected(self, xy):
    #     adjacency_matrix = ((xy[None, :, :] - xy[:, None, :]) ** 2).sum(2)
    #     within_radius = (adjacency_matrix < self.radius_of_possible_infection ** 2)
    #     at_risk_of_infection = within_radius * self.infected_matrix
    #     should_get_infected = (np.random.rand(self.numpoints, self.numpoints) < self.probability_of_getting_infected)
    #     newly_infected_matrix = should_get_infected * at_risk_of_infection
    #     identities_of_newly_infected = np.where(np.sum(newly_infected_matrix, 0))[0]
    #     return identities_of_newly_infected
    
    # def update_status(self, xy):
    #     self.current_stages_of_individuals = self.update_who_is_infected(xy)
    #     self.current_stages_of_individuals = self.disease_state_manager.update_stages_of_disease(self.current_stages_of_individuals)
    #     return self.current_stages_of_individuals
    
    # TODO externalize this to a new class which handles infections - InfectionManager
    # def update_who_is_infected(self, xy):
    #     identities_of_newly_infected = self.get_newly_infected(xy)
    #     # TODO pull this from memory
    #     already_infected, newly_infected = np.zeros(self.numpoints), np.zeros(self.numpoints)
    #     already_infected[self.identities_of_infected] = 1
    #     newly_infected[identities_of_newly_infected] = 1

    #     # update identities of infected
    #     # TODO make this more efficient
    #     updated_infected = np.logical_or(already_infected, newly_infected)
    #     self.identities_of_infected = np.nonzero(updated_infected)[0]
    #     self.identities_of_recovered = set(np.nonzero(self.current_stages_of_individuals == 5)[0])
    #     self.identities_of_infected = np.array([idx for idx in self.identities_of_infected if idx not in self.identities_of_recovered ]).astype("int")
    #     updated_infected = np.zeros(self.numpoints)
    #     updated_infected[self.identities_of_infected] = 1

    #     # update infected matrix
    #     self.infected_matrix = np.zeros_like(self.infected_matrix)
    #     self.infected_matrix[self.identities_of_infected, :] = 1

    #     # update 
    #     # TODO change non zero to where in multiple places
    #     new_cases = (updated_infected - already_infected).copy().astype("int")
    #     self.disease_state_manager.time_counters[np.nonzero(new_cases)[0]] = 0
    #     self.current_stages_of_individuals += new_cases
    #     return self.current_stages_of_individuals

    def update(self, i):
        """Update the scatter plot."""
        xy, sizes, colors = next(self.stream)
        # self.scat.set_offsets(data[:, :2])
        # self.scat.set_sizes(data[:, 2])
        # self.scat.set_array(data[:, 3])

        self.scat.set_offsets(xy)
        self.scat.set_sizes(sizes)
        self.scat.set_array(colors)
        return self.scat,


if __name__ == '__main__':
    CovidSimulator(numpoints=300)
    plt.show()