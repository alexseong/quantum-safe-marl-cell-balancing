from dataclasses import dataclass

import dimod 

try:
    #dewave-neal was deprecated and merged to dewave-sampler  
    # import neal
    from dwave.sampler import SimulatedAnnealingSampler
except ImportError:
    # neal = None
    SimulatedAnnealingSampler = None

SimulatedAnnealingSampler = None

@dataclass
class SolverResult:
    sample: dict[str, int]
    energy: float


class OceanQuboSolver:
    """
    D-Wave Ocean-compatible QUBO solver.

    V0.1 uses simulated annealing through DWaveSampler if available,
    otherwise falls back to dimod ExactSolver for tiny problems.

    Later:
    - LeapHybridCQMSampler
    - hybrid solvers
    """

    def __init__(self, num_reads: int = 100):
        self.num_reads = num_reads

    def solve(self, Q: dict[tuple[str, str], float]) -> SolverResult:
        # 1. Create BQM
        bqm = dimod.BinaryQuadraticModel.from_qubo(Q)

        #2. Select Sampler         
        if SimulatedAnnealingSampler is not None:
            # sampler = neal.SimulatedAnnealingSampler()
            print("SimulatedAnnealingSampler")
            sampler = SimulatedAnnealingSampler()
            sampleset = sampler.sample(bqm, num_reads=self.num_reads)
        else:
            print("ExactSolver")
            sampler = dimod.ExactSolver()
            sampleset = sampler.sample(bqm)

        print(sampler)
        print(sampleset)

        #3. Extract result
        best = sampleset.first

        return SolverResult(
            sample=dict(best.sample),
            energy=float(best.energy)
        )