import numpy as np
from typing import Tuple
from collections import OrderedDict

TRANSITION_TIMES = OrderedDict(
    infected_contagious={"mean": 20, "std": 5},
    contagious_diagnosis={"mean": 50, "std": 5},
    diagnosis_immobilized={"mean": 5, "std": 2},
    immobilized_recovered={"mean": 100, "std": 5},
)

class DiseaseStateHandler:
    def __init__(self, num_points: int) -> None:
        self.num_points = num_points
        self.number_of_transitions = len(TRANSITION_TIMES)
        self.time_counters = np.zeros(num_points)   
        self.transition_times = self._sample_transition_times()
        self.point_idx = np.arange(num_points)

    def _sample_transition_times(self) -> None:
        transition_array = np.zeros((self.num_points, self.number_of_transitions + 2))
        transition_array[:, 0] = np.inf # must be actively infected to transition
        for i, transition_params in enumerate(TRANSITION_TIMES.values()):
            transition_array[:, i + 1] = transition_params["mean"] + transition_params["std"] * np.random.randn(self.num_points)
        return transition_array

    def _update_stages(self, current_stages_of_individuals: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        relavent_transition_times = self.transition_times[self.point_idx, current_stages_of_individuals]
        transitions_to_apply = (self.time_counters > relavent_transition_times).astype(int)
        new_stages_of_individuals = np.minimum(current_stages_of_individuals + transitions_to_apply, 5)

        self.reset_time_counters(transitions_to_apply)
        return new_stages_of_individuals

    def reset_time_counters(self, reboot_idx: np.ndarray) -> None:
        if len(reboot_idx) > 0:
            self.time_counters[reboot_idx] = 0

    def __call__(self, current_stages_of_individuals: np.ndarray) -> np.ndarray:
        new_stages_of_individuals = self._update_stages(current_stages_of_individuals)
        self.time_counters += 1
        return new_stages_of_individuals
