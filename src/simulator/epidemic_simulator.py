from typing import Tuple

import numpy as np

from handlers.infection_handler import InfectionHandler
from handlers.movement_handler import MovementHandler
from utils.constants import BOX_SIZE


class EpidemicSimulator:
    def __init__(
        self,
        numpoints: int,
        num_infected: int,
        amount_of_movement: float,
        radius_of_possible_infection: float,
        probability_of_getting_infected: float,
    ) -> None:
        self.numpoints = numpoints
        self.movement_handler = MovementHandler(numpoints, amount_of_movement)
        self.infection_handler = InfectionHandler(
            numpoints,
            num_infected,
            radius_of_possible_infection,
            probability_of_getting_infected,
        )
        self.stream = self.data_stream()

    def initialize_data_stream(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        xy = (np.random.random((self.numpoints, 2)) - 0.5) * BOX_SIZE
        disease_states = np.zeros(self.numpoints)
        return xy, disease_states

    def data_stream(self) -> Tuple[np.ndarray, np.ndarray]:
        xy, _ = self.initialize_data_stream()
        while True:
            disease_states = self.infection_handler(xy)
            xy = self.movement_handler(xy, disease_states)
            yield xy, disease_states

    def __next__(self) -> Tuple[np.ndarray, np.ndarray]:
        return next(self.stream)
