import numpy as np
from constants import STATES

class MovementHandler:
    def __init__(self, numpoints, amount_of_movement):
        self.numpoints = numpoints
        self.amount_of_movement = amount_of_movement
        self.current_stages_of_individuals = np.zeros(self.numpoints).astype("int")

    def update_positions(self, xy, current_stages_of_individuals):
        mobile_individuals = np.expand_dims((current_stages_of_individuals != STATES["immobilized"]).astype(int), 1)
        xy += self.amount_of_movement * mobile_individuals * (np.random.random((self.numpoints, 2)) - 0.5) 
        return xy