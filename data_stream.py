from constants import STATES, COLORS, SIZE, BOX_SIZE
import numpy as np
from infection_handler import InfectionHandler
from movement_handler import MovementHandler
class DataStream:
    def __init__(self, numpoints, num_infected, amount_of_movement, radius_of_possible_infection, probability_of_getting_infected):
        self.numpoints = numpoints
        self.movement_handler = MovementHandler(numpoints, amount_of_movement)
        self.infection_handler = InfectionHandler(numpoints, num_infected, radius_of_possible_infection, probability_of_getting_infected)
        self.stream = self.data_stream()

    def initialize_data_stream(self):
        xy = (np.random.random((self.numpoints, 2)) - 0.5) * BOX_SIZE
        sizes = SIZE * np.ones(self.numpoints)
        colors = COLORS['not_infected'] * np.ones(self.numpoints)
        return xy, sizes, colors 

    def data_stream(self):
        xy, sizes, colors = self.initialize_data_stream()
        while True:
            disease_states = self.infection_handler(xy)
            xy = self.movement_handler(xy, disease_states)
            colors = self.update_colors(disease_states)
            yield xy, colors

    def update_colors(self, disease_states):
        colors = np.zeros(self.numpoints)
        for stage_name, stage_num in STATES.items():
            colors[disease_states == stage_num] = COLORS[stage_name]
        return colors
    
    def __next__(self):
        return next(self.stream)