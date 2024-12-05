import numpy as np

class DiseaseStateHandler:

    def __init__(self, num_points):
        self.num_points = num_points
        self.transition_times = {
            "infected-contagious": {"mean": 20, "std": 5},
            "contagious-diagnosis": {"mean": 50, "std": 5},
            "diagnosis-immobilized": {"mean" : 5, "std": 2},
            "immobilized-recovered": {"mean" : 100, "std": 5}
        }
        self.number_of_transitions = len(self.transition_times)
        self.time_counters = np.zeros(num_points)
        self._set_transition_dicts()
        self._sample_transition_times_from_distribution()


    def _set_transition_dicts(self):
        """ initializes the transition dicts"""
        self.transition_2_num = {
            "infected-contagious": 1,
            "contagious-diagnosis": 2,
            "diagnosis-immobilized": 3,
            "immobilized-recovered": 4
        }

        self.num_2_transition = {
            1 : "infected-contagious",
            2 : "contagious-diagnosis",
            3 : "diagnosis-immobilized",
            4 : "immobilized-recovered",
        }

    def _sample_transition_times_from_distribution(self):
        """ samples the transition times for all individuals, and saves in self.transition_times """
        transition_array = np.zeros((self.num_points , self.number_of_transitions + 2))
        for i in range(1, self.number_of_transitions + 1):

            # get distribution parameters
            mean = self.transition_times[ self.num_2_transition [i] ] ["mean"]
            std = self.transition_times[ self.num_2_transition [i] ] ["std"]
            
            # sample transition times from distribution
            transition_array[: , i] = std * np.random.randn(self.num_points) + mean
        
        self.transition_times = transition_array

    def _update_stages(self, current_stages_of_individuals):
        current_stages_of_individuals = current_stages_of_individuals.astype("int") 
        relavent_transition_times = np.array([self.transition_times[i, current_stages_of_individuals[i] ] for i in range(self.num_points)])

        # find transitions to apply
        transitions_to_apply = (current_stages_of_individuals != 0) * (self.time_counters > relavent_transition_times).astype("int")

        # apply transitions and get the indicies which they occurs in
        new_stages_of_individuals = current_stages_of_individuals + transitions_to_apply

        # make sure we don't pass the maximum allows stage for the disease
        new_stages_of_individuals = np.minimum(new_stages_of_individuals, 5) 
        indicies_that_transitioned_to_next_stage = np.nonzero(transitions_to_apply) [0] 

        return new_stages_of_individuals, indicies_that_transitioned_to_next_stage

    def reset_time_counters(self, new_cases_idx):
        self.time_counters[new_cases_idx] = 0

    def __call__(self, current_stages_of_individuals):
        # updates the stages of the individuals
        new_stages_of_individuals, indicies_that_transitioned_to_next_stage = self._update_stages(current_stages_of_individuals)

        # increments the time counter for individuals, and reboots it if a transition occured
        if (len(indicies_that_transitioned_to_next_stage) > 0):
            self.time_counters[indicies_that_transitioned_to_next_stage] = 0
        self.time_counters += 1

        return new_stages_of_individuals
