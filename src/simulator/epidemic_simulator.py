from typing import Tuple

import numpy as np

from handlers.infection_handler import InfectionHandler
from handlers.movement_handler import MovementHandler
from utils.constants import BOX_SIZE, COLORS, STATES


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
        colors = COLORS["not_infected"] * np.ones(self.numpoints)
        return xy, colors

    def data_stream(self) -> Tuple[np.ndarray, np.ndarray]:
        xy, colors = self.initialize_data_stream()
        while True:
            disease_states = self.infection_handler(xy)
            xy = self.movement_handler(xy, disease_states)
            colors = self.update_colors(disease_states)
            yield xy, colors

    def update_colors(self, disease_states: np.ndarray) -> np.ndarray:
        colors = np.zeros(self.numpoints)
        for stage_name, stage_num in STATES.items():
            colors[disease_states == stage_num] = COLORS[stage_name]
        return colors

    def __next__(self) -> Tuple[np.ndarray, np.ndarray]:
        return next(self.stream)
