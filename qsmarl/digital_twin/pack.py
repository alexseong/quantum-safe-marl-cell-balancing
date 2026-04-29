from dataclasses import dataclass
from typing import List
import numpy as np

from qsmarl.digital_twin.cell import CellState, CellConfig, create_cell, soc_to_voltage


@dataclass
class BatteryPackConfig:
    num_cells: int = 8
    soc_min: float = 0.2
    soc_max: float = 0.9
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
        rng = np.random.default_rng(seed)
        socs = rng.uniform(
            self.config.soc_min,
            self.config.soc_max,
            size=self.config.num_cells,
        )

        cell_config = CellConfig(
            v_min=self.config.v_min,
            v_max=self.config.v_max,
            capacity_ah=self.config.capacity_ah,
            initial_temparature_c=self.config.initial_temparature_c,
            initial_soh=self.config.initial_soh,
            internal_resistance_ohm=self.config.internal_resistance_ohm,
        )

        self.cells = [create_cell(float(soc), cell_config) for soc in socs]

    def get_soc_array(self) -> np.ndarray:
        return np.array([cell.soc for cell in self.cells], dtype=np.float64)

    def get_temperature_array(self) -> np.ndarray:
        return np.array([cell.temparature for cell in self.cells], dtype=np.float64)


    def soc_variance(self) -> float:
        return float(np.var(self.get_soc_array()))
