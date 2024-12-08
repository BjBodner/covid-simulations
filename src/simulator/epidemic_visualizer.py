import numpy as np
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from simulator.epidemic_simulator import EpidemicSimulator
from utils.constants import BOX_SIZE, COLORS, SIZE, STATES

L = int(BOX_SIZE / 2)


class SimulationVisualizer:
    def __init__(
        self,
        numpoints: int = 100,
        num_infected: int = 5,
        amount_of_movement: float = 0.15,
        radius_of_possible_infection: float = 1,
        probability_of_getting_infected: float = 0.1,
    ) -> None:
        self.numpoints = numpoints
        self.stream = EpidemicSimulator(
            numpoints=numpoints,
            num_infected=num_infected,
            amount_of_movement=amount_of_movement,
            radius_of_possible_infection=radius_of_possible_infection,
            probability_of_getting_infected=probability_of_getting_infected,
        )
        self.time_series_data = {state: [] for state in STATES}
        self.timestamps = []
        self.current_time = 0

    def update_time_series(self, s: np.ndarray) -> None:
        """Update time series data with current state counts"""
        self.timestamps.append(self.current_time)
        for state_name, state_num in STATES.items():
            count = np.sum(s == state_num)
            self.time_series_data[state_name].append(count)
        self.current_time += 1

    def create_figure(self) -> tuple[go.Figure, np.ndarray, np.ndarray]:
        xy, s = next(self.stream)
        self.update_time_series(s)

        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=("Epidemic Spread", "Population States"),
            row_heights=[0.7, 0.3],
            vertical_spacing=0.1,
        )

        # Add scatter plot traces
        xy[: len(STATES), 0] = -BOX_SIZE * 2  # Move legend points out of the plot
        for state_num in STATES.values():
            s[state_num] = state_num

        for state_name, state_num in STATES.items():
            mask = s == state_num
            if np.any(mask):
                fig.add_trace(
                    go.Scatter(
                        x=xy[mask, 0],
                        y=xy[mask, 1],
                        mode="markers",
                        name=state_name,
                        marker=dict(
                            size=SIZE,
                            color=COLORS[state_name],
                            line=dict(width=1, color="black"),
                        ),
                        showlegend=True,
                    ),
                    row=1,
                    col=1,
                )

        # Add population tracking plot traces
        for state_name in STATES:
            fig.add_trace(
                go.Scatter(
                    x=self.timestamps,
                    y=self.time_series_data[state_name],
                    mode="lines",
                    name=f"{state_name} (count)",
                    line=dict(color=COLORS[state_name]),
                    showlegend=True,
                ),
                row=2,
                col=1,
            )

        fig.update_layout(
            width=800,
            height=700,
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.05),
            margin=dict(l=0, r=0, t=30, b=0),
            plot_bgcolor="white",
        )
        fig.update_xaxes(
            range=[-L, L],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            row=1,
            col=1,
        )
        fig.update_yaxes(
            range=[-L, L],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            row=1,
            col=1,
        )
        fig.update_xaxes(title_text="Time", showgrid=True, row=2, col=1)
        fig.update_yaxes(
            title_text="Population", showgrid=True, showticklabels=False, row=2, col=1
        )

        return fig, xy, s
