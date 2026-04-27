from dataclasses import dataclass


@dataclass
class CellState:
    """
    State of a single lithium-ion cell.

    This is intentionally simple in v0.1
    Later versions will extend this with ECM status, RC voltages,
    hysteresis, parameter drift, and degradation states
    """

    soc: float
    voltage: float
    temparature: float
    soh: float
    capacity_ah: float
    internal_resistance_ohm: float


    