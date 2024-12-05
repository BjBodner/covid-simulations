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
        xy, c = next(self.stream)
        s = SIZE * np.ones(self.numpoints)

        xy[:len(STATES), 0] = -BOX_SIZE * 2 # Move legend points out of the plot
        for i, color in enumerate(COLORS.values()):
            c[i] = color

        traces = []
        for state_name, state_num in STATES.items():
            mask = (c == COLORS[state_name])
            if np.any(mask):
                traces.append(
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
    if 'parameters' not in st.session_state:
        st.session_state.parameters = {
            'numpoints': 100,
            'num_infected': 5,
            'amount_of_movement': 0.15,
            'radius_of_infection': 1.0,
            'infection_probability': 0.1
        }

def handle_parameter_change():
    # st.session_state.simulation_running = False
    st.session_state.simulator = StreamlitCovidSimulator(
        numpoints=st.session_state.parameters['numpoints'],
        num_infected=st.session_state.parameters['num_infected'],
        amount_of_movement=st.session_state.parameters['amount_of_movement'],
        radius_of_possible_infection=st.session_state.parameters['radius_of_infection'],
        probability_of_getting_infected=st.session_state.parameters['infection_probability']
    )
    st.session_state.plot_components = st.session_state.simulator.create_figure()

def main():
    st.set_page_config(layout="wide")
    st.title("COVID-19 Spread Simulator")
    
    initialize_session_state()
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Start/Stop"):
            st.session_state.simulation_running = not st.session_state.simulation_running
    
    st.sidebar.header("Simulation Parameters")
    
    # Use key parameter to trigger callback on change
    new_numpoints = st.sidebar.slider("Number of People", 50, 500, 
                                    st.session_state.parameters['numpoints'], 
                                    key='numpoints_slider')
    new_num_infected = st.sidebar.slider("Initial Infected", 1, 20, 
                                       st.session_state.parameters['num_infected'], 
                                       key='infected_slider')
    new_movement = st.sidebar.slider("Movement Amount", 0.0, 1.0, 
                                   st.session_state.parameters['amount_of_movement'], 
                                   key='movement_slider')
    new_radius = st.sidebar.slider("Infection Radius", 0.1, 5.0, 
                                 st.session_state.parameters['radius_of_infection'], 
                                 key='radius_slider')
    new_probability = st.sidebar.slider("Infection Probability", 0.0, 1.0, 
                                      st.session_state.parameters['infection_probability'], 
                                      key='probability_slider')
    
    speed_ = st.sidebar.slider("Simulation Speed", 10., 100., 80., 
                            help="Lower values = faster simulation")
    speed = 10. / speed_

    # Check if any parameter has changed
    parameters_changed = (
        new_numpoints != st.session_state.parameters['numpoints'] or
        new_num_infected != st.session_state.parameters['num_infected'] or
        new_movement != st.session_state.parameters['amount_of_movement'] or
        new_radius != st.session_state.parameters['radius_of_infection'] or
        new_probability != st.session_state.parameters['infection_probability']
    )
    
    if parameters_changed:
        st.session_state.parameters.update({
            'numpoints': new_numpoints,
            'num_infected': new_num_infected,
            'amount_of_movement': new_movement,
            'radius_of_infection': new_radius,
            'infection_probability': new_probability
        })
        handle_parameter_change()
    
    if 'simulator' not in st.session_state:
        handle_parameter_change()
    
    plot_placeholder = st.empty()
    fig, xy, c = st.session_state.plot_components
    
    if st.session_state.simulation_running:
        xy, c = next(st.session_state.simulator.stream)
        
        for i, state_name in enumerate(STATES.keys()):
            mask = (c == COLORS[state_name])
            if np.any(mask):
                try:
                    fig.data[i].x = xy[mask, 0]
                    fig.data[i].y = xy[mask, 1]
                except IndexError:
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
    
    plot_placeholder.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.simulation_running:
        time.sleep(speed)
        st.rerun()

if __name__ == "__main__":
    main()