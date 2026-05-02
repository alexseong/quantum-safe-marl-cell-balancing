import torch
import numpy as np
from dataclasses import dataclass


@dataclass
class SolverResult:
    sample: dict[str, int]
    energy: float


class TorchIsingSolver:
    """
    High speed Ising solver using PyTorch and GPU instead of D-Wave Ocean.
    """

    def __init__(self, num_reads: int = 1000):
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