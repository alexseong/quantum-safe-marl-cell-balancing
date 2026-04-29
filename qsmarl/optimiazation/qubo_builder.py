from dataclasses import dataclass
import numpy as np

from qsmarl.balancing.transfer_graph import TransferEdge


@dataclass
class QuboConfig:
    # Hyper parameters: weights for the each condition
    # A large negative value(-) for high reward
    # A large positive value(+) for high penalty 
