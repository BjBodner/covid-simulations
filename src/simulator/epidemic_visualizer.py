import numpy as np
from plotly import graph_objects as go

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

    def create_figure(self) -> tuple[go.Figure, np.ndarray, np.ndarray]:
        xy: np.ndarray
        c: np.ndarray
        xy, c = next(self.stream)

        xy[: len(STATES), 0] = -BOX_SIZE * 2  # Move legend points out of the plot
        for i, color in enumerate(COLORS.values()):
            c[i] = color

        traces: list[go.Scatter] = []
        for state_name in STATES:
            mask = c == COLORS[state_name]
            if np.any(mask):
                traces.append(
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
                    )
                )

        fig = go.Figure(data=traces)
        fig.update_layout(
            width=800,
            height=800,
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.05),
            xaxis=dict(
                range=[-L, L], showgrid=False, zeroline=False, showticklabels=False
            ),
            yaxis=dict(
                range=[-L, L], showgrid=False, zeroline=False, showticklabels=False
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor="white",
        )

        return fig, xy, c
