import numpy as np
from typing import Optional, Set
from handlers.disease_state_handler import DiseaseStateHandler


class InfectionHandler:
    def __init__(
        self,
        numpoints: int,
        num_initial_infected: int,
        infection_radius: float,
        probability_of_getting_infected: float,
    ) -> None:
        self.numpoints = numpoints
        self.infection_radius_squared = infection_radius ** 2  # Pre-compute square
        self.probability_of_getting_infected = probability_of_getting_infected
        
        self.identities_of_infected = np.random.choice(
            self.numpoints, 
            size=num_initial_infected, 
            replace=False
        )
        self.current_stages = np.zeros(self.numpoints).astype(int)
        self.current_stages[self.identities_of_infected] = 1
        self.identities_of_recovered: Set[int] = set()
        self.disease_state_handler = DiseaseStateHandler(numpoints)
        self._distance_cache: Optional[np.ndarray] = None
        self._last_xy: Optional[np.ndarray] = None

    def get_newly_infected(self, xy: np.ndarray) -> np.ndarray:
        distances = np.sum((xy[None, :, :] - xy[:, None, :]) ** 2, axis=2)
        infected_distances = distances[self.identities_of_infected]
        at_risk = infected_distances < self.infection_radius_squared
        random_values = np.random.rand(*at_risk.shape)
        will_infect = random_values < self.probability_of_getting_infected
        newly_infected = np.unique(np.where(at_risk & will_infect)[1])
        
        mask = np.ones(len(newly_infected), dtype=bool)
        for idx, individual in enumerate(newly_infected):
            if (individual in self.identities_of_recovered or 
                individual in self.identities_of_infected):
                mask[idx] = False
        
        return newly_infected[mask]

    def _update_infected(self, xy: np.ndarray) -> None:
        newly_infected = self.get_newly_infected(xy)
        
        if len(newly_infected) > 0:
            self.identities_of_infected = np.append(
                self.identities_of_infected, 
                newly_infected
            )
            self.disease_state_handler.reset_time_counters(newly_infected)
            self.current_stages[newly_infected] = 1
        
    def _update_recovered(self) -> None:
        recovered_mask = self.current_stages == 5
        new_recovered = set(np.where(recovered_mask)[0]) - self.identities_of_recovered
        self.identities_of_recovered.update(new_recovered)
        
        if new_recovered:
            mask = np.ones(len(self.identities_of_infected), dtype=bool)
            for idx, individual in enumerate(self.identities_of_infected):
                if individual in new_recovered:
                    mask[idx] = False
            self.identities_of_infected = self.identities_of_infected[mask]

    def __call__(self, xy: np.ndarray) -> np.ndarray:
        self._update_infected(xy)
        self._update_recovered()
        self.current_stages = self.disease_state_handler(self.current_stages)
        return self.current_stages