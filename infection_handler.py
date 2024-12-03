import numpy as np
from disease_state_handler import DiseaseStateHandler

class InfectionHandler:
    def __init__(self, numpoints, num_initial_infected, infection_radius, probability_of_getting_infected):
        self.numpoints = numpoints
        self.infection_radius = infection_radius
        self.probability_of_getting_infected = probability_of_getting_infected
        self.infected_matrix = np.zeros((self.numpoints,self.numpoints))
        self.current_stages_of_individuals = np.zeros(self.numpoints) #.astype("int")
        self.identities_of_infected = np.random.randint(0, self.numpoints, num_initial_infected)
        self.infected_matrix[self.identities_of_infected, :] = 1
        self.current_stages_of_individuals[self.identities_of_infected] = 1
        self.identities_of_recovered = set()
        self.disease_state_handler = DiseaseStateHandler(numpoints)

    def get_newly_infected(self, xy):
        adjacency_matrix = ((xy[None, :, :] - xy[:, None, :]) ** 2).sum(2)
        within_radius = (adjacency_matrix < self.infection_radius ** 2)
        at_risk_of_infection = within_radius * self.infected_matrix
        should_get_infected = (np.random.rand(self.numpoints, self.numpoints) < self.probability_of_getting_infected)
        newly_infected_matrix = should_get_infected * at_risk_of_infection
        identities_of_newly_infected = np.where(np.sum(newly_infected_matrix, 0))[0]
        return identities_of_newly_infected
    
    def update_with_new_infection(self, xy):
            identities_of_newly_infected = self.get_newly_infected(xy)
            # TODO pull this from memory
            already_infected, newly_infected = np.zeros(self.numpoints), np.zeros(self.numpoints)
            already_infected[self.identities_of_infected] = 1
            newly_infected[identities_of_newly_infected] = 1

            # update identities of infected
            # TODO make this more efficient
            updated_infected = np.logical_or(already_infected, newly_infected)
            self.identities_of_infected = np.nonzero(updated_infected)[0]
            self.identities_of_recovered = set(np.nonzero(self.current_stages_of_individuals == 5)[0])
            self.identities_of_infected = np.array([idx for idx in self.identities_of_infected if idx not in self.identities_of_recovered ]).astype("int")
            updated_infected = np.zeros(self.numpoints)
            updated_infected[self.identities_of_infected] = 1

            # update infected matrix
            self.infected_matrix = np.zeros_like(self.infected_matrix)
            self.infected_matrix[self.identities_of_infected, :] = 1

            # update 
            # TODO change non zero to where in multiple places
            new_cases = (updated_infected - already_infected).copy().astype("int")
            self.disease_state_handler.reset_time_counters(np.nonzero(new_cases)[0])
            self.current_stages_of_individuals += new_cases
            return self.current_stages_of_individuals
    

    def __call__(self, xy):
        disease_states = self.update_with_new_infection(xy)
        disease_states = self.disease_state_handler(disease_states)
        self.current_stages_of_individuals = disease_states
        return self.current_stages_of_individuals