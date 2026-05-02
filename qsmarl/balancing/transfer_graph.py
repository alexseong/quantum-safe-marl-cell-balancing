from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class TransferEdge:
    source: int
    target: int
    soc_gap: float
    

def build_candidate_edges(
    soc: np.ndarray,
    min_gap: float = 0.02,
) -> list[TransferEdge]:
    """
    Build feasible active balancing transfer candiates.
    Energy should flow from htigh-SOC to low-SOC cells.
    """
    edges: list[TransferEdge] = []

    n = len(soc)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            gap = float(soc[i] - soc[j])

            if gap >= min_gap:
                edges.append(TransferEdge(source=i, target=j, soc_gap=gap))

    return edges