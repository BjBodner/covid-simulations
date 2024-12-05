import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from constants import STATES, COLORS, SIZE, BOX_SIZE
from data_stream import DataStream

class StreamlitCovidSimulator:
    def __init__(self, numpoints=100, num_infected=5,
                 amount_of_movement=0.15, radius_of_possible_infection=1,
                 probability_of_getting_infected=0.1):
        self.numpoints = numpoints
        self.stream = DataStream(numpoints, num_infected, amount_of_movement, 
                               radius_of_possible_infection, probability_of_getting_infected)
        
    def setup_plot(self):
        # Create figure with adjusted size to accommodate legend
        plt.style.use('fast')  # Use fast style for better performance
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Get initial data
        xy, c = next(self.stream)

        # Create scatter plot
        scat = ax.scatter(xy[:, 0], xy[:, 1], c=c, s=SIZE * np.ones(self.numpoints), vmin=0, vmax=1, 
                         cmap="jet", edgecolor="k", alpha=0.9, rasterized=True)
        
        # Set axis limits
        L = int(BOX_SIZE / 2)
        ax.axis([-L, L, -L, L])
        
        # remove the ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Add legend outside the plot
        handles, labels = self.get_handles_for_legend()
        ax.legend(handles, labels, 
                 loc='center left', 
                 bbox_to_anchor=(1.05, 0.5),
                 title="Disease Stages", 
                 fontsize=12)
        
        # Adjust layout to prevent legend cutoff
        plt.tight_layout()
        ax.set_axis_off()
        return fig, scat, xy, c
    
    def get_handles_for_legend(self):
        num_states = len(STATES)
        colors = np.zeros(num_states)
        x = np.ones(num_states) * 2 * BOX_SIZE # dummy values for x and y out of bounds
        y = x.copy()
        color_names = [None] * num_states
        
        for status, num in STATES.items():
            colors[num] = COLORS[status]
            color_names[num] = status

        scat = plt.scatter(x, y, c=colors, s=SIZE * np.ones(num_states), 
                         vmin=0, vmax=1, label=color_names, cmap="jet", edgecolor="k")
        handles, labels = scat.legend_elements(prop="colors", alpha=0.6)

        handle_labels = []
        for i in range(len(labels)):
            handle_color = float(labels[i].split('{')[-1].split('}')[0])
            idx = np.argmin((handle_color - colors)**2)
            handle_labels.append(color_names[idx])

        return handles, handle_labels

def main():
    st.set_page_config(layout="centered")  # Use wide layout for better performance
    st.title("COVID-19 Spread Simulator")
    
    # Sidebar controls
    st.sidebar.header("Simulation Parameters")
    numpoints = st.sidebar.slider("Number of People", 50, 500, 100)
    num_infected = st.sidebar.slider("Initial Infected", 1, 20, 5)
    amount_of_movement = st.sidebar.slider("Movement Amount", 0.0, 1.0, 0.15)
    radius_of_infection = st.sidebar.slider("Infection Radius", 0.1, 5.0, 1.0)
    infection_probability = st.sidebar.slider("Infection Probability", 0.0, 1.0, 0.1)
    
    # Add speed control
    speed = st.sidebar.slider("Simulation Speed", 0.01, 0.5, 0.1, 
                            help="Lower values = faster simulation")
    # Initialize simulator
    simulator = StreamlitCovidSimulator(
        numpoints=numpoints,
        num_infected=num_infected,
        amount_of_movement=amount_of_movement,
        radius_of_possible_infection=radius_of_infection,
        probability_of_getting_infected=infection_probability
    )
    
    # Create placeholder for the plot
    # plot_placeholder = st.empty()
    if 'plot_placeholder' not in st.session_state:
        st.session_state.plot_placeholder = st.empty()
    if 'plot_components' not in st.session_state:
        st.session_state.plot_components = st.session_state.simulator.setup_plot()
        
    # Create initial plot
    fig, scat, xy, c = simulator.setup_plot()
    


    # Main simulation loop
    running = st.button("Start/Stop Simulation")
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
    
    if running:
        st.session_state.simulation_running = not st.session_state.simulation_running
    
    while st.session_state.simulation_running:
        # Update data
        # xy, s, c = next(simulator.stream)
        xy += np.random.randn(numpoints, 2) * amount_of_movement
        scat.set_offsets(xy)
        # scat.set_sizes(s)
        scat.set_array(c)
        
        # Update plot in Streamlit
        plot_placeholder.pyplot(fig, use_container_width=False)
        
        # Add a small delay to control animation speed
        # time.sleep(0.01)
        # time.sleep(speed)

        # Rerun the app
        # st.rerun()

if __name__ == "__main__":
    main()