import numpy as np

from utils.constants import STATES


class MovementHandler:
    def __init__(self, numpoints: int, amount_of_movement: float) -> None:
        self.numpoints = numpoints
        self.amount_of_movement = amount_of_movement
        self.current_stages = np.zeros(self.numpoints).astype("int")

    def __call__(self, xy: np.ndarray, current_stages: np.ndarray) -> np.ndarray:
        mobile_individuals = np.expand_dims(
            (current_stages != STATES["immobilized"]).astype(int), 1
        )
        xy += (
            self.amount_of_movement
            * mobile_individuals
            * (np.random.random((self.numpoints, 2)) - 0.5)
        )
        return xy
