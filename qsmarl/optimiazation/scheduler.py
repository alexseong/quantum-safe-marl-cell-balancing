from dataclasses import dataclass
import numpy as np

from qsmarl.balancing.transfer_graph import TransferEdge
from qsmarl.optimiazation.qubo_builder import ActiveBalancingQuboBuilder, QuboConfig
from qsmarl.optimiazation.ocean_solver import OceanQuboSolver


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
    - Returns selected active balancing routes
    """

    def __init__(
        self,
        qubo_config: QuboConfig | None = None,
        min_soc_gap: float = 0.02,
        num_reads: int = 100,
    ):
        self.qubo_config = qubo_config or QuboConfig()
        self.min_sop_gap = min_soc_gap
        self.builder = ActiveBalancingQuboBuilder(self.qubo_config)
        self.solver = OceanQuboSolver(num_reads=num_reads)

    # def 
