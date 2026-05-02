from dataclasses import dataclass
import numpy as np

from qsmarl.balancing.transfer_graph import TransferEdge

####################################################################
## QUBO: Quadratic Unconstrained Binary Optimization
####################################################################

@dataclass
class QuboConfig:
    # Hyper parameters: weights for the each condition
    # A large negative value(-) for high reward
    # A large positive value(+) for high penalty 
    alpha_gap_reward: float = 10.0      # Reward for reducing SOC deviation
    beta_loss_penalty: float = 1.0      # Penalty for energy efficiency loss
    gamma_thermal_penalty: float = 1.0  # Penalty for temparature rise
    lambda_one_source: float = 20.0     # Weight constraint that a cell cannot discharge twice
    lambda_one_target: float = 20.0
    lambda_max_edges: float = 5.0
    max_active_edges: int = 2
    efficiency: float = 0.95


@dataclass
class QuboModel:
    Q: dict[tuple[str, str], float]
    varibles: list[str]
    edge_by_var: dict[str, TransferEdge]


class ActiveBalancingQuboBuilder:
    """
    Build QUBO for active cell balancing schedule selection

    Binary variable:
        x_i_j = 1 if energy transfer from cell i to cell j is selected.

    Objective:
        minimize:
            - SOC gap benefit
            + energy loss penalty
            + thermal penalty
            + routing constraint penaltie
    """

    def __init__(self, config: QuboConfig):
        self.config = config

    @staticmethod
    def var_name(edge: TransferEdge) -> str:
        return f"x_{edge.source}_{edge.target}"

    def build(
        self,
        edges: list[TransferEdge],
        temparatures: np.ndarray,
    ) -> QuboModel:
        Q: dict[tuple[str, str], float] = {}
        variables: list[str] = []
        edge_by_var: dict[str, TransferEdge] = {}

        for edge in edges:
            v = self.var_name(edge)
            variables.append(v)
            edge_by_var[v] = edge

            gap_benefit = -self.config.alpha_gap_reward * edge.soc_gap
            loss_penalty = -self.config.beta_loss_penalty * (1.0 - self.config.efficiency)
            thermal_penalty = self.config.gamma_thermal_penalty * (
                temparatures[edge.source] /100.0
            )

            linear = gap_benefit + loss_penalty + thermal_penalty
            Q[(v, v)] = Q.get((v, v), 0) + linear

        print(Q)

        self._add_one_source_constraint(Q, edges)

    def _add_one_source_constraint(
        self,
        Q: dict[tuple[str, str], float],
        edges: list[TransferEdge],
    ) -> None:
        """
            Penalize selecting multiple outoging transfers from the same source cell
        """



    


