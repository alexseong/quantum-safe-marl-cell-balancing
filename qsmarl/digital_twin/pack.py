from dataclasses import dataclass
from typing import List
import numpy as np

from qsmarl.digital_twin.cell import CellState

print("Test pack")
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