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

            # Assigne the net linear cost of selecting edge v to the diagonal entry Q(v, v) of the QUBO matrix.
            # - Store the linear term (representing the sum o fnet benefits and costs incurred 
            # - by selecting edge v) into the diagonal elements of the QUBO matrix.
            Q[(v, v)] = Q.get((v, v), 0) + linear


        self._add_one_source_constraint(Q, edges)
        self._add_one_target_constraint(Q, edges)
        self._add_max_edges_constraint(Q, variables)

        return QuboModel(Q=Q, varibles=variables, edge_by_var=edge_by_var )


    def _add_one_source_constraint(
        self,
        Q: dict[tuple[str, str], float],
        edges: list[TransferEdge],
    ) -> None:
        """
            Penalize selecting multiple outoging transfers from the same source cell.

            Constraint:
                sum_j x_ij <= 1

            QUBO penalty aproximation:
                lambda * x_a * x_b for all pairs sharing same source
        """
        lam = self.config.lambda_one_source

        for a_idx in range(len(edges)):
            for b_idx in range(a_idx + 1, len(edges)):
                e1 = edges[a_idx]
                e2 = edges[b_idx]

                if e1.source == e2.source:
                    v1 = self.var_name(e1)
                    v2 = self.var_name(e2)
                    key = tuple(sorted((v1, v2)))
                    Q[key] = Q.get(key, 0.0) + lam

    def _add_one_target_constraint(
        self,
        Q: dict[tuple[str, str], float],
        edges: list[TransferEdge],
    ) -> None:
        """
            Penalize selecting multiple incoming transfers into the same target cell.

            Constraint:
                sum_j x_ij <= 1

            QUBO penalty aproximation:
                lambda * x_a * x_b for all pairs sharing same source
        """
        lam = self.config.lambda_one_target

        for a_idx in range(len(edges)):
            for b_idx in range(a_idx + 1, len(edges)):
                e1 = edges[a_idx]
                e2 = edges[b_idx]

                if e1.target == e2.target:
                    v1 = self.var_name(e1)
                    v2 = self.var_name(e2)
                    key = tuple(sorted((v1, v2)))
                    Q[key] = Q.get(key, 0.0) + lam

    def _add_max_edges_constraint(
        self,
        Q: dict[tuple[str, str], float],
        variables: list[str],
    ) -> None:
        """
            Soft penalty for selecting too many active routes.

            For v0.1 we use a pairwise crowding penalty.
            Later this can be replaced by exact cardinality encoding.
        """
        lam = self.config.lambda_max_edges
        k = self.config.max_active_edges

        if k >= len(variables):
            return

        for i in range(len(variables)):
            for j in range(i+1, len(variables)):
                key = tuple(sorted((variables[i], variables[j])))
                Q[key] = Q.get(key, 0.0) + lam / max(1, k)





    


