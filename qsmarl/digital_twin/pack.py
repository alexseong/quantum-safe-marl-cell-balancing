from dataclasses import dataclass
from typing import List
import numpy as np

from qsmarl.digital_twin.cell import CellState, CellConfig, create_cell, soc_to_voltage


@dataclass
class BatteryPackConfig:
    num_cells: int = 8
    soc_min: float = 0.2
    soc_min: float = 0.9
    v_min: float = 3.0
    v_max: float = 4.2
    capacity_ah: float = 3.4
    initial_temparature_c: float = 25.0
    initial_soh: float = 1.0
    internal_resistance_ohm: float = 0.02


class BatteryPack:
    """
    Simple battery pack digital twin.

    v0.1:
    - SOC-only dominant dynamics
    - Simple linear voltage model
    - Simple temparature increment due to balancing loss

    Later:
    - ECM
    - Thermal RC model
    - Aging model
    - Drive cycle/load current
    """

    def __init__(self, config: BatteryPackConfig):
        self.config=config
        self.cells: List[CellState] = []


    def reset_random(self, seed: int | None = None) -> None:
        pass