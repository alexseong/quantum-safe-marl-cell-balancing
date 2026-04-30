from dataclasses import dataclass

import dimod 

try:
    import neal
except ImportError:
    neal = None


@dataclass
class SoverResult:
    sample: dict[str, int]
    energy: float


class OceanQuboSolver:
    """
    D-Wave Ocean-compatible QUBO solver.

    V0.1 uses simulated annealing through neal if available,
    otherwise falls back to dimod ExactSolver for tiny problems.

    Later:
    - DWaveSampler
    - LeapHybridCQMSampler
    - hybrid solvers
    """

    def __init__(self, num_reads: int = 100):
        self.num_reads = num_reads