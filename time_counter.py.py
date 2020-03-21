

class DeseaseStageTransitions:

    def __init__(self):

        self.transition_times = {
            "infected-contagious": {"mean": 20, "std": 2},
            "contagious-diagnosis": {"mean": 20, "std": 2},
            "diagnosis-immobilized": {"mean" : 5, "std": 2},
            "immobilized-recovered": {"mean" : 50, "std": 2}
        }

        self.transition_2_num = {
            "infected-contagious": 0,
            "contagious-diagnosis": 1,
            "diagnosis-immobilized": 2,
            "immobilized-recovered": 3
        }

        self.num_2_transition = {
            0 : "infected-contagious",
            1 : "contagious-diagnosis",
            2 : "diagnosis-immobilized",
            3 : "immobilized-recovered",
        }
    
    def get_transition_times(self):
        """returns the parameters for the distribution of transitions, between different stages of the desease
        
        Returns:
            [dict] -- the transition time between different stages of the desease 
                        keys = [infected-contagious, contagious-diagnosis, diagnosis-immobilized, immobilized-recovered]
        """
        return self.transition_times

    def get_transition_2_num_dict(self):
        """returns a dict whith keys=transition names, and values=transition num id
        
        Returns:
            [dict] -- a dict to covert the transition id to its corresponding number id
                        keys = [infected-contagious, contagious-diagnosis, diagnosis-immobilized, immobilized-recovered]
        """
        return self.transition_2_num


    def get_transition_2_num_dict(self):
        """returns a dict whith keys=transition num id, and values=transition names
        
        Returns:
            [dict] -- a dict to covert the transition number id to its corresponding name
                        keys = [0,1,2,3]
        """
        return self.num_2_transition


    def sample_transition_times(self):

        
    


class TimeCounter:


    def __init__(self, num_points):

        self.num_points = num_points
        self.time_counters = np.zeros(num_points)
        self.transition_times = get_transition_times()
        

    def get_time_counters_of_all_individuals(self):


    def get_transition_times(self):
        time_counters = self.get_time_counters_of_all_individuals()
        transition_times = self.get_transition_times()