import numpy as np

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
        self.infection_radius_squared = infection_radius**2
        self.probability_of_getting_infected = probability_of_getting_infected
        self.infected_mask = np.zeros(numpoints, dtype=bool)
        initial_infected = np.random.choice(
            numpoints, size=num_initial_infected, replace=False
        )
        self.infected_mask[initial_infected] = True
        self.current_stages = np.zeros(numpoints, dtype=np.int32)
        self.current_stages[self.infected_mask] = 1
        self.recovered_mask = np.zeros(numpoints, dtype=bool)

        self.disease_state_handler = DiseaseStateHandler(numpoints)

    def get_newly_infected(self, xy: np.ndarray) -> np.ndarray:
        distances = np.sum((xy[None, :, :] - xy[:, None, :]) ** 2, axis=2)
        infected_distances = distances[self.infected_mask]
        at_risk = infected_distances < self.infection_radius_squared

        random_values = np.random.rand(*at_risk.shape)
        will_infect = random_values < self.probability_of_getting_infected

        potential_infections = at_risk & will_infect
        new_infections = np.any(potential_infections, axis=0)

        # Remove already infected or recovered individuals
        new_infections &= ~self.infected_mask & ~self.recovered_mask
        return new_infections

    def _update_infected(self, xy: np.ndarray) -> None:
        new_infections = self.get_newly_infected(xy)
        if np.any(new_infections):
            self.infected_mask |= new_infections
            self.disease_state_handler.reset_time_counters(np.where(new_infections)[0])
            self.current_stages[new_infections] = 1

    def _update_recovered(self) -> None:
        new_recovered = (self.current_stages == 5) & ~self.recovered_mask
        if np.any(new_recovered):
            # Add new recovered and remove recovered individuals from infected mask
            self.recovered_mask |= new_recovered
            self.infected_mask &= ~new_recovered

    def __call__(self, xy: np.ndarray) -> np.ndarray:
        self._update_infected(xy)
        self._update_recovered()
        self.current_stages = self.disease_state_handler(self.current_stages)
        return self.current_stages
