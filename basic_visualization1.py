import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

RADIUS_OF_INFECTION = 1
PROBABILITY_OF_INFECTION = 0.1
SIZE = 0.2
MOVEMENT_COEFFICIENT = 0.2
INITIAL_BOX_SIZE = 20
numpoints = 300


def get_status_colors():
    """creates and returns a dict with the colors for the different statuses of the balls
    
    Returns:
        [dict] -- a dict for the status colors of the balls:
                    keys are: [not_infected, infected, contagious, sick-immobilized, immune]
    """
    colors = {
        "not_infected" : 0.3,
        "infected" : 0.7,
        "contagious" : 0.8,
        "diagnosis": 0.85,
        "immobilized" : 0.9,
        "recovered" : 0.5,
    }
    return colors


def get_status2num_dict():
    """[summary]
    
    Returns:
        [type] -- [description]
    """

    status2num = {
        "not_infected" : 0,
        "infected" : 1,
        "contagious" : 2,
        "diagnosis": 3,
        "immobilized" : 4,
        "recovered" : 5,
    }
    return status2num


def get_num2status_dict():
    """[summary]
    
    Returns:
        [type] -- [description]
    """
    status2num = get_status2num_dict()
    num2status = {}
    for key, val in status2num.items():
        num2status[val] = key

    return num2status


def get_transition_times():
    """[summary]
    
    Returns:
        [dict] -- the transition time between different stages of the desease 
    """
    transition_times = {
        "infected-contagious": {"mean": 1, "std": 2},
        "contagious-diagnosis": {"mean": 1, "std": 2},
        "diagnosis-immobilized": {"mean" : 1, "std": 2},
        "infected-recovered": {"mean" : 1, "std": 2}
    }

    return transition_times


def get_movement_coefficient():
    """"samples the movement coefficient from a boltzman distribution
    how much each individual moves
    
    """


class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, numpoints=100, num_infected=5, max_num_steps=500):
        self.numpoints = numpoints
        self.stream = self.data_stream()

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, 
                                          init_func=self.setup_plot, blit=True)

        self.status_colors = get_status_colors()
        self.initialize_infected(num_infected)
        self.counter = 0
        self.max_num_steps = max_num_steps

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y, s, c = next(self.stream).T
        self.scat = self.ax.scatter(x, y, c=c, s=s, vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k")
        L = int(INITIAL_BOX_SIZE/2)
        self.ax.axis([-L, L, -L, L])
        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,


    def data_stream(self):
        """Generate a random walk (brownian motion). Data is scaled to produce
        a soft "flickering" effect."""
        # xy = (np.random.random((self.numpoints, 2))-0.5)*10
        # sizes = 0.3*np.ones(self.numpoints)
        # colors = self.status_colors['not_infected']*np.ones(self.numpoints)

        xy, sizes, colors = self.initialize_data_stream()

        while True:
            xy += MOVEMENT_COEFFICIENT * (np.random.random((self.numpoints, 2)) - 0.5)
            self.update_status(xy)
            colors = self.update_colors()
            # self.counter += 1
            # if self.counter > self.max_num_steps:
            #     break

            yield np.c_[xy[:,0], xy[:,1], sizes, colors]


    def update_colors(self):

        infected = np.zeros(self.numpoints)
        infected[self.identities_of_infected] = 1

        colors = infected*self.status_colors['infected'] + (1-infected)*self.status_colors['not_infected']
        return colors



    def initialize_infected(self, num_infected):
        """ initializes the infected matrix with the number of infected individuals"""

        self.infected_matrix = np.zeros((self.numpoints,self.numpoints))
        self.identities_of_infected = np.random.randint(0, self.numpoints, num_infected)

        # set the rows of the infected to 1
        self.infected_matrix[self.identities_of_infected, :] = 1


    def update_status(self, xy):

        # find all individuals that are within radius of infection
        x = np.expand_dims(xy[:,0] , 1)
        y = np.expand_dims(xy[:,1] , 1)
        adjacency_matrix = np.sqrt((x - x.T)**2 + (y - y.T)**2 )
        within_radius = (adjacency_matrix < RADIUS_OF_INFECTION)

        # find individuals that are within this radius with another infected individual
        at_risk_of_infection = within_radius * self.infected_matrix

        # find all individuals that should probabalistically get infected  (with or without contact with another infected)
        should_get_infected = ( np.random.rand(self.numpoints, self.numpoints) < PROBABILITY_OF_INFECTION)

        # find newly infected that are within the infection radious
        newly_infected = should_get_infected * at_risk_of_infection

        # save the identities of the newly infected
        identities_of_newly_infected = np.nonzero( np.sum(newly_infected,0) ) [0]

        # update who is infected
        self.update_who_is_infected(identities_of_newly_infected)


    def update_who_is_infected(self, identities_of_newly_infected):

        # create helper vector to prevent overlaps
        already_infected, newly_infected = np.zeros(self.numpoints), np.zeros(self.numpoints)
        already_infected[self.identities_of_infected] = 1
        newly_infected[identities_of_newly_infected] = 1

        # update identities of infected
        updated_infected = np.logical_or(already_infected, newly_infected)
        self.identities_of_infected = np.nonzero(updated_infected)[0]

        # update infected matrix
        self.infected_matrix = np.zeros_like(self.infected_matrix)
        self.infected_matrix[self.identities_of_infected, :] = 1


    def initialize_data_stream(self):
        """initializes he sizes positions and sizes and statuses of the balls
        
        Returns:
            [np.ndarray, np.ndarray, np.ndarray] -- the positions, sizes and colors of the balls, in that corresponding order
        """
        xy = (np.random.random((self.numpoints, 2))-0.5)*INITIAL_BOX_SIZE
        sizes = SIZE*np.ones(self.numpoints)
        colors = self.status_colors['not_infected']*np.ones(self.numpoints)

        return xy, sizes, colors 


    def update(self, i):
        """Update the scatter plot."""
        data = next(self.stream)

        # Set x and y data...
        self.scat.set_offsets(data[:, :2])
        # Set sizes...
        self.scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)
        # Set colors..
        self.scat.set_array(data[:, 3])

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,


if __name__ == '__main__':
    a = AnimatedScatter(numpoints=numpoints)
    plt.show()