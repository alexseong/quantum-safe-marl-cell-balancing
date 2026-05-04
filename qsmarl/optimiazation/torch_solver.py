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
        # 1. Variable Mapping
        nodes = sorted(list(set([k for tup in Q.keys() for k in tup])))
        node_to_idx = { node: i for i, node in enumerate(nodes)}
        n = len(nodes)

        #2. Convert QUBO matrix to GPU tensor
        Q_matrix = torch.zeros((n, n), device='cuda', dtype=torch.float32)
        for (u, v), val in Q.items():
            ui, vi = node_to_idx[u], node_to_idx[v]
            Q_matrix[ui, vi] += val
            if ui != vi:
                Q_matrix[vi, ui] += val # Symetric matrix

        #3. Parallet Simulated Annealing (True SA)
        # Initialize states
        states = (torch.rand((self.num_reads, n), device='cuda') > 0.5).float()

        # Temperature Schedule 
        start_temp = 10.0
        end_temp = 0.01
        steps = 200

        temps = torch.linspace(start_temp, end_temp, steps)

        for T in temps:
            # x_Q for current energy calculation
            # Vector calculation of the energy change(dE) when each variable(n variable) is flipped
            for i in range(n):
                # Calculate the energy change when variable_i is flipped
                # dE = E(new) - E(old)
                q_i = Q_matrix[i, :]
                # dE_i = (1 - 2*x_i) * (Q_ii + sum_{j!=i} Q_ij * x_j)
                # (1 - 2 * x): 1 if x == 0, -1 if x ==  1
                dE = (1 - 2 * states[:, i]) * (Q_matrix[i, i] + torch.matmul(states, q_i) - Q_matrix[i, i] * states[:, i])

                # Metropolis Criterion: accept if dE < 0 or with prob exp(-dE/T)
                # 1. Accept unconditionally if dE < 0 (better solution)
                # 2. Accept with probability exp(-dE/T) (accept even if it's a worse solution to escape the local minimum)
                accept_prob = torch.exp(-dE / T)
                accept = (dE < 0) | (torch.rand(self.num_reads, device='cuda') < accept_prob)

                # Flip the i-th bit for accepted samples
                states[accept, i] = 1 - states[accept, i]
                

        #4. Extract optimized results
        final_x_Q = torch.matmul(states, Q_matrix)
        final_energies = torch.sum(final_x_Q * states, dim=1)

        min_e, min_idx = torch.min(final_energies, dim=0)
        best_sample = states[min_idx].cpu().int().numpy()

        #5. Formatting results
        sample_dict = {nodes[i]: int(best_sample[i]) for i in range(n)}

        print("best_energy:", float(min_e.item()))

        return SolverResult(
            sample=sample_dict,
            energy=float(min_e.item())
        )