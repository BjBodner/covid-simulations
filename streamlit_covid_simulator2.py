import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from infection_handler import InfectionHandler
from constants import STATES, COLORS, SIZE, BOX_SIZE
from movement_handler import MovementHandler
from data_stream import DataStream

class StreamlitCovidSimulator:
    def __init__(self, numpoints=100, num_infected=5,
                 amount_of_movement=0.15, radius_of_possible_infection=1,
                 probability_of_getting_infected=0.1):
        self.numpoints = numpoints
        self.stream = DataStream(numpoints, num_infected, amount_of_movement, 
                               radius_of_possible_infection, probability_of_getting_infected)
        
    def create_figure(self):
        # Get initial data
        xy, c = next(self.stream)
        s = SIZE * np.ones(self.numpoints)

        xy[:len(STATES), 0] = -BOX_SIZE * 2
        for i, color in enumerate(COLORS.values()):
            c[i] = color

        # Create traces for each state
        traces = []
        for state_name, state_num in STATES.items():
            mask = (c == COLORS[state_name])
            if np.any(mask):  # Only create trace if there are points in this state
                traces.append(
                    go.Scatter(
                        x=xy[mask, 0],
                        y=xy[mask, 1],
                        mode='markers',
                        name=state_name,
                        marker=dict(
                            size=SIZE,  # Use constant SIZE instead of s
                            color=COLORS[state_name],
                            line=dict(width=1, color='black')
                        )
                    )
                )
        
        # Create figure
        L = int(BOX_SIZE / 2)
        fig = go.Figure(data=traces)
        fig.update_layout(
            width=800,
            height=800,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.05
            ),
            xaxis=dict(
                range=[-L, L],
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                range=[-L, L],
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='white'
        )
        
        return fig, xy, c

def initialize_session_state():
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
    if 'needs_reset' not in st.session_state:
        st.session_state.needs_reset = False

def reset_simulation(numpoints, num_infected, amount_of_movement, radius_of_infection, infection_probability):
    st.session_state.simulator = StreamlitCovidSimulator(
        numpoints=numpoints,
        num_infected=num_infected,
        amount_of_movement=amount_of_movement,
        radius_of_possible_infection=radius_of_infection,
        probability_of_getting_infected=infection_probability
    )
    st.session_state.plot_components = st.session_state.simulator.create_figure()
    st.session_state.needs_reset = False

def main():
    st.set_page_config(layout="wide")
    st.title("COVID-19 Spread Simulator")
    
    initialize_session_state()
    
    # Create columns for control buttons
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Start/Stop"):
            st.session_state.simulation_running = not st.session_state.simulation_running
    
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

    # Apply button for parameter changes
    if st.sidebar.button("Apply Parameters"):
        st.session_state.needs_reset = True
        st.session_state.simulation_running = False
    
    # Initialize or reset simulator if needed
    if 'simulator' not in st.session_state or st.session_state.needs_reset:
        reset_simulation(numpoints, num_infected, amount_of_movement, 
                        radius_of_infection, infection_probability)
    
    # Create placeholder for the plot
    plot_placeholder = st.empty()
    
    # Get current plot components
    fig, xy, c = st.session_state.plot_components
    
    if st.session_state.simulation_running:
        # Update data
        xy, c = next(st.session_state.simulator.stream)
        
        # Update each trace with new data
        for i, state_name in enumerate(STATES.keys()):
            mask = (c == COLORS[state_name])
            if np.any(mask):
                try:
                    fig.data[i].x = xy[mask, 0]
                    fig.data[i].y = xy[mask, 1]
                except IndexError:
                    # If state doesn't exist yet, create new trace
                    fig.add_trace(
                        go.Scatter(
                            x=xy[mask, 0],
                            y=xy[mask, 1],
                            mode='markers',
                            name=state_name,
                            marker=dict(
                                size=SIZE,
                                color=COLORS[state_name],
                                line=dict(width=1, color='black')
                            )
                        )
                    )
    
    # Display plot
    plot_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Rerun if simulation is running
    if st.session_state.simulation_running:
        time.sleep(speed)
        st.rerun()

if __name__ == "__main__":
    main()