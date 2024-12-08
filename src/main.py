import time

import numpy as np
import streamlit as st

from simulator.epidemic_visualizer import SimulationVisualizer
from utils.constants import STATES

st.set_page_config(
    layout="wide", page_title="Epidemic Spread simulation_visualizer", page_icon="🦠"
)


def handle_parameter_change() -> None:
    st.session_state.simulation_visualizer = SimulationVisualizer(
        numpoints=st.session_state.parameters["numpoints"],
        num_infected=st.session_state.parameters["num_infected"],
        amount_of_movement=st.session_state.parameters["amount_of_movement"],
        radius_of_possible_infection=st.session_state.parameters["radius_of_infection"],
        probability_of_getting_infected=st.session_state.parameters[
            "infection_probability"
        ],
    )
    st.session_state.plot_components = (
        st.session_state.simulation_visualizer.create_figure()
    )


def initialize_session_state() -> None:
    st.session_state.initialized = True
    st.session_state.simulation_running = True
    st.session_state.parameters = {
        "numpoints": 200,
        "num_infected": 5,
        "amount_of_movement": 0.25,
        "radius_of_infection": 1.5,
        "infection_probability": 0.1,
    }
    st.session_state.plot_placeholder = st.empty()
    handle_parameter_change()


def toggle_simulation() -> None:
    st.session_state.simulation_running = not st.session_state.simulation_running


def start_stop_simulation() -> None:
    cols = st.columns([1, 5])
    with cols[0]:
        st.button("Start/Pause", key="start_pause_button", on_click=toggle_simulation)
    with cols[1]:
        st.button("Reset", key="reset_button", on_click=handle_parameter_change)


def update_simulation_parameters() -> float:
    new_numpoints = st.sidebar.slider(
        "Population",
        50,
        500,
        st.session_state.parameters["numpoints"],
        key="numpoints_slider",
    )
    new_num_infected = st.sidebar.slider(
        "Initial Infected",
        1,
        20,
        st.session_state.parameters["num_infected"],
        key="infected_slider",
    )
    new_movement = st.sidebar.slider(
        "Movement Amount",
        0.0,
        1.0,
        st.session_state.parameters["amount_of_movement"],
        key="movement_slider",
    )
    new_radius = st.sidebar.slider(
        "Infection Radius",
        0.1,
        5.0,
        st.session_state.parameters["radius_of_infection"],
        key="radius_slider",
    )
    new_probability = st.sidebar.slider(
        "Infection Probability",
        0.0,
        1.0,
        st.session_state.parameters["infection_probability"],
        key="probability_slider",
    )

    inverse_speed = st.sidebar.slider(
        "Simulation Speed", 10.0, 100.0, 80.0, help="Lower values = faster simulation"
    )
    speed = 10.0 / inverse_speed

    # check if any parameters have changed
    parameters_changed = (
        new_numpoints != st.session_state.parameters["numpoints"]
        or new_num_infected != st.session_state.parameters["num_infected"]
        or new_movement != st.session_state.parameters["amount_of_movement"]
        or new_radius != st.session_state.parameters["radius_of_infection"]
        or new_probability != st.session_state.parameters["infection_probability"]
    )

    if parameters_changed:
        st.session_state.parameters.update(
            {
                "numpoints": new_numpoints,
                "num_infected": new_num_infected,
                "amount_of_movement": new_movement,
                "radius_of_infection": new_radius,
                "infection_probability": new_probability,
            }
        )
        handle_parameter_change()
    return speed


def render_simulation_visualization() -> None:
    fig, xy, s = st.session_state.plot_components

    if st.session_state.simulation_running:
        xy, s = next(st.session_state.simulation_visualizer.stream)
        st.session_state.simulation_visualizer.update_time_series(s)

        for i, (state_name, state_num) in enumerate(STATES.items()):
            mask = s == state_num
            if np.any(mask):
                fig.data[i].x = xy[mask, 0]
                fig.data[i].y = xy[mask, 1]

            fig.data[
                i + len(STATES)
            ].x = st.session_state.simulation_visualizer.timestamps
            fig.data[
                i + len(STATES)
            ].y = st.session_state.simulation_visualizer.time_series_data[state_name]

    st.session_state.plot_placeholder.plotly_chart(fig, use_container_width=True)


def render_static_elements() -> None:
    st.title("Epidemic Spread simulation_visualizer")
    st.sidebar.header("Simulation Parameters")


def main() -> None:
    render_static_elements()
    if "initialized" not in st.session_state:
        initialize_session_state()

    start_stop_simulation()
    speed = update_simulation_parameters()
    render_simulation_visualization()

    time.sleep(speed)
    st.rerun()


if __name__ == "__main__":
    main()
