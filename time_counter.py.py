

class TransitionManager:

    def __init__(self, num_points):

        self.num_points = num_points

        self.transition_times = {
            "infected-contagious": {"mean": 20, "std": 2},
            "contagious-diagnosis": {"mean": 20, "std": 2},
            "diagnosis-immobilized": {"mean" : 5, "std": 2},
            "immobilized-recovered": {"mean" : 50, "std": 2}
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
        transition_array = np.zeros((self.num_points , self.number_of_transitions))
        for i in range(1, self.number_of_transitions):

            # get distribution parameters
            mean = self.transition_times[ self.num_2_transition [i] ] ["mean"]
            std = self.transition_times[ self.num_2_transition [i] ] ["std"]
            
            # sample transition times from distribution
            transition_array[: , i] = std * np.random.randn(self.num_points) + mean
        
        self.transition_times = transition_array


    def update_stages_of_desease(self, current_stages_of_individuals):
        """ updates the stages of the desease"""

        # updates the stages of the individuals
        new_stages_of_individuals, indicies_that_transitioned_to_next_stage = self.update_stages(current_stages_of_individuals)

        # increments the time counter for individuals, and reboots it if a transition occured
        if len(indicies_of_counters_to_reboot) > 0
            self.time_counters[indicies_of_counters_to_reboot] = 0
        self.time_counters += 1

        return new_stages_of_individuals


    def update_stages(self, current_stages_of_individuals):
        """updates the stages of the desease for all individuals, using the transition times
        
        Arguments:
            current_stages_of_individuals {[np.ndarray]} -- the current stages of all individuals
        
        Returns:
            [np.ndarray, np.ndarray] -- [the new stages of the individuals, the indicies for which these changes happened]
        """
        # get the relavent transition times for each individual
        current_stages_of_individuals_ = np.expand_dims(current_stages_of_individuals, 1)
        relavent_transition_times = self.transition_times[stagecurrent_stages_of_individuals_s_of_individuals_ ]

        # find transitions to apply
        transitions_to_apply = (self.time_counters > relavent_transition_times).int()

        # apply transitions and get the indicies which they occurs in
        new_stages_of_individuals = current_stages_of_individuals + transitions_to_apply
        indicies_that_transitioned_to_next_stage = np.nonzero(transitions_to_apply) [0] 

        return new_stages_of_individuals, indicies_that_transitioned_to_next_stage




def test_transition_manager():
    transition_manager = TransitionManager()


if __name__ == '__main__':
    test_transition_manager()