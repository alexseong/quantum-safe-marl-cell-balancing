from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class TransferEdge:
    source: int
    target: int
    soc_gap: float

    