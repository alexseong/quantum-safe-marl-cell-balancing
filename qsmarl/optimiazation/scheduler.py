from dataclasses import dataclass
import numpy as np

from qsmarl.balancing.transfer_graph import TransferEdge, build_candidate_edges
from qsmarl.optimiazation.qubo_builder import ActiveBalancingQuboBuilder, QuboConfig
from qsmarl.optimiazation.ocean_solver import OceanQuboSolver
from qsmarl.optimiazation.torch_solver import TorchIsingSolver


@dataclass
class ScheduleResult:
    selected_edges: list[TransferEdge]
    sample: dict[str, int]
    energy: float

class QuantumCompatibleScheduler:
    """
    Upper-level quantum-compatible optimization scheduler.

    In v0.1:
    - Build a QUBO from current pack state
    - Solves it using an Ocean-compatible solver
    - Use TorchIsingSolver because OceanQuboSolver has compatibility issue with numpy version(2.xx) 
    - Returns selected active balancing routes
    """

    def __init__(
        self,
        qubo_config: QuboConfig | None = None,
        min_soc_gap: float = 0.02,
        # num_reads: int = 100,  ## for Ocean
        num_reads: int = 1000, ## with GPU for torch ising solver
    ):
        self.qubo_config = qubo_config or QuboConfig()
        self.min_sop_gap = min_soc_gap
        self.builder = ActiveBalancingQuboBuilder(self.qubo_config)
        # self.solver = OceanQuboSolver(num_reads=num_reads)
        # Use Torch solver instead of D-Wave
        self.solver = TorchIsingSolver(num_reads=num_reads)

    def schedule(
        self, 
        soc: np.ndarray,
        temparatures: np.ndarray,
    ) -> ScheduleResult:

        edges = build_candidate_edges(soc=soc, min_gap=self.min_sop_gap)

        if not edges:
            return ScheduleResult(
                selected_edges=[],
                sample=[],
                energy=0.0
            )

        qubo_model = self.builder.build(edges, temparatures)
        solver_result = self.solver.solve(qubo_model.Q)

        selected_edges: list[TransferEdge] = []

        for var, value in solver_result.sample.items():
            if value == 1 and var in qubo_model.edge_by_var:
                selected_edges.append(qubo_model.edge_by_var[var])

        return ScheduleResult(
            selected_edges=selected_edges,
            sample=solver_result.sample,
            energy=solver_result.energy
        )